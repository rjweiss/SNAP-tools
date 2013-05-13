printjson(
db.dedupe.aggregate(
  [
    { $group: { _id : {domain: "$domain", subdomain: "$subdomain", tld: "$tld"} , number : { $sum : 1 } } },
    { $sort: { number : -1 } }
  ]
)
)
