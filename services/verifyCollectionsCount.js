const { sourceDb, destDb } = require('../db');

async function verifyCollections() {
  const sourceCollectionName = "participants"
  const sourceSnapshot = await sourceDb.collection(sourceCollectionName).get();
  const sourceDocs = sourceSnapshot.docs;
  console.log("count in source: ", sourceDocs.length)
  
  const destCollectionName = "cloudcraft-2025"
  const destSnapshot = await destDb.collection(destCollectionName).get();
  const destDocs = destSnapshot.docs;
  console.log("count in dest: ", destDocs.length)
}

verifyCollections().catch(console.error);
