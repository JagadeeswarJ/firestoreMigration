const { destinationDb } = require('./db');
const fs = require('fs');

const collectionName = 'query_res_backup';

function restore(obj) {
  if (typeof obj === 'string') {
    try {
      // Check if it's an ISO date string
      const date = new Date(obj);
      if (!isNaN(date.getTime()) && obj.includes('T') && (obj.includes('Z') || obj.includes('+'))) {
        return date;
      }
      return obj;
    } catch {
      return obj;
    }
  } else if (obj !== null && typeof obj === 'object') {
    if (Array.isArray(obj)) {
      return obj.map(item => restore(item));
    } else {
      const restored = {};
      for (const [key, value] of Object.entries(obj)) {
        restored[key] = restore(value);
      }
      return restored;
    }
  }
  return obj;
}

const data = JSON.parse(fs.readFileSync('query_results.json', 'utf8'));

const batch = destinationDb.batch();
let batchCount = 0;
const promises = [];

for (const [docId, docData] of Object.entries(data)) {
  console.log(`Uploading doc ${docId}`);
  const restoredData = restore(docData);
  const docRef = destinationDb.collection(collectionName).doc(docId);
  batch.set(docRef, restoredData);
  batchCount++;

  if (batchCount >= 500) {
    promises.push(batch.commit());
    batchCount = 0;
  }
}

if (batchCount > 0) {
  promises.push(batch.commit());
}

Promise.all(promises)
  .then(() => {
    console.log(`Uploaded ${Object.keys(data).length} documents to collection '${collectionName}'`);
  })
  .catch(error => {
    console.error('Error uploading documents:', error);
  });