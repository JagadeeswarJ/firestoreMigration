const admin = require('firebase-admin');

// Source project
const sourceApp = admin.initializeApp({
  credential: admin.credential.cert(require('./keys/kv-db.json'))
}, 'source');

// Destination project
const destApp = admin.initializeApp({
  credential: admin.credential.cert(require('./keys/vjdq-prod.json'))
}, 'dest');

const sourceDb = sourceApp.firestore();
const destDb = destApp.firestore();

module.exports = {
  sourceDb,
  destDb
};