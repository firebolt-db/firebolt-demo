import time
import pandas as pd
import streamlit as st
from firebolt.db import connect
from firebolt.client.auth import ClientCredentials
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ---- Config ----
REFRESH_INTERVAL = 5

# ---- Streamlit Setup ----
st.set_page_config(page_title="🔥 Odds Tracker", layout="wide")

# Initialize session state
if "selected_sport" not in st.session_state:
    st.session_state["selected_sport"] = "Soccer"
if "last_update" not in st.session_state:
    st.session_state["last_update"] = datetime.now()

# ---- Firebolt Connection ----
@st.cache_resource
def get_connection():
    return connect(
        engine_name="debezium_ingestion",
        database="demo_debezium_cdc",
        account_name="YOUR-ACCOUNT-NAME",
        auth=ClientCredentials(
            client_id="YOUR-CLIENT-ID",
            client_secret="YOUR-CLIENT-SECRET"
        )
    )

conn = get_connection()

# ---- Custom CSS ----
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .sport-selector {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 20px 0;
    }
    
    .sport-icon {
        width: 80px;
        height: 80px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        margin: 0 auto;
    }
    
    .sport-icon:hover {
        transform: translateX(5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .sport-icon.active {
        background-color: #c8ff00;
        border-color: #a8df00;
    }
    
    .sport-icon.inactive {
        background-color: #f0f0f0;
        border-color: #ddd;
    }
    
    .game-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #eee;
    }
    
    .game-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .odds-card {
        background: white;
        border: 2px solid #eee;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .odds-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    .bookmaker-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #666;
        margin-bottom: 10px;
    }
    
    .odds-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .odds-green { color: #28a745; border-color: #28a745; }
    .odds-blue { color: #007bff; border-color: #007bff; }
    .odds-orange { color: #fd7e14; border-color: #fd7e14; }
    .odds-red { color: #dc3545; border-color: #dc3545; }
    
    .update-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #28a745;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        z-index: 1000;
    }
    
    .streaming-status {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    .streaming-dot {
        width: 12px;
        height: 12px;
        background: #28a745;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ---- Queries with Caching ----
@st.cache_data(ttl=30)  # Cache for 30 seconds
def query_games(sport_filter=None):
    if sport_filter:
        query = f"""
            SELECT DISTINCT g.game_id, g.home_team, g.away_team, g.commence_time, g.sport
            FROM cdc_public_games g
            JOIN cdc_public_odds_history o ON g.game_id = o.game_id
            WHERE g.sport = '{sport_filter}'
            ORDER BY g.commence_time DESC LIMIT 100
        """
    else:
        query = """
            SELECT DISTINCT g.game_id, g.home_team, g.away_team, g.commence_time, g.sport
            FROM cdc_public_games g
            JOIN cdc_public_odds_history o ON g.game_id = o.game_id
            ORDER BY g.commence_time DESC LIMIT 100
        """
    return pd.read_sql(query, conn)

@st.cache_data(ttl=5)  # Cache for 5 seconds for more frequent updates
def query_latest_odds(game_id):
    return pd.read_sql(f"""
        SELECT 
        o.bookmaker, MAX_BY(o.price, o.fetched_at) AS "Latest Odds"
        FROM cdc_public_odds_history o
        JOIN cdc_public_games g ON o.game_id = g.game_id
        WHERE o.game_id = {game_id}
        GROUP BY o.bookmaker
        ORDER BY o.bookmaker
    """, conn)

@st.cache_data(ttl=60)  # Cache history for 1 minute
def query_odds_history(game_id, bookmaker=None):
    query = f"""
        SELECT 
        o.bookmaker, DATE_TRUNC('minute', o.fetched_at) as "Time", MAX_BY(o.price, o.fetched_at) as "Odds"
        FROM cdc_public_odds_history o
        JOIN cdc_public_games g ON o.game_id = g.game_id
        WHERE o.game_id = {game_id}
    """
    if bookmaker:
        query += f" AND o.bookmaker = '{bookmaker}'"
    query += """
        GROUP BY o.bookmaker, DATE_TRUNC('minute', o.fetched_at)
        ORDER BY "Time"
    """
    return pd.read_sql(query, conn)

def create_mini_chart(game_id, bookmaker, color):
    """Create a mini sparkline chart for odds history"""
    hist_df = query_odds_history(game_id, bookmaker)
    if hist_df.empty:
        return None
    
    color_map = {
        '#28a745': 'rgba(40, 167, 69, 0.1)',
        '#007bff': 'rgba(0, 123, 255, 0.1)', 
        '#fd7e14': 'rgba(253, 126, 20, 0.1)',
        '#dc3545': 'rgba(220, 53, 69, 0.1)'
    }
    fill_color = color_map.get(color, 'rgba(128, 128, 128, 0.1)')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist_df['Time'],
        y=hist_df['Odds'],
        mode='lines',
        line=dict(color=color, width=3),
        fill='tonexty',
        fillcolor=fill_color,
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        height=40,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

# ---- Header ----
st.markdown('<div class="main-header">Sports Odds Tracker</div>', unsafe_allow_html=True)

# ---- Streaming Status Indicator ----
st.markdown(f"""
<div class="streaming-status">
    <div class="streaming-dot"></div>
    <span>Live streaming • Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}</span>
</div>
""", unsafe_allow_html=True)

# ---- Layout: Sidebar for Sports + Main Content ----
sidebar_col, main_col = st.columns([1, 4])

with sidebar_col:
    st.markdown("### Sports")
    
    # ---- Sport Selector ----
    sports = [
        ("Soccer", "⚽", "Soccer"),
        ("Basketball", "🏀", "Basketball"), 
        ("Football", "🏈", "Football"),
        ("Baseball", "⚾", "Baseball")
    ]
    
    for sport_key, icon, name in sports:
        if st.button(f"{icon}", key=f"sport_{sport_key}", help=name, use_container_width=True):
            st.session_state.selected_sport = sport_key
            st.cache_data.clear()  # Clear cache when sport changes
            st.rerun()

with main_col:
    # ---- Create containers for dynamic content ----
    header_container = st.container()
    content_container = st.container()
    
    with header_container:
        selected_sport_name = next((name for key, _, name in sports if key == st.session_state.selected_sport), "Unknown")
        st.markdown(f"## {selected_sport_name} Games")
    
    # ---- Use st.empty() for dynamic content updates ----
    games_placeholder = st.empty()
    
    with games_placeholder.container():
        # Load Games Data
        games = query_games(st.session_state.selected_sport)
        
        if games.empty:
            st.warning(f"No games found for {selected_sport_name}")
        else:
            # Display Games
            for idx, game in games.iterrows():
                with st.container():
                    st.markdown(f"""
                        <div class="game-card">
                            <div class="game-title">{game['away_team']} @ {game['home_team']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Get odds for this game
                    odds_df = query_latest_odds(game['game_id'])
                    
                    if not odds_df.empty:
                        # Create columns for odds cards
                        num_bookmakers = len(odds_df)
                        cols = st.columns(min(4, num_bookmakers))
                        
                        colors = ['#28a745', '#007bff', '#fd7e14', '#dc3545']
                        color_classes = ['odds-green', 'odds-blue', 'odds-orange', 'odds-red']
                        
                        for i, (_, odds_row) in enumerate(odds_df.iterrows()):
                            col_idx = i % 4
                            color = colors[col_idx]
                            color_class = color_classes[col_idx]
                            
                            with cols[col_idx]:
                                # Create mini chart
                                mini_fig = create_mini_chart(game['game_id'], odds_row['bookmaker'], color)
                                
                                st.markdown(f"""
                                    <div class="odds-card {color_class}">
                                        <div class="bookmaker-name">{odds_row['bookmaker']}</div>
                                        <div class="odds-value">{odds_row['Latest Odds']:.1f}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                # Add mini chart if available
                                if mini_fig:
                                    st.plotly_chart(mini_fig, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.info("No odds available for this game")
                    
                    st.markdown("<br>", unsafe_allow_html=True)

# ---- Auto-refresh using st.rerun with fragment ----
if st.button("🔄 Refresh Now", type="secondary"):
    st.cache_data.clear()
    st.session_state.last_update = datetime.now()
    st.rerun()

# ---- Auto-refresh timer (more elegant approach) ----
refresh_placeholder = st.empty()
refresh_placeholder.caption("🔄 Auto-refresh enabled • Click 'Refresh Now' for immediate update")

# Optional: Add a toggle for auto-refresh
auto_refresh = st.sidebar.checkbox("Enable Auto-refresh", value=True)
if auto_refresh:
    time.sleep(REFRESH_INTERVAL)
    st.session_state.last_update = datetime.now()
    st.rerun()