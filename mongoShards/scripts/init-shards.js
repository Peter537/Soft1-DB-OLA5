// init-shards.js

// Connect to mongos (this script is run inside the mongos container)
mongos = new Mongo("localhost:27017");
adminDB = mongos.getDB("admin");
db = mongos.getDB("testDB"); // Target your database

print("Starting shard initialization process...");

// Initiate shard replica sets
// Wait a bit for shard replica sets to potentially elect a primary if they were just started.
// In a production script, you'd have more robust checks.
print("Attempting to connect to shard1 to initiate replica set...");
try {
    sh1 = new Mongo("shard1:27017");
    sh1.getDB("admin").runCommand({
      replSetInitiate: {
        _id: "shardReplSet1",
        members: [{ _id: 0, host: "shard1:27017" }]
      }
    });
    print("shardReplSet1 initiated or already exists.");
} catch (e) {
    print("Error initiating shardReplSet1 (or already initiated): " + e);
}

print("Attempting to connect to shard2 to initiate replica set...");
try {
    sh2 = new Mongo("shard2:27017");
    sh2.getDB("admin").runCommand({
      replSetInitiate: {
        _id: "shardReplSet2",
        members: [{ _id: 0, host: "shard2:27017" }]
      }
    });
    print("shardReplSet2 initiated or already exists.");
} catch (e) {
    print("Error initiating shardReplSet2 (or already initiated): " + e);
}

// It might take a moment for replica sets to be fully ready.
// In a real script, you'd poll for replica set status.
print("Pausing for 5 seconds for replica sets to stabilize...");
sleep(5000); // 10 seconds

// Add shards to the cluster
print("Adding shardReplSet1...");
try {
    printjson(adminDB.runCommand({ addShard: "shardReplSet1/shard1:27017" }));
} catch (e) {
    print("Error adding shardReplSet1 (or already added): " + e);
}

print("Adding shardReplSet2...");
try {
    printjson(adminDB.runCommand({ addShard: "shardReplSet2/shard2:27017" }));
} catch (e) {
    print("Error adding shardReplSet2 (or already added): " + e);
}

print("Listing shards:");
printjson(adminDB.runCommand({ listShards: 1 }));

// Enable sharding for the database 'testDB'
print("Enabling sharding for database 'testDB'...");
try {
    printjson(adminDB.runCommand({ enableSharding: "testDB" }));
} catch (e) {
    print("Error enabling sharding for testDB (or already enabled): " + e);
}

// Create a hashed index on _id for the 'tweets' collection in 'testDB'
// This should be done BEFORE sharding the collection on this key.
print("Creating hashed index on _id for 'testDB.tweets'...");
try {
    printjson(db.tweets.createIndex({ _id: "hashed" }));
} catch (e) {
    print("Error creating index on testDB.tweets (or index already exists): " + e);
}

// Shard the 'tweets' collection in 'testDB' using the _id field (hashed)
print("Sharding collection 'testDB.tweets' on _id (hashed)...");
try {
    printjson(adminDB.runCommand({
      shardCollection: "testDB.tweets",
      key: { _id: "hashed" }
    }));
} catch (e) {
    print("Error sharding collection testDB.tweets (or already sharded): " + e);
}

print("Shard initialization process completed.");
print("Current sharding status for testDB.tweets:");
printjson(db.tweets.stats());