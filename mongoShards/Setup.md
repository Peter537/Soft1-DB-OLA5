# ⚙️ Automated MongoDB Sharded Cluster Setup (Using Container Names)

I had wanted to set up a python script for this but its much easier to just do this through 3 commands.
Docker compose 
and to docker exec commands that sets up and populates our shards

lastly you can do some manual queries that i noted at the bottom which shows you if the structure is sharded or not and also shows that the data persists and gets sharded.

---

## 🧰 The setup

- Docker and Docker Compose containrizes everything so its clean and easy
- Cluster runs via `docker compose up -d`
- The `docker-compose.yml` in this folder already defines:
  - 3 Config Servers
  - 2 Shards
  - 1 Mongos router
- scripts folder:
  - init-configsvr.js
  - init-shards.js

## 📁 THe init functions

The init functions inside the [scripts](./scripts/) folder are used to automate the shard creation and usage

They will be used in the later steps to populate the created shard volumes with the names defined in the compose file and also set up the mongos router which handles all quries and chooses which shards to devide data to/from.

## 🧠 All you have to do is run these commands:
Of course we start with docker compose function. Make sure you are in the [`mongoShards folder.`](../mongoShards/) 
```
docker compose up -d
```


```powershell
Get-Content .\scripts\init-configsvr.js | docker exec -i mongo-sharded-cluster-configsvr1-1 mongosh
```
- The above script will executes the `init-configsvr.js` script inside the `mongo-sharded-cluster-configsvr1-1` container. The configs are predefined with a structure in the compose file that allows them to be routed easily by mongos router.

## Wait 10-20 seconds otherwise it will fail

```powershell
Get-Content .\scripts\init-shards.js | docker exec -i mongo-sharded-cluster-mongos-1 mongosh
```

- This script executes the `init-shards.js` script inside the `mongos` container which sets up the most crucial part, the mongos router which will handle all quries and funnel them to/from and between the shards.

And its done. Nowe can test the cluster.

---

## 💡 Testing the Sharded Cluster

After the setup is complete, you can test the sharded cluster by connecting to the `mongos` container and performing operations like inserting data into the `testDB.testColl`. With the names in the compose file, which should be **mongo-sharded-cluster-mongos-1**

## Keep in mind docker consoles dont allow ctrl+v and instead use rightclick to paste into terminal. *At least for me..*

```powershell
docker exec -it mongo-sharded-cluster-mongos-1 mongosh
```

Once connected, you can run MongoDB commands to interact with your database and test sharding. For example:

```js
use testDB;
db.testColl.insert({ _id: 1, name: "test" });
```
- This inserts a document with an `_id` of `1` and a `name` field set to `"test"` into the `testColl` collection within the `testDB` database.

```js
db.testColl.stats();
```
- This retrieves and displays statistics about the `testColl` collection, such as the number of documents, storage size, and other metadata. It also shows if the instance is sharded or not.

---

### Final remarks
We have now created shards, and used our mongos instance to funnel the queries between/into different shards which allows bigger entities and loads to be seperated into smaller pieces, all managed by mongos.

