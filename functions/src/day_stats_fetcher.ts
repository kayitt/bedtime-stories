import * as admin from "firebase-admin";
import {PathProvider} from "./path_provider";

export class DayStatsFetcher {
  fetcher: Fetcher;
  pathProvider = new PathProvider();

  constructor(fetcher: Fetcher) {
    this.fetcher = fetcher;
  }

  async fetch(date: Date): Promise<DayStats> {
    const stats = await this.fetcher.fetch(this.pathProvider.basePath(date));

    if (stats.num_tea_boils == undefined ||
      stats.wake_up_time == undefined ||
      stats.temperature_inside == undefined ||
      stats.temperature_outside == undefined) {
      throw Error(`Returned values for ${date.toLocaleDateString} are undefined`);
    }

    return {
      teaBoils: stats.num_tea_boils,
      wakeUpTime: stats.wake_up_time.toDate(),
      temperatureInside: {
        value: stats.temperature_inside.current,
        date: new Date(),

      },
      minTemperatureOutside: {
        date: stats.temperature_outside.min.ts.toDate(),
        value: stats.temperature_outside.min.value,
      },
      maxTemperatureOutside: {
        date: stats.temperature_outside.max.ts.toDate(),
        value: stats.temperature_outside.max.value,
      },
    } as DayStats;
  }
}

export interface DayStats {
  wakeUpTime: Date;
  teaBoils: number;
  temperatureInside: TemperaturePoint,
  minTemperatureOutside: TemperaturePoint,
  maxTemperatureOutside: TemperaturePoint,
}

interface TemperaturePoint {
  date: Date;
  value: number;
}

interface FirestoreTemperatureScalar {
  current: number;
}

interface FirestoreTemperaturePoint {
  ts: admin.firestore.Timestamp;
  value: number;
}

interface FirestoreTemperatureRange {
  min: FirestoreTemperaturePoint;
  max: FirestoreTemperaturePoint;
}

export interface FirestoreDayStats {
  temperature_outside: FirestoreTemperatureRange;
  temperature_inside: FirestoreTemperatureScalar;
  wake_up_time: admin.firestore.Timestamp;
  num_tea_boils: number | undefined;
}

export class FetcherImpl implements Fetcher {
  firestore: admin.firestore.Firestore;

  constructor(firestore: admin.firestore.Firestore) {
    this.firestore = firestore;
  }

  async fetch(path: string): Promise<FirestoreDayStats> {
    const map = await this.firestore.doc(path).get();

    return map.data() as FirestoreDayStats;
  }
}

export interface Fetcher {

  fetch(path: string): Promise<FirestoreDayStats>;
}
