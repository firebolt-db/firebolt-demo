const { Pool } = require('pg');
const { faker } = require('@faker-js/faker');

const pool = new Pool({
  user: 'admin',
  host: 'localhost',
  database: 'postgres',
  password: 'admin',
  port: 5432,
});

const sports = ['Basketball', 'Football', 'Baseball', 'Soccer'];
const leagues = {
  Basketball: ['NBA'],
  Football: ['NFL'],
  Baseball: ['MLB'],
  Soccer: ['EPL', 'La Liga', 'Bundesliga'],
};

const bookmakers = ['DraftKings', 'FanDuel', 'BetMGM', 'Caesars'];
const markets = ['moneyline', 'spread', 'total'];
const outcomes = {
  moneyline: ['home', 'away'],
  spread: ['home', 'away'],
  total: ['over', 'under'],
};


function pluralize(word) {
  if (word.endsWith('y')) {
    return word.slice(0, -1) + 'ies';
  }
  if (word.endsWith('s')) {
    return word;
  }
  return word + 's';
}

function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}


async function createFakeGame() {
  const sport = faker.helpers.arrayElement(sports);
  const league = faker.helpers.arrayElement(leagues[sport]);
  const homeTeam = faker.location.city() + ' ' + capitalize(pluralize(faker.animal.type()));
  const awayTeam = faker.location.city() + ' ' + capitalize(pluralize(faker.animal.type()));
  const commenceTime = faker.date.soon(7); // within next week

  const { rows } = await pool.query(
    `INSERT INTO games (sport, league, home_team, away_team, commence_time) VALUES ($1, $2, $3, $4, $5) RETURNING game_id`,
    [sport, league, homeTeam, awayTeam, commenceTime]
  );
  return rows[0].game_id;
}

async function createFakeOdds(gameId, numSnapshots = 10) {
  for (let snapshot = 0; snapshot < numSnapshots; snapshot++) {
    for (const bookmaker of bookmakers) {
      for (const market of markets) {
        const priceHome = faker.number.float({ min: 1.5, max: 3.5, precision: 0.01 });
        const priceAway = faker.number.float({ min: 1.5, max: 3.5, precision: 0.01 });

        // Simulate slightly different fetched_at times
        const fetchedAt = new Date(Date.now() - snapshot * 60 * 1000); // Each snapshot 1 minute apart

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
  }
}


async function generateFakeData(numGames = 10) {
  for (let i = 0; i < numGames; i++) {
    const gameId = await createFakeGame();
    await createFakeOdds(gameId);
  }
  console.log(`Inserted ${numGames} fake games with odds.`);
  await pool.end();
}

generateFakeData(10);
