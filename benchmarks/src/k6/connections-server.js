const express = require("express");
const fs = require("fs");
const path = require("path");

function parseArgs(argv) {
  const argsMap = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      let value = true;
      if (i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
        value = argv[i + 1];
        i++;
      }
      argsMap[key] = value;
    }
  }
  return argsMap;
}

// Load environment variables from .env file if available
const dotenvPath = path.resolve(__dirname, "../../.env");
if (fs.existsSync(dotenvPath)) {
  const envContent = fs.readFileSync(dotenvPath, "utf-8");
  const envLines = envContent.split("\n");
  envLines.forEach(line => {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith("#") && trimmed.includes("=")) {
      const [key, ...valueParts] = trimmed.split("=");
      const value = valueParts.join("=");
      if (!process.env[key.trim()]) {
        process.env[key.trim()] = value.trim();
      }
    }
  });
}

// Legacy credentials file support (optional)
const argMap = parseArgs(process.argv.slice(2));
const credsFile = argMap.creds;
let credsConfig = {};
if (credsFile) {
  const credsPath = path.isAbsolute(credsFile)
    ? credsFile
    : path.resolve(process.cwd(), credsFile);
  try {
    if (fs.existsSync(credsPath)) {
      const rawCredsJson = fs.readFileSync(credsPath, "utf-8");
      credsConfig = JSON.parse(rawCredsJson);
      console.log("Using legacy credentials file:", credsPath);
    }
  } catch (err) {
    console.warn("Could not read or parse credentials file:", err);
  }
} else {
  console.log("Using environment variables for credentials");
}

const k6ConfigPath = "../../config/k6config.json"; 
let k6Config = {} 
try {
  if (fs.existsSync(k6ConfigPath)) {
    const rawConfigJson = fs.readFileSync(k6ConfigPath, "utf-8");
    k6Config = JSON.parse(rawConfigJson);
  }
} catch (err) {
  console.warn("Could not read or parse K6 config file:", err);
}


// Prioritize environment variables over legacy credentials file
const fileFirebolt = credsConfig.firebolt ?? {};
const fileFireboltAuth = fileFirebolt.auth ?? {};
const FIREBOLT_ENGINE        = process.env.FIREBOLT_ENGINE_NAME || fileFirebolt.engine_name;
const FIREBOLT_DB            = process.env.FIREBOLT_DATABASE || fileFirebolt.database;
const FIREBOLT_ACCOUNT       = process.env.FIREBOLT_ACCOUNT_NAME || fileFirebolt.account_name;
const FIREBOLT_CLIENT_ID     = process.env.FIREBOLT_SERVICE_ID || fileFireboltAuth.id;
const FIREBOLT_CLIENT_SECRET = process.env.FIREBOLT_SERVICE_SECRET || fileFireboltAuth.secret;

const fileSnowflake = credsConfig.snowflake ?? {};
const SNOWFLAKE_ACCOUNT      = process.env.SNOWFLAKE_ACCOUNT || fileSnowflake.account;
const SNOWFLAKE_USERNAME     = process.env.SNOWFLAKE_USER || fileSnowflake.user;
const SNOWFLAKE_PASSWORD     = process.env.SNOWFLAKE_PASSWORD || fileSnowflake.password;
const SNOWFLAKE_WAREHOUSE    = process.env.SNOWFLAKE_WAREHOUSE || fileSnowflake.warehouse;
const SNOWFLAKE_DATABASE     = process.env.SNOWFLAKE_DATABASE || fileSnowflake.database;
const SNOWFLAKE_SCHEMA       = process.env.SNOWFLAKE_SCHEMA || fileSnowflake.schema;

const fileRedshift = credsConfig.redshift ?? {};
const REDSHIFT_HOST          = process.env.REDSHIFT_HOST || fileRedshift.host;
const REDSHIFT_PORT          = process.env.REDSHIFT_PORT || fileRedshift.port;
const REDSHIFT_DATABASE      = process.env.REDSHIFT_DATABASE || fileRedshift.database;
const REDSHIFT_USER          = process.env.REDSHIFT_USER || fileRedshift.user;
const REDSHIFT_PASSWORD      = process.env.REDSHIFT_PASSWORD || fileRedshift.password;
const REDSHIFT_SSL           = process.env.REDSHIFT_SSL || fileRedshift.ssl;


const { Firebolt } = require("firebolt-sdk");
const snowflake = require("snowflake-sdk");
const { Client: RedshiftClient } = require("pg");

const app = express();
app.use(express.json());

const CONNECTIONS_PER_THREAD = k6Config.connections_per_thread || 10;
const VENDOR = k6Config.vendor ?? "firebolt";

if (VENDOR === "snowflake") {
  snowflake.configure({
    logLevel: "ERROR",
    logFilePath: "/dev/null",
    additionalLogToConsole: true
  });
}



// Map for storing connections by VU ID
// Key: vuID (string or number)
// Value: a database connection instance
const connections = new Map();


