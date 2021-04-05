import * as functions from "firebase-functions";
import {conversation} from "@assistant/conversation";
import {TeaConsumer} from "./tea_consumer";
import {PathProvider} from "./path_provider";
import {TimeUtils} from "./time_utils";

// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript

const teaConsumer = new TeaConsumer();
const pathProvider = new PathProvider();
const timeUtils = new TimeUtils();

import * as admin from "firebase-admin";
admin.initializeApp();
const db = admin.firestore();

const app = conversation();


const currentData = async (): Promise<any> => {
  const teaMap = await db.doc(pathProvider.basePath(new Date("2021-03-08T07:45:00Z"))).get();

  return teaMap.data();
};


app.handle("tea_consumption", async (conv) => {
  console.log("Start scene: Tea consumption");

  const teaCups = (await currentData()).num_tea_boils;

  conv.add(teaConsumer.consume(teaCups));
});

app.handle("wake_up_time", async (conv) => {
  const wakeUpTime = (await currentData()).wake_up_time.toDate();
  conv.add(`Today you have woken up at a ${timeUtils.formatDate(wakeUpTime)}.`);
});

app.handle("whole_story", async (conv) => {
  const allData = await currentData();

  const maxTemp = allData.temperature_outside.max;
  const minTemp = allData.temperature_outside.min;

  conv.add(
      `Today you have woken up at a ${timeUtils.formatDate(allData.wake_up_time.toDate())}. 
  Since then you have made ${allData.num_tea_boils} cups of tea.
  Current temperature at home is ${allData.temperature_inside.current} degrees celsius.
  The coldest it has been outside was ${minTemp.value} degrees at ${timeUtils.formatDate(minTemp.ts.toDate())} 
  and the warmest ${maxTemp.value} degrees at ${timeUtils.formatDate(maxTemp.ts.toDate())}.`
  );
});

exports.ActionsOnGoogleFulfillment = functions.https.onRequest(app);
