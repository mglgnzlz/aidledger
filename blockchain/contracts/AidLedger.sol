pragma solidity ^0.5.0;

contract AidLedger {
  uint public reliefGoodCount = 0;
  mapping(uint => ReliefGood) public reliefGoods;

  struct ReliefGood {
    uint id;
    string donor; // change to address instead of string later
    string description;
    string location;
    bool delivered;
  }

  constructor() public {
    createReliefGood("test donor", "test description", "test location");
  }

  // Create a new relief good
  function createReliefGood(string memory _donor, string memory _description, string memory _location) public {
    reliefGoodCount++;
    reliefGoods[reliefGoodCount] = ReliefGood(reliefGoodCount, _donor, _description, _location, false);
  }

  // Update relief good details
  function updateReliefGoodLocation(uint _id, string memory _location) public {
    reliefGoods[_id].location = _location;
  }

  // Mark relief good as delivered
  function markAsDelivered(uint _id) public {
    reliefGoods[_id].delivered = true;
  }

  // Get relief good details
  function getReliefGood(uint _id) public view returns (uint, string memory, string memory, string memory, bool) {
    return (reliefGoods[_id].id, reliefGoods[_id].donor, reliefGoods[_id].description, reliefGoods[_id].location, reliefGoods[_id].delivered);
  }
}