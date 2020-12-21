pragma solidity >=0.4.22 <0.7.0;

/** 
 * @title DCPG
 * @dev Implements voting process along with vote delegation
 */
contract DCPG {
   
    struct ChargingProcess {
        string userID; // Kunden ID
        string chargerID;  // Saeule ID
        address chargee; // addresshash vom chargee
        uint startTime;   // 
        uint estimatedDuration;
        uint availableFlex; //desired Flex
        uint desiredWh;
    }

    address public godwin;

    ChargingProcess[] public chargingprocesses;

    /** 
     * @dev Create a new ballot to choose one of 'proposalNames'.
     * @param station names of proposals
     */
    constructor(string memory station) public { 
        godwin = msg.sender;
        //Welche Charger IDs zu welcher Station gehoeren
    }
    
    function _burn(uint x) internal {
        require(x < chargingprocesses.length,
        "Burn hat nicht funktioniert");
        chargingprocesses[x] = chargingprocesses[chargingprocesses.length-1];
        chargingprocesses.pop();
        //Check if deep copy and not shallow copy
    }
    /** 
     * @dev Give 'voter' the right to vote on this ballot. May only be called by 'chairperson'.
     * @param userID address of voter
     */
    function stopCharging(string memory userID, string memory chargerID, uint endTime, int flexFlow, uint chargedWh) public {
        require(
            msg.sender == godwin,
            "Only godwin can stop charging process."
        );
        uint index = 0;
        bool found = false;
        
        for (uint x = 0; x < chargingprocesses.length; x++){
            if (keccak256(abi.encodePacked(chargingprocesses[x].chargerID)) == keccak256(abi.encodePacked(chargerID))) {
                found = true;
                index = x;
                break;
            }
        }
        require(
            found,
            "Charger ID nicht bekannt."
            );
        //+Flexflow == chargee gets flextokens
        //Flexflow in Wei
        //checken ob genug tokens im wallet vorhanden
        
        //+availableFlex == Kunden will boost (Vorstreckung); Flexflow == Auszahlung vom Godwin (Negativ zum Verbrauch vom Flex)
        require( int(chargingprocesses[index].availableFlex) + flexFlow >= 0,
            "Godwin allocated too much Flex."
            );

        uint payout = uint(int(chargingprocesses[index].availableFlex) + flexFlow);
        address payable chargee = payable (chargingprocesses[index].chargee);
        _burn(index);
        chargee.transfer(payout);

    }

    /**
     * @dev Delegate your vote to the voter 'to'.
     * @param userID address to which vote is delegated
     */
     
     //Sanity Checks
    function startCharging(string memory userID, string memory chargerID, uint startTime, uint estimatedDuration, uint desiredWh) payable public {
        
        chargingprocesses.push(ChargingProcess({
            userID : userID, // Kunden ID
            chargerID : chargerID,  // Saeule ID
            chargee : msg.sender, // person delegated to
            startTime : startTime,   // index of the voted proposal
            estimatedDuration : estimatedDuration,
            availableFlex : msg.value,
            desiredWh : desiredWh
        }));
    }

}
