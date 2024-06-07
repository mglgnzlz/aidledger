pragma solidity ^0.5.0;

contract AidLedger {
  uint256 public reliefGoodCount = 0;
  mapping(uint256 => ReliefGood) public reliefGoods;

  event ReliefGoodCreated(
    uint256 id,
    address donor,
    string typeOfGood,
    string weight,
    string status,
    address handler,
    address recipient
  );

  struct ReliefGood {
    uint256 id;
    address donor;
    string typeOfGood;
    string weight;
    string status;
    address handler;
    address recipient;
  }

  constructor() public {
  }

  function createReliefGood(address _donor, string memory _typeOfGood, string memory _weight, string memory _status, address _handler, address _recipient) public {
    reliefGoodCount++;
    reliefGoods[reliefGoodCount] = ReliefGood(reliefGoodCount, _donor, _typeOfGood, _weight, _status, _handler, _recipient);
    emit ReliefGoodCreated(reliefGoodCount, _donor, _typeOfGood, _weight, _status, _handler, _recipient);
  }

  function updateReliefGoodHandler(uint256 _id, string memory _status, address _handler) public {
    reliefGoods[_id].status = _status;
    reliefGoods[_id].handler = _handler;
  }

  function updateReliefGoodRecipient(uint256 _id, string memory _status, address _recipient) public {
    reliefGoods[_id].status = _status;
    reliefGoods[_id].recipient = _recipient;
  }

  function getReliefGood(uint256 _id) public view returns (uint256, address, string memory, string memory, string memory, address, address) {
    ReliefGood memory reliefGood = reliefGoods[_id];
    return (reliefGood.id, reliefGood.donor, reliefGood.typeOfGood, reliefGood.weight, reliefGood.status, reliefGood.handler, reliefGood.recipient);
  }
}
