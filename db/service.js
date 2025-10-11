const { db } = require("./index");

class FirestoreService {
  constructor(db) {
    this.db = db;
  }

  async getAll(collectionName) {
    const snapshot = await this.db.collection(collectionName).get();
    return snapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
  }
  //snapshot =>
  // QuerySnapshot → represents the whole collection or query result.
  // QueryDocumentSnapshot → represents a single document in that snapshot.

  async createOrUpdate(collectionName, docId, data) {
    const createRes = await this.db
      .collection(collectionName)
      .doc(docId)
      .set(data);
    console.log(createRes);
    // gives _writeTime
    return { id: docId, ...data };
  }
  // in .collection => if the collection is not present it will be created
  // in .doc ->. if not exist ,will be create when u write the data
}

module.exports = new FirestoreService(db);
