pragma solidity >=0.7.0 <0.8.0;

/**
 * @title DCPG
 * @dev Distribution of Tokens according to Godwin Algorithm
 */
contract DCPG {
    struct ChargingProcess {
        string userID; // Client ID
        string chargerID; // Charging unit ID
        address chargee; // addresshash vom chargee
        uint256 startTime; // Charging start Time
        uint256 estimatedDuration; //estimated charge duration
        uint256 availableFlex; //Amout of flex that client is willing to pay for charging boost
        uint256 desiredWh; //Amount of Energy client wants to charge
    }

    address public godwin;

    ChargingProcess[] public chargingprocesses; //Array with all charging processes in Charging Station

    function getChargingProcessesLength() public returns (uint256) {
        return chargingprocesses.length;
    }

    /**
     * @dev Definition of which charging units are part of charging station
     * @param station names of charging station
     */
    constructor(string memory station) public {
        godwin = msg.sender;
        //Welche Charger IDs zu welcher Station gehoeren (Nice to have)
    }

    //function to delete a charging process from array. Used in stopCharging
    function _burn(uint256 x) internal {
        require(
            x < chargingprocesses.length,
            "Charging process could not be deleted."
        );
        chargingprocesses[x] = chargingprocesses[chargingprocesses.length - 1];
        chargingprocesses.pop();
        //Check if deep copy and not shallow copy
    }

    /**
     * @dev Stops charging process and distributes flex to client
     * @param userID ID of client
     */
    function stopCharging(
        string memory userID,
        string memory chargerID,
        uint256 endTime,
        int256 flexFlow,
        uint256 chargedWh
    ) public {
        require(msg.sender == godwin, "Only godwin can stop charging process.");
        uint256 index = 0;
        bool found = false;
        //Flexflow provided in Wei
        for (uint256 x = 0; x < chargingprocesses.length; x++) {
            if (
                keccak256(abi.encodePacked(chargingprocesses[x].chargerID)) ==
                keccak256(abi.encodePacked(chargerID))
            ) {
                found = true;
                index = x;
                break;
            }
        }
        require(found, "Charger ID not found.");
        //+Flexflow == chargee gets flextokens
        //checken ob genug tokens im wallet vorhanden

        //+availableFlex == Kunden will boost (Vorstreckung); Flexflow == Auszahlung vom Godwin (Negativ zum Verbrauch vom Flex)
        require(
            int256(chargingprocesses[index].availableFlex) + flexFlow >= 0,
            "Godwin allocated too much Flex."
        );

        uint256 payout =
            uint256(int256(chargingprocesses[index].availableFlex) + flexFlow);
        address payable chargee = payable(chargingprocesses[index].chargee);
        _burn(index);
        chargee.transfer(payout);
    }

    /**
     * @dev Starts charging process.
     * @param userID client ID.
     */

    //Sanity Checks
    function startCharging(
        string memory userID,
        string memory chargerID,
        uint256 startTime,
        uint256 estimatedDuration,
        uint256 desiredWh
    ) public payable {
        chargingprocesses.push(
            ChargingProcess({
                userID: userID,
                chargerID: chargerID,
                chargee: msg.sender,
                startTime: startTime,
                estimatedDuration: estimatedDuration,
                availableFlex: msg.value,
                desiredWh: desiredWh
            })
        );
    }
}
