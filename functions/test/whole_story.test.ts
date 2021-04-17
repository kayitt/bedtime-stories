var expect = require("chai").expect;
import { WholeStoryFactory } from "../src/whole_story";

describe("english whole story", function () {

  const wholeStory = new WholeStoryFactory().create('en-EN');

  it("the entire trimmed story", function () {
    const dayStats = {
      teaBoils: 2,
      wakeUpTime: new Date("2021-03-08T07:45:00Z"),
      temperatureInside: {
        value: 20.0,
        date: new Date(),

      },
      minTemperatureOutside: {
        date: new Date("2021-03-08T06:45:00Z"),
        value: 11.0,
      },
      maxTemperatureOutside: {
        date: new Date("2021-03-08T17:00:00Z"),
        value: 11.0,
      },
    };

    let speach = wholeStory.say(dayStats);

    expect(speach).to.equal(`Today you have woken up at a 8:45 AM. 
    Since then you have made 2 cups of tea. 
    Current temperature at home is 20 degrees celsius. 
    The coldest it has been outside was 11 degrees at 7:45 AM 
    and the warmest 11 degrees at 6:00 PM.`.replace(/\s+/g, ' '));
  });

  it("singular tee cups", function () {
    const dayStats = {
      teaBoils: 1,
      wakeUpTime: new Date("2021-03-08T07:45:00Z"),
      temperatureInside: {
        value: 20.0,
        date: new Date(),

      },
      minTemperatureOutside: {
        date: new Date("2021-03-08T06:45:00Z"),
        value: 11.0,
      },
      maxTemperatureOutside: {
        date: new Date("2021-03-08T17:00:00Z"),
        value: 11.0,
      },
    };

    let speach = wholeStory.say(dayStats);

    expect(speach).to.contains(`Since then you have made 1 cup of tea.`);
  });
});

describe("spanish from spain whole story", function () {

  const wholeStory = new WholeStoryFactory().create('es-EN');

  it("the entire trimmed story", function () {
    const dayStats = {
      teaBoils: 2,
      wakeUpTime: new Date("2021-03-08T07:45:00Z"),
      temperatureInside: {
        value: 20.0,
        date: new Date(),

      },
      minTemperatureOutside: {
        date: new Date("2021-03-08T06:45:00Z"),
        value: 11.0,
      },
      maxTemperatureOutside: {
        date: new Date("2021-03-08T17:00:00Z"),
        value: 11.0,
      },
    };

    let speach = wholeStory.say(dayStats);

    expect(speach).to.equal(`Hoy te has levantado a las 8:45 AM. 
    Desde entonces has hecho 2 tazas de té. 
    La temperatura actual en casa es de 20 grados centígrados. 
    Lo más frío que ha estado afuera fue de 11 grados a las 7:45 AM
    y el más cálido de 11 grados a las 6:00 PM.`
      .replace(/\s+/g, ' '));
  });

  it("singular tee cups", function () {
    const dayStats = {
      teaBoils: 1,
      wakeUpTime: new Date("2021-03-08T07:45:00Z"),
      temperatureInside: {
        value: 20.0,
        date: new Date(),

      },
      minTemperatureOutside: {
        date: new Date("2021-03-08T06:45:00Z"),
        value: 11.0,
      },
      maxTemperatureOutside: {
        date: new Date("2021-03-08T17:00:00Z"),
        value: 11.0,
      },
    };

    let speach = wholeStory.say(dayStats);

    expect(speach).to.contains(`Desde entonces has hecho 1 taza de té`);
  });
});

describe("spanish from latin america whole story", function () {

  const wholeStory = new WholeStoryFactory().create('es-419');

  it("the entire trimmed story", function () {
    const dayStats = {
      teaBoils: 2,
      wakeUpTime: new Date("2021-03-08T07:45:00Z"),
      temperatureInside: {
        value: 20.0,
        date: new Date(),

      },
      minTemperatureOutside: {
        date: new Date("2021-03-08T06:45:00Z"),
        value: 11.0,
      },
      maxTemperatureOutside: {
        date: new Date("2021-03-08T17:00:00Z"),
        value: 11.0,
      },
    };

    let speach = wholeStory.say(dayStats);

    expect(speach).to.equal(`Hoy te has levantado a las 8:45 AM. ¿Por qué dormiste tan poco? 
    Desde entonces has hecho 2 tazas de Yerba mate. 
    La temperatura actual en casa es de 20 grados centígrados. 
    Lo más frío que ha estado afuera fue de 11 grados a las 7:45 AM 
    y el más cálido de 11 grados a las 6:00 PM. ¡Qué frío!`
      .replace(/\s+/g, ' '));
  });

  it("singular tee cups", function () {
    const dayStats = {
      teaBoils: 1,
      wakeUpTime: new Date("2021-03-08T07:45:00Z"),
      temperatureInside: {
        value: 20.0,
        date: new Date(),

      },
      minTemperatureOutside: {
        date: new Date("2021-03-08T06:45:00Z"),
        value: 11.0,
      },
      maxTemperatureOutside: {
        date: new Date("2021-03-08T17:00:00Z"),
        value: 11.0,
      },
    };

    let speach = wholeStory.say(dayStats);

    expect(speach).to.contains(`Desde entonces has hecho 1 taza de Yerba mate`);
  });
});

