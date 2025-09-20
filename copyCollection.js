const { sourceDb, destDb } = require('./db');

async function copyCollection(collectionName, destCollectionName = collectionName) {
  const snapshot = await sourceDb.collection(collectionName).get();
  const docs = snapshot.docs;
  const batchSize = 500;

  console.log(`Starting migration of ${docs.length} documents from ${collectionName} to ${destCollectionName}`);

  for (let i = 0; i < docs.length; i += batchSize) {
    const batch = destDb.batch();
    const batchDocs = docs.slice(i, i + batchSize);

    for (const doc of batchDocs) {
      const docData = doc.data();
      const destDocRef = destDb.collection(destCollectionName).doc(doc.id);
      batch.set(destDocRef, docData);
    }

    try {
      await batch.commit();
      console.log(`Batch ${Math.floor(i / batchSize) + 1}: Copied ${batchDocs.length} documents`);
    } catch (error) {
      console.error(`Error in batch ${Math.floor(i / batchSize) + 1}:`, error);
      throw error;
    }
  }

  console.log(`Successfully copied ${docs.length} documents from ${collectionName} to ${destCollectionName}`);
}

// copyCollection('admins');
// copyCollection('general');
copyCollection('participants','cloudcraft-2025');
copyCollection('technovista','technovista-2025');