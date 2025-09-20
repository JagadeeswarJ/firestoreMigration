const { sourceDb, destDb } = require('./db');

async function copyCollection(collectionName) {
  const snapshot = await sourceDb.collection(collectionName).get();

  for (const doc of snapshot.docs) {
    const docData = doc.data();
    await destDb.collection(collectionName).doc(doc.id).set(docData);
    console.log(`Copied doc ${doc.id}`);
  }

  console.log(`Copied ${snapshot.docs.length} documents`);
}

copyCollection('query_results');