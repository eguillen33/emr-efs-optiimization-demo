# EMR + EFS Optimization Demo

This project demonstrates how to reduce EMR cluster bootstrap time by caching dependencies on Amazon EFS.

## 💡 Problem
Fetching dependencies on every EMR run causes delays and increased costs.

## 🚀 Solution
On the first run, we store dependencies in EFS. On future runs, the EMR cluster mounts EFS and skips the download process.

## 🔁 Toggle Setup
```json
// toggle/config.json
{
  "use_efs": true
}
```

## Expectation
Method | Bootstrap Time
Remote Fetch | ~30 seconds
EFS Cache | ~5 seconds
