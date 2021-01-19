pragma solidity >=0.7.0 <0.8.0;

/**
 * @title DCPG
 * @dev Distribution of Tokens according to Godwin Algorithm
 */
contract DCPG {
    struct ChargingProcess {
        string userID; // User ID, unique string
        string chargerID; // Charging unit ID, unique string
        address userWallet; // wallet address of user
        uint256 startTime; // Charging start time, in UNIX-Time
        uint256 estimatedDuration; //estimated charge duration, the user stated when starting to charge, in seconds
        uint256 availableFlex; //Amout of flex that user is willing to pay for charging boost, in wei
        uint256 desiredWh; //Amount of energy user wants to charge
    }

    // Admin address, that is allowed to stop charging processes
    address public godwin;

    // List of all charging processes in Contract (facility with limited energy)
    ChargingProcess[] public chargingprocesses;

    /**
     * @dev Returns the amount of current charging processes.
     * @return uint256 Length
     */
    function getChargingProcessesLength() public returns (uint256) {
        return chargingprocesses.length;
    }

    /**
     * @dev Function that can be called to charge wallet of contract (not really necessary but it is used)
     */

    function loadGasBuffer() public payable {}

    /**
     * @dev Constructor sets the admin account
     * @param station names of charging station
     */
    constructor(string memory station) public {
        godwin = msg.sender;
        // possibly save station id for future reference.
    }

    //function to delete a charging process from list. Used in stopCharging
    function _burn(uint256 x) internal {
        require(
            x < chargingprocesses.length,
            "Charging process could not be deleted."
        );
        chargingprocesses[x] = chargingprocesses[chargingprocesses.length - 1];
        chargingprocesses.pop();
    }

    /**
     * @dev Stops charging process and distributes flex to user
     * @param userID ID of user
     * @param chargerID ID of charger
     * @param endTime UNIX time of end time, currently not in use but to keep log in blockchain
     * @param flexFlow Flex flow calculated by God(win), to be payed out to user wallet.
     * @param chargedWh Charged energy during charing process, currently not in use but to keep log in blockchain
     */
    function stopCharging(
        string memory userID,
        string memory chargerID,
        uint256 endTime,
        int256 flexFlow,
        uint256 chargedWh
    ) public {
        // only admin may stop a charing process
        require(msg.sender == godwin, "Only godwin can stop charging process.");

        uint256 index = 0;
        bool found = false;

        // check wether userID is in charging processes
        for (uint256 x = 0; x < chargingprocesses.length; x++) {
            // Not elegantest method to check for string equality
            if (
                keccak256(abi.encodePacked(chargingprocesses[x].chargerID)) ==
                keccak256(abi.encodePacked(chargerID))
            ) {
                found = true;
                index = x;
                break;
            }
        }
        // return if not found
        require(found, "Charger ID not found.");

        // positive Flexflow equates to userWallet gets flextokens.
        // positive availableFlex equates to user wants to boost and has deposited tokens to be used
        require(
            int256(chargingprocesses[index].availableFlex) + flexFlow >= 0,
            "Godwin allocated too much Flex."
        );

        // calculate flexflow with deposited tokens for payout
        uint256 payout =
            uint256(int256(chargingprocesses[index].availableFlex) + flexFlow);

        // Save user wallet in temporary variable.
        address payable userWallet =
            payable(chargingprocesses[index].userWallet);

        // remove entry from list of charging processes
        _burn(index);

        // transfer the calculated tokens
        if (payout > 0) {
            userWallet.transfer(payout);
        }
    }

    /**
     * @dev Start charging process by appending to list of charging processes. Sender address and transaction value are saved as userWallet and availableFlex(deposit)
     * @param userID ID of user
     * @param chargerID ID of charger
     * @param startTime UNIX time of start time
     * @param estimatedDuration User stated estimated duration in seconds
     * @param desiredWh User desired amount of energy in Wh
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
                userWallet: msg.sender,
                startTime: startTime,
                estimatedDuration: estimatedDuration,
                availableFlex: msg.value,
                desiredWh: desiredWh
            })
        );
        // Possible improvement dispatch an event to be listend to by Godwin
    }
}
