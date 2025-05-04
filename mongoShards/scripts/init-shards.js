// Initiate shard replica sets
sh1 = new Mongo("shard1:27017");
sh1.getDB("admin").runCommand({
  replSetInitiate: {
    _id: "shardReplSet1",
    members: [{ _id: 0, host: "shard1:27017" }]
  }
});

sh2 = new Mongo("shard2:27017");
sh2.getDB("admin").runCommand({
  replSetInitiate: {
    _id: "shardReplSet2",
    members: [{ _id: 0, host: "shard2:27017" }]
  }
});

// Add shards and enable sharding
mongos = new Mongo("localhost:27017");
mongos.getDB("admin").runCommand({ addShard: "shardReplSet1/shard1:27017" });
mongos.getDB("admin").runCommand({ addShard: "shardReplSet2/shard2:27017" });

mongos.getDB("admin").runCommand({ enableSharding: "testDB" });
mongos.getDB("admin").runCommand({
  shardCollection: "testDB.testColl",
  key: { _id: "hashed" }
});
