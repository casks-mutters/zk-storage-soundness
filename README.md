# zk-storage-soundness

## Overview
**zk-storage-soundness** is a lightweight Python CLI that verifies whether a smart contract’s **storage root** remains consistent between two blocks (or chains).  
This check is useful for ensuring **state integrity** in systems like **Aztec** or **Zama**, where on-chain storage consistency underpins zero-knowledge or encrypted proofs.

## Features
- Fetches storage root via `eth_getProof` RPC method  
- Compares roots between blocks or chains  
- Detects unexpected state changes or reinitializations  
- Works with any EVM-compatible network  
- Optional JSON output for CI/CD or monitoring scripts  

## Installation
1. Requires Python 3.9+  
2. Install dependencies:
   pip install web3
3. Set an RPC endpoint:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

## Usage
Fetch the storage root at the latest block:
   python app.py --address 0xYourContract

Compare between two blocks:
   python app.py --address 0xYourContract --from-block 20000000 --to-block 20010000

JSON output for automated analysis:
   python app.py --address 0xYourContract --from-block 20000000 --to-block 20010000 --json

## Example Output
🔧 zk-storage-soundness  
🔗 RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🧭 Chain ID: 1  
🏷️ Address: 0x00000000219ab540356cBB839Cbe05303d7705Fa  
🧱 From block: 20000000  
📦 Storage root @ 20000000: 0x5a3b7cf54ad8e9ff3a7f5cefb0a6b3cf78d25a8b4e0a13fa91c58a71d91a8bb4  
🧱 Comparing with block: 20010000  
📦 Storage root @ 20010000: 0x5a3b7cf54ad8e9ff3a7f5cefb0a6b3cf78d25a8b4e0a13fa91c58a71d91a8bb4  
🧩 Storage root comparison: ✅ MATCH  
⏱️ Completed in 0.64s  

## Notes
- If the RPC does not support `eth_getProof`, the tool may return `None` for the root.  
- For accurate audits, use archive nodes capable of historical proofs.  
- Works across Ethereum mainnet, L2s (Arbitrum, Base, Optimism), and private devnets.  
- Helpful for detecting stealth reinitializations or inconsistent proxy storage layouts.  
- In Aztec/Zama deployments, verifying stable storage roots ensures on-chain state soundness across proof systems.  
- Exit codes:  
  `0` → success (match or single root)  
  `2` → mismatch or retrieval failure.  
