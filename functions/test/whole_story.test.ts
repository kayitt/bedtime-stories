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

    let speach = wholeStory.report(dayStats);

    expect(speach).to.equal(`Today you have woken up at a 8:45 AM. 
    You have boiled 2 kettles for tea. 
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

    let speach = wholeStory.report(dayStats);

    expect(speach).to.contains(`You have boiled 1 kettle for tea.`);
  });

  it("not woken up yet", function () {
    const dayStats = {
      teaBoils: 1,
      wakeUpTime: undefined,
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

    let speach = wholeStory.report(dayStats);

    expect(speach).to.not.contains(`Today you have woken up at`);
  });
  
  it("no outside min temperature", function () {
    const dayStats = {
      teaBoils: 1,
      wakeUpTime: new Date("2021-03-08T07:45:00Z"),
      temperatureInside: {
        value: 20.0,
        date: new Date(),

      },
      minTemperatureOutside: undefined,
      maxTemperatureOutside: {
        date: new Date("2021-03-08T17:00:00Z"),
        value: 11.0,
      },
    };

    let speach = wholeStory.report(dayStats);

    expect(speach).to.not.contains(`The coldest it has been`);
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

    let speach = wholeStory.report(dayStats);

    expect(speach).to.equal(`Hoy te has levantado a las 8:45 AM. 
    Desde entonces has hecho 2 tazas de té.
    La temperatura actual en casa es de 20 grados centígrados. 
    Lo más frío que ha estado afuera fue de 11 grados a las 7:45 AM
    y lo más cálido fue 11 grados a las 6:00 PM.`
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

    let speach = wholeStory.report(dayStats);

    expect(speach).to.contains(`Desde entonces has hecho 1 taza de té`);
  });

  it("not woken up yet", function () {
    const dayStats = {
      teaBoils: 1,
      wakeUpTime: undefined,
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

    let speach = wholeStory.report(dayStats);

    expect(speach).to.not.contains(`Hoy te has levantado a las`);
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

    let speach = wholeStory.report(dayStats);

    expect(speach).to.equal(`Hoy te has levantado a las 8:45 AM. ¿Por qué dormiste tan poco?
    Desde entonces has hervido 2 termos para el mate.
    La temperatura actual en casa es de 20 grados centígrados. 
    Lo más frío que ha estado afuera fue de 11 grados a las 7:45 AM 
    y lo más cálido fue 11 grados a las 6:00 PM. ¡Qué frío!`
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

    let speach = wholeStory.report(dayStats);

    expect(speach).to.contains(`Desde entonces has hervido 1 termo para el mate`);
  });


  it("not woken up yet", function () {
    const dayStats = {
      teaBoils: 1,
      wakeUpTime: undefined,
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

    let speach = wholeStory.report(dayStats);

    expect(speach).to.not.contains(`Hoy te has levantado a las`);
  });
});
