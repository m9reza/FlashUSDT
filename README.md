# FlashUSDT on Sepolia

This project deploys a custom ERC-20 token called "Flash USDT" (FUSDT) on the Ethereum Sepolia testnet. It mints 1,000,000 FUSDT to the deployer's wallet.

## Files
- `FlashUSDT.sol`: The Solidity smart contract for the FUSDT token.
- `deploy_flashusdt.py`: Python script to compile and deploy the contract using web3.py.

## Prerequisites
- Python 3.x
- Libraries: `pip install web3 py-solc-x tronpy`
- An Infura account for Sepolia RPC endpoint
- A Sepolia wallet with test ETH (from a faucet like https://sepoliafaucet.com/)
- TronLink wallet (optional, for Tron-related experiments)

## How to Use
1. Clone this repository:
   ```bash
   git clone https://github.com/m9reza/FlashUSDT.git
   cd FlashUSDT