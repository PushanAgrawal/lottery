// SPDX-License-Identifier: MIT

pragma solidity  ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is Ownable,VRFConsumerBase {

    address payable[] public players;
    address payable public  recentWinner;
    uint256 public USDEntryFee;
    uint256 public randomness;
    AggregatorV3Interface internal ethUSDPriceFeed;
    enum Lottery_State {
        OPEN,
        CLOSED,
        CALCULATING_WIN
    }
    Lottery_State public lottery_state;
    uint256 public fee;
    bytes32 public keyhash;
    event RequestedRandomness(bytes32 requestId);

    constructor(address _PriceFeed, address _vrfCordinator, address _link,uint256 _fee, bytes32 _keyhash ) public VRFConsumerBase(_vrfCordinator, _link)  {
        USDEntryFee = 50*(10**18);
        ethUSDPriceFeed = AggregatorV3Interface(_PriceFeed);
        lottery_state = Lottery_State.CLOSED;
        // fee= _fee;
        // keyhash=_keyhash;

    }

    function enter() public payable {
        require(lottery_state==Lottery_State.OPEN);
        require(msg.value >= getEntranceFee(), "not enpugh eth");

        players.push(msg.sender);
    }

    function getEntranceFee() public view returns(uint256) {
        (, int256 price, , , ) = ethUSDPriceFeed.latestRoundData();
        uint256 adPrice = uint256(price*(10**10));
        uint256 costToEnter = (USDEntryFee * (10**18))/adPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(lottery_state==Lottery_State.CLOSED);
        lottery_state = Lottery_State.OPEN;

    }
    
    function endLottery() public {
        // require(lottery_state==0);
        lottery_state=Lottery_State.CALCULATING_WIN;
        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
    }
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override {
        require(lottery_state==Lottery_State.CALCULATING_WIN);
        require(_randomness>0,'random not found');
        uint256 winnerIndex = _randomness % players.length;
        recentWinner = players[winnerIndex];
        recentWinner.transfer(address(this).balance);
        
        players= new address payable[](0); 
        lottery_state=Lottery_State.CLOSED;
        randomness = _randomness;


    }
    

}