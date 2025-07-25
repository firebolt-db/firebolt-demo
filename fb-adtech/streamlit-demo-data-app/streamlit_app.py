"""A demo data app using Streamlit on top of Firebolt."""
import time
import pandas as pd
import streamlit as st
from firebolt.db import connect
from firebolt.client import DEFAULT_API_URL
from firebolt.client.auth import ClientCredentials

from numerize import numerize
import datetime
from fastavro import reader

# page config
st.set_page_config(layout="wide", page_title="Firebolt AdTech data app demo", page_icon="firebolt-logo.png")

# sidebar with parameters, bound to session state
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')

    with col2:
        st.image("firebolt-logo.png")

    with col3:
        st.write(' ')

    st.sidebar.title(f"Welcome!")

    st.write(
        """
        This demo data app was built using Streamlit on top of Firebolt. 
        Uses Firebolt Python SDK and the AdTech demo dataset (60 billion rows).
        """
    )

    sidebar_row2 = st.columns((2, 3))

    date_from_selected = st.date_input("Date from and to", value=(datetime.date(year=2025, month=2, day=1), datetime.date(year=2025, month=2, day=15)), key='date_from_to', help="Choose the start and end date")
    
    media_sources = st.multiselect('Media Source', ['source_a', 'source_b', 'source_c'], ['source_a'], key='media_sources', help="Choose one or more media sources")
    

