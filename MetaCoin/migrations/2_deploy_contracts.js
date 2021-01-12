var dcpg = artifacts.require("DCPG")

module.exports = function(deployer) {
    deployer.deploy(dcpg, 'dcpg');
};