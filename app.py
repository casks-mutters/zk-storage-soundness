# app.py
import os
import sys
import json
import time
import argparse
from typing import Dict, Any, Optional
from web3 import Web3

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

def get_storage_root(w3: Web3, address: str, block: Optional[str] = "latest") -> Optional[str]:
    """
    Retrieve the storage root of a contract using eth_getProof (if supported by the RPC).
    """
    try:
        address = Web3.to_checksum_address(address)
        proof = w3.provider.make_request("eth_getProof", [address, [], block])
        return proof.get("result", {}).get("storageHash")
    except Exception as e:
        print(f"❌ Failed to get storage root for {address}: {e}")
        return None

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-storage-soundness — verify that contract storage roots remain sound across blocks or between chains (useful for Aztec/Zama auditing)."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM RPC URL (default from RPC_URL)")
    p.add_argument("--address", required=True, help="Contract address to check")
    p.add_argument("--from-block", default="latest", help="Starting block tag/number (default: latest)")
    p.add_argument("--to-block", help="Compare against another block or chain endpoint")
    p.add_argument("--timeout", type=int, default=30, help="RPC timeout (seconds)")
    p.add_argument("--json", action="store_true", help="Output results in JSON format")
    return p.parse_args()

def main() -> None:
    start_time = time.time()
    args = parse_args()

    # Validate RPC URL
    if not args.rpc.startswith("http"):
        print("❌ Invalid RPC URL format. It must start with 'http' or 'https'.")
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": args.timeout}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check RPC_URL or --rpc parameter.")
        sys.exit(1)
        
 # Display current timestamp for audit logs
    from datetime import datetime
    print(f"🕒 Timestamp: {datetime.utcnow().isoformat()}Z")
    print("🔧 zk-storage-soundness")
    print(f"🔗 RPC: {args.rpc}")
    try:
        print(f"🧭 Chain ID: {w3.eth.chain_id}")
    except Exception:
        pass
    print(f"🏷️ Address: {args.address}")
    print(f"🧱 From block: {args.from_block}")

    root_from = get_storage_root(w3, args.address, args.from_block)
    if root_from is None:
        print("❌ Could not retrieve storage root from the source block.")
        sys.exit(2)
    print(f"📦 Storage root @ {args.from_block}: {root_from}")

    root_to = None
    if args.to_block:
        print(f"🧱 Comparing with block: {args.to_block}")
        root_to = get_storage_root(w3, args.address, args.to_block)
        if root_to is None:
            print("❌ Could not retrieve storage root from the destination block.")
            sys.exit(2)
        print(f"📦 Storage root @ {args.to_block}: {root_to}")

    if args.to_block:
        match = root_from.lower() == root_to.lower()
        status = "✅ MATCH" if match else "❌ MISMATCH"
        print(f"🧩 Storage root comparison: {status}")
    else:
        print("ℹ️ No comparison block provided — single root fetched.")

    elapsed = time.time() - start_time
    print(f"⏱️ Completed in {elapsed:.2f}s")

    if args.json:
        result = {
            "rpc": args.rpc,
            "address": Web3.to_checksum_address(args.address),
            "from_block": args.from_block,
            "to_block": args.to_block,
            "root_from": root_from,
            "root_to": root_to,
            "match": (root_from == root_to) if args.to_block else None,
            "elapsed_seconds": round(elapsed, 2)
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if (not args.to_block or root_from == root_to) else 2)

if __name__ == "__main__":
    main()
