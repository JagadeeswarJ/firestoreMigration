const admin = require('firebase-admin');

// Source project
const sourceApp = admin.initializeApp({
  credential: admin.credential.cert(require('./keys/source-serviceAccountKey.json'))
}, 'source');

// Destination project
const destApp = admin.initializeApp({
  credential: admin.credential.cert(require('./keys/destination-serviceAccountKey.json'))
}, 'dest');

const sourceDb = sourceApp.firestore();
const destDb = destApp.firestore();

module.exports = {
  sourceDb,
  destDb
};