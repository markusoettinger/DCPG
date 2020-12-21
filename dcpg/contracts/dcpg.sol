pragma solidity >=0.4.22 <0.7.0;

/** 
 * @title DCPG
 * @dev Distribution of Tokens according to Godwin Algorithm
 */
contract DCPG {
   
    struct ChargingProcess {
        string userID; // Client ID
        string chargerID;  // Charging unit ID
        address chargee; // addresshash vom chargee
        uint startTime;   // Charging start Time
        uint estimatedDuration; //estimated charge duration
        uint availableFlex; //Amout of flex that client is willing to pay for charging boost
        uint desiredWh; //Amount of Energy client wants to charge
    }

    address public godwin;

    ChargingProcess[] public chargingprocesses; //Array with all charging processes in Charging Station

    /** 
     * @dev Definition of which charging units are part of charging station
     * @param station names of charging station
     */
    constructor(string memory station) public { 
        godwin = msg.sender;
        //Welche Charger IDs zu welcher Station gehoeren (Nice to have)
    }
    
    //function to delete a charging process from array. Used in stopCharging
    function _burn(uint x) internal {
        require(x < chargingprocesses.length,
        "Charging process could not be deleted.");
        chargingprocesses[x] = chargingprocesses[chargingprocesses.length-1];
        chargingprocesses.pop();
        //Check if deep copy and not shallow copy
    }
    /** 
     * @dev Stops charging process and distributes flex to client
     * @param userID ID of client
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
            "Charger ID not found."
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
     * @dev Starts charging process.
     * @param userID client ID.
     */
     
     //Sanity Checks
    function startCharging(string memory userID, string memory chargerID, uint startTime, uint estimatedDuration, uint desiredWh) payable public {
        
        chargingprocesses.push(ChargingProcess({
            userID : userID, 
            chargerID : chargerID,  
            chargee : msg.sender, 
            startTime : startTime, 
            estimatedDuration : estimatedDuration,
            availableFlex : msg.value,
            desiredWh : desiredWh
        }));
    }

}
