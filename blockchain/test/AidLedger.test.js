const AidLedger = artifacts.require("./AidLedger.sol");

contract("AidLedger", (accounts) => {
  before(async () => {
    this.aidLedger = await AidLedger.deployed();
  });

  it("Deploys successfully", async () => {
    const address = await this.aidLedger.address;
    assert.notEqual(address, 0x0);
    assert.notEqual(address, "");
    assert.notEqual(address, null);
    assert.notEqual(address, undefined);
  });

  it("Lists relief goods", async () => {
    const reliefGoodCount = await this.aidLedger.reliefGoodCount();
    const reliefGood = await this.aidLedger.reliefGoods(reliefGoodCount);
    assert.equal(reliefGood.id.toNumber(), reliefGoodCount.toNumber());
    assert.include(["Ced", "Kyle"], reliefGood.donor);
    assert.include(["Hotdog", "Egg"], reliefGood.description);
    assert.include(["Delivered", "In transit"], reliefGood.status);
    assert.include(["Migs", "Clarence"], reliefGood.recipient);
    assert.equal(reliefGoodCount.toNumber(), 3);
  });

  it("Creates relief goods", async () => {
    const result = await this.aidLedger.createReliefGood(
      "donor",
      "description",
      "status",
      "recipient"
    );
    const reliefGoodCount = await this.aidLedger.reliefGoodCount();
    assert.equal(reliefGoodCount.toNumber(), 4);
    const event = result.logs[0].args;
    assert.equal(event.id.toNumber(), 4);
    assert.equal(event.donor, "donor");
    assert.equal(event.description, "description");
    assert.equal(event.status, "status");
    assert.equal(event.recipient, "recipient");
  });
});
