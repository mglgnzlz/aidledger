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

  it("Creates relief goods", async () => {
    const result = await this.aidLedger.createReliefGood(
      accounts[0],
      "Food",
      "1 kg",
      "Prepared",
      accounts[1],
      accounts[3]
    );
    const reliefGoodCount = await this.aidLedger.reliefGoodCount();
    assert.equal(reliefGoodCount.toNumber(), 1);

    const event = result.logs[0].args;
    assert.equal(event.id.toNumber(), 1);
    assert.equal(event.donor, accounts[0]);
    assert.equal(event.typeOfGood, "Food");
    assert.equal(event.weight, "1 kg");
    assert.equal(event.status, "Prepared");
    assert.equal(event.handler, accounts[1]);
    assert.equal(event.recipient, accounts[3]);
  });

  it("Lists relief goods", async () => {
    // Create a relief good for testing
    await this.aidLedger.createReliefGood(
      accounts[0],
      "Clothes",
      "2 kg",
      "Prepared",
      accounts[1],
      accounts[3]
    );

    const reliefGoodCount = await this.aidLedger.reliefGoodCount();
    const reliefGood = await this.aidLedger.reliefGoods(reliefGoodCount);
    assert.equal(reliefGood.id.toNumber(), reliefGoodCount.toNumber());
    assert.equal(reliefGood.donor, accounts[0]);
    assert.equal(reliefGood.typeOfGood, "Clothes");
    assert.equal(reliefGood.weight, "2 kg");
    assert.equal(reliefGood.status, "Prepared");
    assert.equal(reliefGood.handler, accounts[1]);
    assert.equal(reliefGood.recipient, accounts[3]);
  });

  it("Updates relief good status and handler", async () => {
    await this.aidLedger.updateReliefGoodHandler(2, "In transit", accounts[2]);
    const reliefGood = await this.aidLedger.reliefGoods(2);
    assert.equal(reliefGood.status, "In transit");
    assert.equal(reliefGood.handler, accounts[2]);
  });

  it("Updates relief good status and recipient", async () => {
    await this.aidLedger.updateReliefGoodRecipient(2, "Delivered", accounts[4]);
    const reliefGood = await this.aidLedger.reliefGoods(2);
    assert.equal(reliefGood.status, "Delivered");
    assert.equal(reliefGood.recipient, accounts[4]);
  });

  it("Gets relief good details", async () => {
    // Retrieve details of a relief good
    const reliefGood = await this.aidLedger.getReliefGood(2);
    assert.equal(reliefGood[0].toNumber(), 2);
    assert.equal(reliefGood[1], accounts[0]);
    assert.equal(reliefGood[2], "Clothes");
    assert.equal(reliefGood[3], "2 kg");
    assert.equal(reliefGood[4], "Delivered");
    assert.equal(reliefGood[5], accounts[2]);
    assert.equal(reliefGood[6], accounts[4]);
  });
});
