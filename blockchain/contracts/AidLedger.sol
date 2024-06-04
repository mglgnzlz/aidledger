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
    address recipient
  );

  struct ReliefGood {
    uint256 id;
    address donor;
    string typeOfGood;
    string weight;
    string status;
    address recipient;
  }

  constructor() public {
    // createReliefGood(0x0000000000000000000000000000000000000001, "Canned food", "0.5 kg", "In transit", 0x000000000000000000000000000000000000000A);
    // createReliefGood(0x0000000000000000000000000000000000000002, "Clothes", "1 kg", "In transit", 0x000000000000000000000000000000000000000b);
    // createReliefGood(0x0000000000000000000000000000000000000003, "Noodles", "0.87 kg", "Delivered", 0x000000000000000000000000000000000000000C);
  }

  function createReliefGood(address _donor, string memory _typeOfGood, string memory _weight, string memory _status, address _recipient) public {
    reliefGoodCount++;
    reliefGoods[reliefGoodCount] = ReliefGood(reliefGoodCount, _donor, _typeOfGood, _weight, _status, _recipient);
    emit ReliefGoodCreated(reliefGoodCount, _donor, _typeOfGood, _weight, _status, _recipient);
  }

  function updateReliefGoodStatus(uint256 _id, string memory _status) public {
    reliefGoods[_id].status = _status;
  }

  function getReliefGood(uint256 _id) public view returns (uint256, address, string memory, string memory, string memory, address) {
    ReliefGood memory reliefGood = reliefGoods[_id];
    return (reliefGood.id, reliefGood.donor, reliefGood.typeOfGood, reliefGood.weight, reliefGood.status, reliefGood.recipient);
  }
}
