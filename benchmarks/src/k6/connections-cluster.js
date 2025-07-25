const cluster = require("cluster");
const fs = require("fs");

if (cluster.isMaster) {
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

  const numberOfThreads = k6Config.number_of_threads;
  console.log(`Master process ${process.pid} is running`);

  for (let i = 0; i < numberOfThreads; i++) {
    cluster.fork();
  }

} else {
  require("./connections-server");
}