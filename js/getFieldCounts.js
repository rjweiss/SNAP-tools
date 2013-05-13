db.dedupe.find().forEach(function(doc) {
	var docstring = doc._id + '\t' + doc.domain;
	print(docstring);
	})

