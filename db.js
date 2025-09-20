const admin = require('firebase-admin');

const sourceCred = require('./keys/source-serviceAccountKey.json');
const destinationCred = require('./keys/destination-serviceAccountKey.json');

const sourceApp = admin.initializeApp({
  credential: admin.credential.cert(sourceCred)
}, 'source');

const destinationApp = admin.initializeApp({
  credential: admin.credential.cert(destinationCred)
}, 'destination');

const sourceDb = admin.firestore(sourceApp);
const destinationDb = admin.firestore(destinationApp);

module.exports = {
  sourceDb,
  destinationDb
};