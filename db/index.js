const admin = require("firebase-admin");
const serviceAccountJson = require("../keys/infra.json");

const app = admin.initializeApp(
  {
    credential: admin.credential.cert(serviceAccountJson),
  },
  "test"
);

const db = app.firestore();

module.exports = { db };
