import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import {conversation} from "@assistant/conversation";
import {TeaConsumer} from "./tea_consumer";
import {TimeUtils} from "./time_utils";
import {DayStatsFetcher, FetcherImpl, DayStats} from "./day_stats_fetcher";
import {WholeStoryFactory} from "./whole_story";

const teaConsumer = new TeaConsumer();
const timeUtils = new TimeUtils();


admin.initializeApp();
const firestore = admin.firestore();
const dayFetcher = new DayStatsFetcher(new FetcherImpl(firestore));

const app = conversation();

const currentData = async (): Promise<DayStats> => {
  const today = new Date();
  console.log(`Fetch the day data for ${today.toLocaleDateString}`);

  return dayFetcher.fetch(today);
};

app.handle("tea_consumption", async (conv) => {
  console.log("Start scene: Tea consumption");

  try {
    const teaCups = (await currentData()).teaBoils;

    conv.add(teaConsumer.consume(teaCups));
  } catch (error) {
    console.error(`Unable to return tea consumption. ${error}`);
    conv.append("Unable to return tea consumption.");
  }
});

app.handle("wake_up_time", async (conv) => {
  try {
    const wakeUpTime = (await currentData()).wakeUpTime;
    conv.add(wakeUpTime != undefined ?
      `Today you have woken up at a ${timeUtils.formatLocalTime(wakeUpTime)}.` :
      "We haven't seen you around the house today.");
  } catch (error) {
    console.error(`Unable to return wake up time. ${error}`);
    conv.append("Unable to return wake up time.");
  }
});

app.handle("whole_story", async (conv) => {
  const now = new Date();
  const wholeStory = new WholeStoryFactory().create(conv.user.locale);
  try {
    const speach = wholeStory.say(await dayFetcher.fetch(now));

    conv.append(speach);
  } catch (error) {
    const demoDate = new Date("2021-03-08T07:45:00Z");
    console.error(`Unable to return the whole story. ${error}`);

    conv.append(`Unable to return the whole story for ${now.toUTCString()} UTC. `);
    conv.append("Lets have it for a demo date. ");
    conv.append(wholeStory.say(await dayFetcher.fetch(demoDate)));
  }
});

exports.ActionsOnGoogleFulfillment = functions.https.onRequest(app);


