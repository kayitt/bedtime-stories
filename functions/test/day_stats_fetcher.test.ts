var chai = require('chai');
var expect = chai.expect;

var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);

import * as admin from "firebase-admin";
import { DayStatsFetcher, Fetcher, FirestoreDayStats } from "../src/day_stats_fetcher";

describe("day stats fetcher", function () {

  it("fetches stats for a date", async function () {
    let stats: FirestoreDayStats =
    {
      wake_up_time: admin.firestore.Timestamp.fromDate(new Date("2021-03-08T07:45:00Z")),
      num_tea_boils: 1,
      temperature_inside: { current: 1 },
      temperature_outside: { min: { ts: admin.firestore.Timestamp.fromDate(new Date("2021-03-08T07:45:00Z")), value: 20.1 }, max: { ts: admin.firestore.Timestamp.fromDate(new Date("2021-03-08T07:45:00Z")), value: 21.1 } }
    };
    let fetcher = new DayStatsFetcher(new FakeFetcher(stats));

    var result = await fetcher.fetch(new Date());

    expect(result.teaBoils).to.equal(1);
    expect(result.wakeUpTime).deep.equal(new Date("2021-03-08T07:45:00Z"));
    expect(result.temperatureInside.value).to.equal(1);
    expect(result.minTemperatureOutside.value).to.equal(20.1);
    expect(result.minTemperatureOutside.date).deep.equal(new Date("2021-03-08T07:45:00Z"));
    expect(result.maxTemperatureOutside.value).to.equal(21.1);
    expect(result.maxTemperatureOutside.date).deep.equal(new Date("2021-03-08T07:45:00Z"));
  });

  it("throws when date does not exist", async function () {
    const fetcher = new DayStatsFetcher(new FailingFetcher());

    var result = fetcher.fetch(new Date("2021-03-08T07:45:00Z"));

    return expect(result).to.be.rejected;
  });

  it("throws when data is undefined", async function () {
    let stats: FirestoreDayStats =
    {
      wake_up_time: admin.firestore.Timestamp.fromDate(new Date("2021-03-08T07:45:00Z")),
      num_tea_boils: undefined,
      temperature_inside: { current: 1 },
      temperature_outside: { min: { ts: admin.firestore.Timestamp.fromDate(new Date("2021-03-08T07:45:00Z")), value: 20.1 }, max: { ts: admin.firestore.Timestamp.fromDate(new Date("2021-03-08T07:45:00Z")), value: 21.1 } }
    };
    const fetcher = new DayStatsFetcher(new FakeFetcher(stats));

    var result = fetcher.fetch(new Date("2021-03-08T07:45:00Z"));

    return expect(result).to.be.rejected;
  });

});


class FakeFetcher implements Fetcher {

  stats: FirestoreDayStats;

  constructor(stats: FirestoreDayStats) {
    this.stats = stats;
  }

  async fetch(path: string): Promise<FirestoreDayStats> {
    return this.stats;
  }
}

class FailingFetcher implements Fetcher {

  fetch(path: string): Promise<FirestoreDayStats> {
    return Promise.reject(new Error());
  }
}