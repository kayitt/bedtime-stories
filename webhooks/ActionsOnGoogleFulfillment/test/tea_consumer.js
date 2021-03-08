var expect    = require("chai").expect;
var consumer = require("../tea_consumer");

describe("Color Code Converter", function() {
  describe("RGB to Hex conversion", function() {
    it("converts the basic colors", function() {
      let speach = consumer.toSpeach(4);

      expect(speach).to.equal("You have conumed 4 cups of tea.");
    });
  });

});

