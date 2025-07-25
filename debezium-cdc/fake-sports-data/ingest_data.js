const { Pool } = require('pg');
const { faker } = require('@faker-js/faker');

const pool = new Pool({
  user: 'admin',
  host: 'localhost',
  database: 'postgres',
  password: 'admin',
  port: 5432,
});

const bookmakers = ['DraftKings', 'FanDuel', 'BetMGM', 'Caesars'];
const markets = ['moneyline', 'spread', 'total'];
const outcomes = {
  moneyline: ['home', 'away'],
  spread: ['home', 'away'],
  total: ['over', 'under'],
};

async function getGameTimestamps() {
  const res = await pool.query(`
    SELECT game_id, MAX(fetched_at) as last_fetched
    FROM odds_history
    GROUP BY game_id
  `);
  const gameTimestamps = {};
  for (const row of res.rows) {
    gameTimestamps[row.game_id] = new Date(row.last_fetched).getTime();
  }
  return gameTimestamps;
}

async function getAllGameIds() {
  const res = await pool.query(`SELECT game_id FROM games`);
  return res.rows.map(row => row.game_id);
}

async function insertOddsForGames(gameIds, previousTimestamps) {
  for (const gameId of gameIds) {
    const lastTimestamp = previousTimestamps[gameId] || Date.now();
    const fetchedAt = new Date(lastTimestamp + 30_000); // +30 seconds

    for (const bookmaker of bookmakers) {
      for (const market of markets) {
        const priceHome = faker.number.float({ min: 1.5, max: 3.5, precision: 0.01 });
        const priceAway = faker.number.float({ min: 1.5, max: 3.5, precision: 0.01 });

        await pool.query(
          `INSERT INTO odds_history (game_id, bookmaker, market, outcome, price, fetched_at)
           VALUES ($1, $2, $3, $4, $5, $6)`,
          [gameId, bookmaker, market, outcomes[market][0], priceHome, fetchedAt]
        );

        await pool.query(
          `INSERT INTO odds_history (game_id, bookmaker, market, outcome, price, fetched_at)
           VALUES ($1, $2, $3, $4, $5, $6)`,
          [gameId, bookmaker, market, outcomes[market][1], priceAway, fetchedAt]
        );
      }
    }

    previousTimestamps[gameId] = fetchedAt.getTime();
    console.log(`✅ Inserted new odds for game ${gameId} at ${fetchedAt.toISOString()}`);
  }
}

async function main() {
  const startTime = Date.now();
  const runDuration = 5 * 60 * 1000; // 5 minutes
  const previousTimestamps = await getGameTimestamps();

  while (Date.now() - startTime < runDuration) {
    try {
      const gameIds = await getAllGameIds();
      if (gameIds.length === 0) {
        console.log("⚠️ No games found. Waiting...");
      } else {
        await insertOddsForGames(gameIds, previousTimestamps);
      }
    } catch (err) {
      console.error("❌ Error inserting odds:", err);
    }

    await new Promise(resolve => setTimeout(resolve, 5_000)); // wait 30 sec
  }

  console.log("🛑 5 minutes elapsed. Ending script.");
  await pool.end();
}

main();
