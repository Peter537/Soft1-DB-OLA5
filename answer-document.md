## Questions

### 1. "What are the top 10 hashtags used in the given tweets?"

To figure out which are the top 10 hashtags used in the dataset, we will use aggregation in MongoDB.

We will first filter the words in the text field to get only the hashtags. Then we will unwind the array of hashtags to create a separate document for each hashtag. After that, we will group by the hashtag and count the occurrences. Finally, we will sort the results in descending order and limit it to 10.

```mongo
db.tweets.aggregate([
  {
    $project: {
      hashtags: {
        $filter: {
          input: { $split: [ "$text", " " ] },
          as: "word",
          cond: { $regexMatch: { input: "$$word", regex: /^#/ } }
        }
      }
    }
  },
  { $unwind: "$hashtags" },
  {
    $group: {
      _id: { $toLower: "$hashtags" },
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } },
  { $limit: 10 }
])
```

This will give us the top 10 hashtags used in the tweets along with their counts.

The top 10 hashtags from the dataset are:

```json
{
  _id: '#angularjs',
  count: 29
},
{
  _id: '#nodejs',
  count: 28
},
{
  _id: '#fcblive',
  count: 27
},
{
  _id: '#espanyolfcb',
  count: 18
},
{
  _id: '#webinar',
  count: 18
},
{
  _id: '#javascript',
  count: 17
},
{
  _id: '#lfc',
  count: 17
},
{
  _id: '#cfclive',
  count: 16
},
{
  _id: '#cfc',
  count: 15
},
{
  _id: '#redbizuk',
  count: 15
}
```

### a) What is sharding in mongoDB?

Sharding is a way to make horizontal scaling, which means we distribute data across multiple servers. This way, we can handle more data and more requests without slowing down the system. Sharding is useful when a single server cannot handle the amount of data or traffic we have.

### b) What are the different components required to implement sharding?

- Config servers: These stores the cluster's metadata (ex. mapping of data ranges to shards) and config settings. They are deployed as a replica set because they are essential for the cluster's operation.

- Mongos: This is the query router. It is the interface between the client application and the sharded cluster. It routes queries to the appropriate shard(s) based on the metadata stored in the config servers.

- Shards: These are where the data is stored. Each shard is a replica set, which means it has multiple copies of the data for redundancy and high availability.

### c) Explain architecture of sharding in mongoDB?

Data is being divided into chunks based on a shard-key, where each is being stored on a shard. The config servers store the metadata about the chunks and their locations. The mongos acts as a query router, directing queries to the appropriate shard based on the metadata.

### d) Provide implementation of map and reduce function

### e) Provide execution command for running MapReduce or the aggregate way of doing the same

### f) Provide top 10 recorded out of the sorted result. (hint: use sort on the result returned by MapReduce or the aggregate way of doing the same)

## Optional Questions

### g) Show what happens to the data when one shard is turned off.

### h) Show what happens to the data when the shard rejoins.

### i) Explain how you could introduce redundancy to the setup above.
