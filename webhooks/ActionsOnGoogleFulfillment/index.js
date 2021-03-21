const {conversation} = require('@assistant/conversation');
const functions = require('firebase-functions');
const teaConsumer = require('./tea_consumer');
const pathProvider = require('./path_provider');


const admin = require('firebase-admin');
admin.initializeApp();
const db = admin.firestore();

const app = conversation();


function currentData() {
  const teaMap = await db.doc(pathProvider.basePath(new Date("2021-03-08T07:45:00Z"))).get();
  
  return teaMap.data()
}

app.handle('tea_consumption', async (conv) => {
  console.log('Start scene: Tea consumption');

  const teaCups = currentData().num_tea_boils;

  conv.add(teaConsumer.toSpeach(teaCups));
});

app.handle('wake_up_time', (conv) => {
  conv.add('Today you have woken up a 11:23 am.');
});

exports.ActionsOnGoogleFulfillment = functions.https.onRequest(app);

