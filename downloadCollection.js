const { sourceDb } = require('./db');
const fs = require('fs');

const docRef = sourceDb.collection('query_results');

function convert(obj) {
  if (obj && obj._seconds !== undefined && obj._nanoseconds !== undefined) {
    // Firestore Timestamp object
    return new Date(obj._seconds * 1000 + obj._nanoseconds / 1000000).toISOString();
  } else if (obj instanceof Date) {
    return obj.toISOString();
  } else if (obj !== null && typeof obj === 'object') {
    if (Array.isArray(obj)) {
      return obj.map(item => convert(item));
    } else {
      const converted = {};
      for (const [key, value] of Object.entries(obj)) {
        converted[key] = convert(value);
      }
      return converted;
    }
  }
  return obj;
}

docRef.get()
  .then(snapshot => {
    const data = {};
    snapshot.forEach(doc => {
      data[doc.id] = convert(doc.data());
    });

    fs.writeFileSync('query_results.json', JSON.stringify(data, null, 2));
    console.log(`Downloaded ${Object.keys(data).length} documents to query_results.json`);
  })
  .catch(error => {
    console.error('Error downloading collection:', error);
  });