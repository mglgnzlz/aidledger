var AidLedger = artifacts.require("./AidLedger.sol");

module.exports = function (deployer) {
  deployer.deploy(AidLedger);
};
