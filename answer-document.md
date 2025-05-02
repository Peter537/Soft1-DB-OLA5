## Questions

### a) What is sharding in mongoDB?

Sharding is a way to make horizontal scaling, which means we distribute data across multiple servers. This way, we can handle more data and more requests without slowing down the system. Sharding is useful when a single server cannot handle the amount of data or traffic we have.

### b) What are the different components required to implement sharding?

- Config servers: These stores the cluster's metadata (ex. mapping of data ranges to shards) and config settings. They are deployed as a replica set because they are essential for the cluster's operation.

- Mongos: This is the query router. It is the interface between the client application and the sharded cluster. It routes queries to the appropriate shard(s) based on the metadata stored in the config servers.

- Shards: These are where the data is stored. Each shard is a replica set, which means it has multiple copies of the data for redundancy and high availability.

### c) Explain architecture of sharding in mongoDB?

Data is being divided into chunks based on a shard-key, where each is being stored on a shard. The config servers store the metadata about the chunks and their locations. The mongos acts as a query router, directing queries to the appropriate shard based on the metadata.

### d) Provide implementation of map and reduce function

**Map Function:**

The $project stage is used to create a new field called hashtags, which contains an array of objects. Each object has a key (the hashtag) and a value (1). The $map operator is used to iterate over the array of words in the text field, and the $filter operator is used to select only those words that start with a #.

The $unwind stage is used to deconstruct the hashtags array, creating a separate document for each hashtag.

Lastly, the $out stage is used to write the results to a new collection called temp_hashtags.

```js
db.tweets.aggregate([
  {
    $project: {
      _id: 0,
      hashtags: {
        $map: {
          input: {
            $filter: {
              input: { $split: ["$text", " "] },
              cond: { $regexMatch: { input: "$$this", regex: /^#/ } }
            }
          },
          as: "hashtag",
          in: { key: { $toLower: "$$hashtag" }, value: 1 }
        }
      }
    }
  },
  { $unwind: "$hashtags" },
  { $out: "temp_hashtags" }
]);
```

**Reduce Function:**

The $group stage is used to group the documents by the hashtag key and sum the values.

The $sort stage is used to sort the results in descending order (-1) based on the count.

Lastly, the $limit stage is used to limit the results to the top 10 hashtags.

```js
db.temp_hashtags.aggregate([
  {
    $group: {
      _id: "$hashtags.key",
      count: { $sum: "$hashtags.value" }
    }
  },
  { $sort: { count: -1 } },
  { $limit: 10 }
]);
```

### e) Provide execution command for running MapReduce or the aggregate way of doing the same

First, run the map function created above, and after that, run the reduce function.

### f) Provide top 10 recorded out of the sorted result. (hint: use sort on the result returned by MapReduce or the aggregate way of doing the same)

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
  _id: '#lfc',
  count: 17
},
{
  _id: '#javascript',
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

## Optional Questions

### g) Show what happens to the data when one shard is turned off.

### h) Show what happens to the data when the shard rejoins.

### i) Explain how you could introduce redundancy to the setup above.
