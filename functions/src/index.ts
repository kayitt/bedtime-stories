import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import {conversation} from "@assistant/conversation";
import {DayStatsFetcher, FetcherImpl} from "./day_stats_fetcher";
import {WholeStoryFactory} from "./whole_story";


admin.initializeApp();
const firestore = admin.firestore();
const dayFetcher = new DayStatsFetcher(new FetcherImpl(firestore));

const app = conversation();

app.handle("whole_story", async (conv) => {
  const now = new Date();
  const wholeStory = new WholeStoryFactory().create(conv.user.locale);
  try {
    const speach = wholeStory.report(await dayFetcher.fetch(now));

    conv.append(speach);
  } catch (error) {
    const demoDate = new Date("2021-03-08T07:45:00Z");
    console.error(`Unable to return the whole story. ${error}`);

    conv.append(`Unable to return the whole story for ${now.toUTCString()} UTC. `);
    conv.append("Lets have it for a demo date. ");
    conv.append(wholeStory.report(await dayFetcher.fetch(demoDate)));
  }
});

app.handle("whole_story_en", async (conv) => {
  const now = new Date();
  const wholeStory = new WholeStoryFactory().create("en_US");
  try {
    const speach = wholeStory.report(await dayFetcher.fetch(now));

    conv.append(speach);
  } catch (error) {
    const demoDate = new Date("2021-03-08T07:45:00Z");
    console.error(`Unable to return the whole story. ${error}`);

    conv.append(`Unable to return the whole story for ${now.toUTCString()} UTC. `);
    conv.append("Lets have it for a demo date. ");
    conv.append(wholeStory.report(await dayFetcher.fetch(demoDate)));
  }
});


exports.ActionsOnGoogleFulfillment = functions.https.onRequest(app);


