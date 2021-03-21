var expect = require("chai").expect;
var pathProvider = require("../../webhooks/ActionsOnGoogleFulfillment/path_provider.js");

describe("path provider", function () {

  it("accepts the current date", function () {
    pathProvider.basePath(new Date());
  });

  it("returns base path for the current date", function () {
    let path = pathProvider.basePath(new Date("2021-03-21T07:45:00Z"));

    expect(path).to.equal("/home/2021-03-21");
  });

  it("returns base path for another day", function () {
    let path = pathProvider.basePath(new Date("2020-01-12T07:45:00Z"));

    expect(path).to.equal("/home/2020-01-12");
  });
});


