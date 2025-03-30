from web3 import Web3
from solcx import compile_source, install_solc

# Install solc 0.8.20 if not already installed
try:
    install_solc('0.8.20')
except Exception as e:
    print(f"Solc installation check: {e}")

# Connect to Sepolia testnet via Infura
infura_url = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"
w3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if not w3.is_connected():
    raise Exception("Failed to connect to Sepolia")

# Your wallet details (replace with your own when running)
private_key = "YOUR_PRIVATE_KEY"  # User must replace this
account = w3.eth.account.from_key(private_key)
w3.eth.default_account = account.address

# Check pending nonce and balance
nonce = w3.eth.get_transaction_count(account.address, 'pending')
balance = w3.eth.get_balance(account.address)
print(f"Using nonce: {nonce}")
print(f"Wallet balance: {w3.from_wei(balance, 'ether')} Sepolia ETH")

# Read and compile the Solidity contract
with open("FlashUSDT.sol", "r") as file:
    contract_source_code = file.read()

# Compile with specified solc version
compiled_sol = compile_source(contract_source_code, solc_version='0.8.20')
contract_interface = compiled_sol['<stdin>:FlashUSDT']

# Deploy the contract
FlashUSDT = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
initial_supply = 1000000  # 1 million FUSDT
tx = FlashUSDT.constructor(initial_supply).build_transaction({
    'from': account.address,
    'nonce': nonce,
    'gasPrice': w3.to_wei('30', 'gwei'),
    'gas': FlashUSDT.constructor(initial_supply).estimate_gas({'from': account.address})
})

# Check if balance is sufficient
gas_cost = tx['gas'] * tx['gasPrice']
if balance < gas_cost:
    print(f"Insufficient funds! Need at least {w3.from_wei(gas_cost, 'ether')} ETH")
    exit(1)

signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print(f"Deploying FlashUSDT... Tx hash: {tx_hash.hex()}")

# Wait for deployment
try:
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    contract_address = tx_receipt.contractAddress
    print(f"FlashUSDT deployed at: {contract_address}")
    print(f"Check your wallet ({account.address}) for {initial_supply} FUSDT!")
except Exception as e:
    print(f"Waiting failed: {e}")
    print(f"Check transaction status on https://sepolia.etherscan.io/tx/{tx_hash.hex()}")

# Verify balance if deployed
if 'contract_address' in locals():
    flash_usdt = w3.eth.contract(address=contract_address, abi=contract_interface['abi'])
    balance = flash_usdt.functions.balanceOf(account.address).call()
    print(f"Your FlashUSDT balance: {balance / 10**6} FUSDT")