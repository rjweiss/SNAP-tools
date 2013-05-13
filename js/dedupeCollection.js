db.dedupe.ensureIndex( {title: 1}, { unique: true, dropDups: true  }  )

db.news.find().forEach( function(doc) {
	if (doc.title != '__notitle__')
	{
		db.dedupe.save(doc);
	};
})

