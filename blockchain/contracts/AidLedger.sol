pragma solidity ^0.5.0;

contract AidLedger {
  uint256 public reliefGoodCount = 0;
  mapping(uint256 => ReliefGood) public reliefGoods;

  event ReliefGoodCreated(
    uint256 id,
    address donor,
    string description,
    string status,
    string recipient
  );

  struct ReliefGood {
    uint256 id;
    address donor;
    string description;
    string status;
    string recipient;
  }

  constructor() public {
    createReliefGood(0x0000000000000000000000000000000000000001, "Hotdog", "In transit", "Clarence");
    createReliefGood(0x0000000000000000000000000000000000000002, "Egg", "In transit", "Ced");
    createReliefGood(0x0000000000000000000000000000000000000003, "Hotdog", "Delivered", "Migs");
  }

  function createReliefGood(address _donor, string memory _description, string memory _status, string memory _recipient) public {
    reliefGoodCount++;
    reliefGoods[reliefGoodCount] = ReliefGood(reliefGoodCount, _donor, _description, _status, _recipient);
    emit ReliefGoodCreated(reliefGoodCount, _donor, _description, _status, _recipient);
  }

  function updateReliefGoodStatus(uint256 _id, string memory _status) public {
    reliefGoods[_id].status = _status;
  }

  function getReliefGood(uint256 _id) public view returns (uint256, address, string memory, string memory, string memory) {
    ReliefGood memory reliefGood = reliefGoods[_id];
    return (reliefGood.id, reliefGood.donor, reliefGood.description, reliefGood.status, reliefGood.recipient);
  }
}
