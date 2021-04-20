import {DayStats, TemperaturePoint} from "./day_stats_fetcher";
import {TimeUtils} from "./time_utils";

const timeUtils = new TimeUtils();

export class WholeStoryFactory {
  create(locale: string): WholeStory {
    if (locale.startsWith("es-419")) {
      return new WholeStorySpanishLatin();
    } else if (locale.startsWith("es-")) {
      return new WholeStorySpanish();
    } else {
      return new WholeStoryEnglish();
    }
  }
}

export abstract class WholeStory {
  report(stats: DayStats): string {
    return this.doReport(stats).replace(/\s+/g, " ").trim();
  }

  doReport(stats: DayStats): string {
    const wakeUp = stats.wakeUpTime == undefined ?
      "" :
      this.reportWakeUpTime(stats.wakeUpTime);

    const temperatureOutside = stats.minTemperatureOutside != undefined && stats.maxTemperatureOutside != undefined ?
      this.reportTemperatureOutside(stats.minTemperatureOutside, stats.maxTemperatureOutside) :
      "";

    const temperatureInside = stats.temperatureInside != undefined ?
      this.reportTemperatureInside(stats.temperatureInside) :
      "";

    return `
        ${wakeUp} 
        ${this.reportKettleBoils(stats.teaBoils ?? 0)}
        ${temperatureInside}
        ${temperatureOutside}`;
  }

  abstract reportTemperatureInside(tp: TemperaturePoint): string;

  abstract reportTemperatureOutside(minTp: TemperaturePoint, maxTp: TemperaturePoint): string;

  abstract reportWakeUpTime(wakeUpTime: Date): string;

  abstract reportKettleBoils(boilCount: number): string;
}

class WholeStorySpanish extends WholeStory {
  reportTemperatureInside(tp: TemperaturePoint): string {
    return `La temperatura actual en casa es de ${tp.value} grados centígrados. `;
  }

  reportTemperatureOutside(minTp: TemperaturePoint, maxTp: TemperaturePoint): string {
    return `Lo más frío que ha estado afuera fue de ${minTp.value} grados
    a las ${timeUtils.formatLocalTime(minTp.date)} 
    y lo más cálido fue ${maxTp.value} grados a las ${timeUtils.formatLocalTime(maxTp.date)}. `;
  }

  reportWakeUpTime(wakeUpTime: Date): string {
    return `Hoy te has levantado a las ${timeUtils.formatLocalTime(wakeUpTime)}. `;
  }

  reportKettleBoils(boilCount: number): string {
    return boilCount == 1 ?
      `Desde entonces has hecho ${boilCount} taza de té. ` :
      `Desde entonces has hecho ${boilCount} tazas de té. `;
  }
}

class WholeStorySpanishLatin extends WholeStory {
  reportTemperatureInside(tp: TemperaturePoint): string {
    return `La temperatura actual en casa es de ${tp.value} grados centígrados. `;
  }

  reportTemperatureOutside(minTp: TemperaturePoint, maxTp: TemperaturePoint): string {
    return `Lo más frío que ha estado afuera fue de ${minTp.value} grados
    a las ${timeUtils.formatLocalTime(minTp.date)} 
    y lo más cálido fue ${maxTp.value} grados a las ${timeUtils.formatLocalTime(maxTp.date)}. ¡Qué frío!`;
  }

  reportWakeUpTime(wakeUpTime: Date): string {
    return `Hoy te has levantado a las ${timeUtils.formatLocalTime(wakeUpTime)}. ¿Por qué dormiste tan poco? `;
  }

  reportKettleBoils(boilCount: number): string {
    return boilCount == 1 ?
      `Desde entonces has hervido ${boilCount} termo para el mate. ` :
      `Desde entonces has hervido ${boilCount} termos para el mate. `;
  }
}

class WholeStoryEnglish extends WholeStory {
  reportTemperatureInside(tp: TemperaturePoint): string {
    return `Current temperature at home is ${tp.value} degrees celsius. `;
  }

  reportTemperatureOutside(minTp: TemperaturePoint, maxTp: TemperaturePoint): string {
    return `The coldest it has been outside was ${minTp.value} degrees at ${timeUtils.formatLocalTime(minTp.date)}
    and the warmest ${maxTp.value} degrees at ${timeUtils.formatLocalTime(maxTp.date)}. `;
  }

  reportWakeUpTime(wakeUpTime: Date): string {
    return `Today you have woken up at a ${timeUtils.formatLocalTime(wakeUpTime)}. `;
  }

  reportKettleBoils(boilCount: number): string {
    return boilCount == 1 ?
      `You have boiled ${boilCount} kettle for tea. ` :
      `You have boiled ${boilCount} kettles for tea. `;
  }
}
