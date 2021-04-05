var expect = require("chai").expect;
import {TeaConsumer} from "../src/tea_consumer";

const consumer = new TeaConsumer();

describe("tea comsumer", function () {

  it("consumes plural number of tea", function () {
    let speach = consumer.consume(4);

    expect(speach).to.equal("You have consumed 4 cups of tea.");
  });

  it("consumes no tea", function () {
    let speach = consumer.consume(0);

    expect(speach).to.equal("You have not drank any tea.");
  });

  it("consumes a single tea", function () {
    let speach = consumer.consume(1);

    expect(speach).to.equal("You have drank a tea.");
  });
});


