function setRandom() {
	db.news.find().forEach(  function(doc) 
		{
			print(doc.file);
			doc.random = Math.random();
			db.news.save(doc);
		}
	);
}

setRandom();
