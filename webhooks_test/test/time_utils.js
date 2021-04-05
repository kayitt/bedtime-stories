var expect = require("chai").expect;
var timeUtils = require("../../webhooks/ActionsOnGoogleFulfillment/time_utils.js");

describe("time utils", function () {

  it("simple format in the morning", function () {
    let time = timeUtils.toSimpleTime(new Date('2020-01-12T07:45:00'));

    expect(time).to.equal("7:45 AM");
  });


  it("simple format in the afternoon", function () {
    let time = timeUtils.toSimpleTime(new Date('2020-01-12T13:45:00'));

    expect(time).to.equal("1:45 PM");
  });

});


