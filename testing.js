const { sourceDb } = require('./db');

const docRef = sourceDb.collection('query_results');

docRef.get()
  .then(snapshot => {
    snapshot.forEach(doc => {
      console.log(doc);
    });
  })
  .catch(error => {
    console.error('Error getting documents:', error);
  });