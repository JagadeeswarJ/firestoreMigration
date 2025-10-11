const { db } = require("../db");

async function run() {
  const snapshot = await db.collection("users").get();
  //snapshot =>
  // QuerySnapshot → represents the whole collection or query result.
  // QueryDocumentSnapshot → represents a single document in that snapshot.
  snapshot.forEach((doc) => {
    const id = doc.id;
    const data = doc.data();
    console.log("ID: ", id);
    console.log("data: ", data);
  });
  console.log("=".repeat(100));

  //create doc
  const createRes = await db
    .collection("users")
    .doc("qwertyuiop")
    .set({ name: "Jagadeeswar" });
  // in .collection => if the collection is not present it will be created
  // in .doc ->. if not exist ,will be create when u write the data
  console.log(createRes);
  // gives _writeTime
}

run();
