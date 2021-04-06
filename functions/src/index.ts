import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import {conversation} from "@assistant/conversation";
import {TeaConsumer} from "./tea_consumer";
import {TimeUtils} from "./time_utils";
import {DayStatsFetcher, FetcherImpl, DayStats} from "./day_stats_fetcher";

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

class WholeStory {
  say(stats: DayStats): string {
    const maxTemp = stats.maxTemperatureOutside;
    const minTemp = stats.minTemperatureOutside;

    return `Today you have woken up at a ${timeUtils.formatTime(stats.wakeUpTime)}. 
    Since then you have made ${stats.teaBoils} cups of tea.
    Current temperature at home is ${stats.temperatureInside.value} degrees celsius.
    The coldest it has been outside was ${minTemp.value} degrees at ${timeUtils.formatTime(minTemp.date)} 
    and the warmest ${maxTemp.value} degrees at ${timeUtils.formatTime(maxTemp.date)}.`;
  }
}

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
    conv.add(`Today you have woken up at a ${timeUtils.formatTime(wakeUpTime)}.`);
  } catch (error) {
    console.error(`Unable to return wake up time. ${error}`);
    conv.append("Unable to return wake up time.");
  }
});

app.handle("whole_story", async (conv) => {
  const now = new Date();
  try {
    const speach = new WholeStory().say(await dayFetcher.fetch(now));

    conv.append(speach);
  } catch (error) {
    const demoDate = new Date("2021-03-08T07:45:00Z");
    console.error(`Unable to return the whole story. ${error}`);

    conv.append(`Unable to return the whole story for ${now.toLocaleString()}. `);
    conv.append("Lets have it for a demo date. ");
    conv.append(new WholeStory().say(await await dayFetcher.fetch(demoDate)));
  }
});

exports.ActionsOnGoogleFulfillment = functions.https.onRequest(app);
