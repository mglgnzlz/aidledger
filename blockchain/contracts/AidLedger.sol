pragma solidity ^0.5.0;

contract AidLedger {
  uint public reliefGoodCount = 0;
  mapping(uint => ReliefGood) public reliefGoods;

  event ReliefGoodCreated(
    uint id,
    string donor,
    string description,
    string status,
    string recipient
  );

  struct ReliefGood {
    uint id;
    string donor;
    string description;
    string status;
    string recipient;
  }

  constructor() public {
    createReliefGood("Migs", "Hotdog", "In transit", "Clarence");
    createReliefGood("Kyle", "Egg", "In transit", "Ced");
    createReliefGood("Ced", "Hotdog", "Delivered", "Migs");
  }

  // Create a new relief good
  function createReliefGood(string memory _donor, string memory _description, string memory _status, string memory _recipient) public {
    reliefGoodCount++;
    reliefGoods[reliefGoodCount] = ReliefGood(reliefGoodCount, _donor, _description, _status, _recipient);
    emit ReliefGoodCreated(reliefGoodCount, _donor, _description, _status, _recipient);
  }

  // Update relief good status
  function updateReliefGoodstatus(uint _id, string memory _status) public {
    reliefGoods[_id].status = _status;
  }

  // Get relief good details
  function getReliefGood(uint _id) public view returns (uint, string memory, string memory, string memory) {
    return (reliefGoods[_id].id, reliefGoods[_id].donor, reliefGoods[_id].description, reliefGoods[_id].status);
  }
}