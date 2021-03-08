const {conversation} = require('@assistant/conversation');
const functions = require('firebase-functions');

const admin = require('firebase-admin');
admin.initializeApp();
const db = admin.firestore();

const app = conversation();

app.handle('tea_consumption', async (conv) => {
  console.log('Start scene: Tea consumption');
  const testRef = db.collection('test');

  const teaMap = await testRef.doc('tea').get();
  
  const teaCups = teaMap.data().cups;
  conv.add(`today you have consumed ${teaCups} cups of tea.`);
});

app.handle('wake_up_time', (conv) => {
  conv.add('Today you have woken up a 11:23 am.');
});

exports.ActionsOnGoogleFulfillment = functions.https.onRequest(app);
