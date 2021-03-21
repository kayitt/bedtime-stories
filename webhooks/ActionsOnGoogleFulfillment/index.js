const {conversation} = require('@assistant/conversation');
const functions = require('firebase-functions');
const teaConsumer = require('./tea_consumer');
const pathProvider = require('./path_provider');
const timeUtils = require('./time_utils');


const admin = require('firebase-admin');
admin.initializeApp();
const db = admin.firestore();

const app = conversation();


async function currentData() {
  const teaMap = await db.doc(pathProvider.basePath(new Date("2021-03-08T07:45:00Z"))).get();
  
  return teaMap.data();
}

app.handle('tea_consumption', async (conv) => {
  console.log('Start scene: Tea consumption');

  const teaCups = (await currentData()).num_tea_boils;

  conv.add(teaConsumer.toSpeach(teaCups));
});

app.handle('wake_up_time', async (conv) => {
  const wakeUpTime = (await currentData()).wake_up_time.toDate();
  conv.add(`Today you have woken up at a ${timeUtils.toSimpleTime(wakeUpTime)}.`);
});

app.handle('whole_story', async (conv) => {
  const allData = await currentData();

  const maxTemp = allData.temperature_outside.max;
  const minTemp = allData.temperature_outside.min;

  conv.add(
  `Today you have woken up at a ${timeUtils.toSimpleTime(allData.wake_up_time.toDate())}. 
  Since then you have made ${allData.num_tea_boils} cups of tea.
  Current temperature at home is ${allData.temperature_inside.current} degrees celsius.
  The coldest it has been outside was ${minTemp.value} degrees at ${timeUtils.toSimpleTime(minTemp.ts.toDate())} 
  and the warmest ${maxTemp.value} degrees at ${timeUtils.toSimpleTime(maxTemp.ts.toDate())}.`
  );
});

exports.ActionsOnGoogleFulfillment = functions.https.onRequest(app);
