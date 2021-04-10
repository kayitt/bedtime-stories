import {expect} from "chai";
import {TimeUtils} from "../src/time_utils";

const timeUtils = new TimeUtils();

describe("utc time", function () {

  it("simple format in the morning", function () {
    let time = timeUtils.formatUtcTime(new Date('2020-01-12T07:45:00Z'));

    expect(time).to.equal("7:45 AM");
  });


  it("simple format in the afternoon", function () {
    let time = timeUtils.formatUtcTime(new Date('2020-01-12T13:45:00Z'));

    expect(time).to.equal("1:45 PM");
  });


  it("when date is marked UTC it shows the proper time", function () {
    let time = timeUtils.formatUtcTime(new Date('2020-01-12T13:45:00Z'));

    expect(time).to.equal("1:45 PM");
  });

});

describe("local time", function () {

  it("simple format in the morning", function () {
    let time = timeUtils.formatLocalTime(new Date('2020-04-10T07:45:00Z'));

    expect(time).to.equal("9:45 AM");
  });

});