# get data from Firebolt
@st.cache_resource(show_spinner=False)
def load_adtech_data(date_from_to, media_sources_tuple):
    date_from = date_from_to[0]
    date_to = date_from_to[0]
    if (len(date_from_to) == 2):
        date_to = date_from_to[1]
    
    if (len(media_sources_tuple) == 0):
        media_sources_tuple = ('3bc36bb9f1bded2703684dae170581dc', 'e391b3d1930968f4cce0d5dee539d256', 'b935fcce8f277b6c60cd7598349c64e8')
    media_sources = ','.join(tuple('\'{}\''.format(x) for x in media_sources_tuple))

    username = st.secrets["db_username"]
    password = st.secrets["db_password"]
    api_endpoint = DEFAULT_API_URL

    connection = connect(
        engine_name="ENGINE_NAME",
        database="DB_NAME",
        account_name="ACCOUNT_NAME",
        auth=ClientCredentials(username, password)
    )

    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN (attribution_type = 'install') THEN clicks_count  ELSE NULL END), 0) AS "Total Clicks Count"
            ,COALESCE(SUM(CASE WHEN (attribution_type = 'install') THEN impressions_count  ELSE NULL END), 0) AS "Total Impressions Count"
            ,COALESCE(SUM(inappevents_count ), 0) AS "Total In App Events Count"
            ,COALESCE(SUM(launches_count ), 0) AS "Total Launches Count"
            ,COALESCE(SUM(CASE WHEN (attribution_type = 'install') THEN installs_count  ELSE NULL END), 0) AS "Total NOI Count"
            FROM
            "ltv" AS "ltv"
            WHERE
                "ltv"."ltv_timestamp_dt" >= ( '%s')
                AND "ltv"."ltv_timestamp_dt" <= ( '%s')
                AND "ltv"."media_source" IN (%s)
            """ % (date_from, date_to, media_sources))
    kpis = cursor.fetchall()[0]
    launches = kpis[3]
    noi = kpis[4]
    inappevents = kpis[2]
    impressions = kpis[1]
    clicks = kpis[0]

    select = """SELECT
                        TO_DATE("ltv"."ltv_timestamp_dt") AS "Date"
                        ,COALESCE(SUM(CASE WHEN (attribution_type = 'install') THEN clicks_count  ELSE NULL END), 0) AS "Clicks"
                        ,COALESCE(SUM(CASE WHEN (attribution_type = 'install') THEN impressions_count  ELSE NULL END), 0) AS "Impressions"
                        ,COALESCE(SUM(inappevents_count ), 0) AS "Total Inappevents Count"
                        ,COALESCE(SUM(launches_count ), 0) AS "Total Launches Count"
                        ,COALESCE(SUM(CASE WHEN (attribution_type = 'install') THEN installs_count  ELSE NULL END), 0) AS "NOI"
                    FROM
                       "ltv" AS "ltv"
                    WHERE 
                        "ltv"."ltv_timestamp_dt" >= ( '%s') 
                        AND "ltv"."ltv_timestamp_dt" <= ( '%s') 
                        AND "ltv"."media_source" IN (%s)
                    GROUP BY 1
                    ORDER BY 1""" % (date_from, date_to, media_sources)
    daily_funnel = pd.read_sql(select, connection)
    daily_funnel = pd.melt(daily_funnel, id_vars='Date', value_vars=['Impressions','Clicks'])

    select = """WITH ltv AS (
                SELECT 
                    ltv.*
                    ,acc.name AS acc_name
                    ,acc.shipping_country
                    ,acc.region
                    ,app.name AS app_name
                    ,app.platform
                    ,app.app_slug
                    ,app.owner_account
                FROM 
                    ltv
                LEFT JOIN 
                    owned_apps AS app 
                    ON CITY_HASH(ltv.app_id) = CITY_HASH(app.app_slug)
                LEFT JOIN 
                    account AS acc 
                    ON CITY_HASH(acc.id) = CITY_HASH(app.owner_account) 
                )
            SELECT
                app_name AS "App Name"
                ,media_source AS "Media Source"
                ,acc_name AS "Account Name"
                ,shipping_country AS "Shipping Country"
                ,region AS "Region"
                ,platform AS "Platform"
                ,COALESCE(SUM(CASE WHEN (attribution_type = 'install') THEN clicks_count  ELSE NULL END), 0) AS "Total Clicks Count"
                ,COALESCE(SUM(CASE WHEN (attribution_type = 'install') THEN impressions_count  ELSE NULL END), 0) AS "Total Impressions Count"
                ,COALESCE(SUM(inappevents_count ), 0) AS "Total Inappevents Count"
                ,COALESCE(SUM(launches_count ), 0) AS "Total Launches Count"
                ,COALESCE(SUM(CASE WHEN (attribution_type = 'install') THEN installs_count  ELSE NULL END), 0) AS "Total NOI Count"
            FROM 
                ltv
            WHERE
                (((ltv_timestamp_dt) >= (TIMESTAMP '%s') 
                AND (ltv_timestamp_dt) < (TIMESTAMP '%s')))
                AND ltv.media_source IN (%s)
            GROUP BY 
            ALL
            ORDER BY 
            7 DESC
            %s""" % (date_from, date_to, media_sources, "LIMIT 100")
    perf_summary = pd.read_sql(select, connection)        
    connection.close()

    return {
        "impressions" : impressions,
        "launches" : launches,
        "clicks" : clicks,
        "inappevents" : inappevents,
        "noi" : noi,
        "daily_funnel" : daily_funnel,
        "performance_summary" : perf_summary
    }
    
# get data based on selected parameters from the session
with st.spinner('Fetching data and rendering...'):
    adtech_data = load_adtech_data(st.session_state['date_from_to'], st.session_state['media_sources'])

st.title("Firebolt AdTech data app")

# main KPIs
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="Clicks", value=numerize.numerize(adtech_data["clicks"]), help = "Total Clicks KPI")
col2.metric(label="Impressions", value=numerize.numerize(adtech_data["impressions"]), help = "Total Impressions KPI")
col3.metric(label="In App Events", value=numerize.numerize(adtech_data["inappevents"]), help = "In App Events KPI")
col4.metric(label="Launches", value=numerize.numerize(adtech_data["launches"]), help = "Launches KPI")
col5.metric(label="NOI", value=numerize.numerize(adtech_data["noi"]), help = "NOI KPI")

row2 = st.columns((2, 3))


# chart element (vegalite)
st.vega_lite_chart(
    adtech_data["daily_funnel"],
    {
        'mark': {
            'type': 'bar',
            'tooltip': True,
            'width': 10,  # thinner bars
            'cornerRadiusTopLeft': 2,
            'cornerRadiusTopRight': 2
        },
        'encoding': {
            'x': {
                'field': 'Date',
                'type': 'temporal',
                'timeUnit': 'yearmonthdate',
                'axis': {
                    'title': 'Date',
                    'labelAngle': -40,
                    'format': '%b %d',
                    'labelFontSize': 12
                }
            },
            'y': {
                'field': 'value',
                'type': 'quantitative',
                'stack': 'zero',
                'axis': {
                    'title': 'Count',
                    'format': '~s',
                    'labelFontSize': 12
                }
            },
            'color': {
                'field': 'variable',
                'scale': {
                    'range': ['#FF0E0E', '#E9EBF2']  # Clicks = red, Impressions = light gray
                },
                'legend': {
                    'title': 'Metric',
                    'labelFontSize': 12,
                    'titleFontSize': 14
                }
            },
            'tooltip': [
                {'field': 'Date', 'type': 'temporal', 'title': 'Date'},
                {'field': 'variable', 'type': 'nominal', 'title': 'Metric'},
                {'field': 'value', 'type': 'quantitative', 'title': 'Value', 'format': ',d'}
            ]
        },
        'config': {
            'axis': {'grid': False},
            'bar': {'binSpacing': 2},
            'background': '#FFFFFF'
        }
    },
    use_container_width=True
)

# table element
cols = [
    "Total Impressions Count",
    "Total Clicks Count",
    "Total NOI Count",
    "Total Inappevents Count",
    "Total Launches Count"
]
st.dataframe(
    adtech_data["performance_summary"]
    .style
    .highlight_max(subset=cols, color="green", axis=0)
    .format({col: "{:,.0f}" for col in cols}),  # No decimals, with comma separators
    use_container_width=True
)