async function getFireboltConnection(vuID) {
  if (!connections.has(vuID)) {
    const firebolt = Firebolt();
    const conn = await firebolt.connect({
      auth: {
        client_id: FIREBOLT_CLIENT_ID,
        client_secret: FIREBOLT_CLIENT_SECRET,
      },
      engineName: FIREBOLT_ENGINE,
      account: FIREBOLT_ACCOUNT,
      database: FIREBOLT_DB
    });
    connections.set(vuID, conn);
    await connections.get(vuID).execute("SET enable_result_cache=false")
  }
  return connections.get(vuID);
}

function connectSnowflakeAsync(conn) {
  return new Promise((resolve, reject) => {
    conn.connect((err, connResult) => {
      if (err) {
        return reject(err);
      }
      resolve(connResult);
    });
  });
}

async function getSnowflakeConnection(vuID, privateKey) {
  if (!connections.has(vuID)) {
    const conn = snowflake.createConnection({
      account: SNOWFLAKE_ACCOUNT,
      username: SNOWFLAKE_USERNAME,
      password: SNOWFLAKE_PASSWORD,
      warehouse: SNOWFLAKE_WAREHOUSE,
      database: SNOWFLAKE_DATABASE,
      schema: SNOWFLAKE_SCHEMA,
      logLevel: 'ERROR'
    });
    await connectSnowflakeAsync(conn);
    connections.set(vuID, conn);
    await new Promise((resolve, reject) => {
      connections.get(vuID).execute({
        sqlText: "ALTER SESSION SET USE_CACHED_RESULT = FALSE;",
        complete: (err, stmt, data) => {
          if (err) {
            return reject(err);
          }
          resolve(data);
        }
      });
    });
  }
  return connections.get(vuID);
}

async function getRedshiftConnection(vuID) {
  if (!connections.has(vuID)) {
    // Build options for node-postgres
    const clientConfig = {
      host: REDSHIFT_HOST,
      port: parseInt(REDSHIFT_PORT, 10) || 5439,
      database: REDSHIFT_DATABASE,
      user: REDSHIFT_USER,
      password: REDSHIFT_PASSWORD,
    };
    // If SSL is desired
    if (REDSHIFT_SSL === "true") {
      clientConfig.ssl = {
        rejectUnauthorized: false
      };
    }

    const client = new RedshiftClient(clientConfig);
    await client.connect();
    connections.set(vuID, client);
    await connections.get(vuID).query("SET enable_result_cache_for_session TO off;");
  }
  return connections.get(vuID);
}

// POST /execute endpoint
app.post("/execute", async (req, res) => {
  try {
    const { query, vuID } = req.body;
    if (!query || !vuID) {
      return res
        .status(400)
        .json({ error: "Both 'query' and 'vuID' fields are required" });
    }

    if (VENDOR === "firebolt") {
      const conn = connections.get((vuID % CONNECTIONS_PER_THREAD) + 1);
      const statement = await conn.execute(query);
      const { data } = await statement.fetchResult();
    } else if (VENDOR === "snowflake") {
      const conn = connections.get((vuID % CONNECTIONS_PER_THREAD) + 1);
      await new Promise((resolve, reject) => {
        conn.execute({
          sqlText: query,
          complete: (err, stmt, rows) => {
            if (err) {
              return reject(err);
            }
            resolve(rows);
          }
        });
      });
    } else if (VENDOR === "redshift") {
      const conn = connections.get((vuID % CONNECTIONS_PER_THREAD) + 1);
      const result = await conn.query(query);
    } else {
      return res.status(400).json({ error: `Unknown VENDOR: ${VENDOR}` });
    }

    res.json({ success: true });
  } catch (error) {
    console.error("Query execution error:", error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/health', (req, res) => {
  res.send('OK');
});

// Start the server
(async function startServer() {
  try {
    const numServerConnections = parseInt(CONNECTIONS_PER_THREAD, 10) || 1;

    // Pre-init connections
    console.log(`Pre-initializing ${numServerConnections} connections to ${VENDOR}...`);
    const query_42 = "SELECT 42";
    if (VENDOR === "firebolt") {
      await getFireboltConnection(-1);
      const statement = await connections.get(-1).execute(query_42);
      const { data } = await statement.fetchResult();
      for (let i = 1; i <= numServerConnections; i++) {
        await getFireboltConnection(i);
      }
    } else if (VENDOR === "snowflake") {
      await getSnowflakeConnection(-1);
      await new Promise((resolve, reject) => {
        connections.get(-1).execute({
          sqlText: query_42,
          complete: (err, stmt, data) => {
            if (err) {
              return reject(err);
            }
            resolve(data);
          }
        });
      });
      for (let i = 1; i <= numServerConnections; i++) {
        await getSnowflakeConnection(i);
      }
    } else if (VENDOR === "redshift") {
      await getRedshiftConnection(-1);
      const result = await connections.get(-1).query(query_42);
      for (let i = 1; i <= numServerConnections; i++) {
        await getRedshiftConnection(i);
      }
    } else {
      console.error("No recognized vendor, skipping pre-init connections.");
      process.exit(1);
    }

    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => {
      console.log(`Server listening on port ${PORT}`);
      console.log(`Vendor: ${VENDOR}, Connections: ${numServerConnections}`);
    });
  } catch (err) {
    console.error("Failed to initialize connections:", err);
    process.exit(1);
  }
})();
