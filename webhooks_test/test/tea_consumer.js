var expect = require("chai").expect;
var consumer = require("../../webhooks/ActionsOnGoogleFulfillment/tea_consumer");

describe("tea comsumer", function () {

  it("consumes plural number of tea", function () {
    let speach = consumer.toSpeach(4);

    expect(speach).to.equal("You have conumed 4 cups of tea.");
  });

  it("consumes no tea", function () {
    let speach = consumer.toSpeach(0);

    expect(speach).to.equal("You have not drank any tea.");
  });

  it("consumes a single tea", function () {
    let speach = consumer.toSpeach(1);

    expect(speach).to.equal("You have drank a tea.");
  });
});


