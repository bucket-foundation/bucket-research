#!/usr/bin/env python3
"""Minimal feed402 consumer. Discover → 402 → sign EIP-3009 → pay → store envelope.

Intentionally small: ~150 LOC, stdlib + httpx + eth-account.
"""
import argparse, json, os, pathlib, sys, time, secrets, base64
import httpx
from eth_account import Account
from eth_account.messages import encode_typed_data

USDC = {
    "base": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "base-sepolia": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
}

def sign_eip3009(pk, chain_id, network, to, value, valid_seconds=60):
    acct = Account.from_key(pk)
    now = int(time.time())
    nonce = "0x" + secrets.token_hex(32)
    msg = {
        "domain": {"name": "USD Coin", "version": "2",
                   "chainId": chain_id, "verifyingContract": USDC[network]},
        "primaryType": "TransferWithAuthorization",
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"}],
            "TransferWithAuthorization": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "validAfter", "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce", "type": "bytes32"}]},
        "message": {"from": acct.address, "to": to, "value": str(value),
                    "validAfter": "0", "validBefore": str(now + valid_seconds),
                    "nonce": nonce},
    }
    signed = acct.sign_message(encode_typed_data(full_message=msg))
    return msg["message"], signed.signature.hex()

def pay_and_fetch(gateway, path, params, pk, network="base-sepolia"):
    url = f"{gateway}{path}"
    r = httpx.get(url, params=params, timeout=30)
    if r.status_code != 402:
        r.raise_for_status()
        return r.json()
    challenge = r.json()
    accepted = challenge["accepts"][0]
    chain_id = 84532 if network == "base-sepolia" else 8453
    auth, sig = sign_eip3009(pk, chain_id, network,
                             accepted["payTo"], int(accepted["maxAmountRequired"]))
    payload = {"x402Version": 1,
               "payload": {"authorization": auth, "signature": sig},
               "accepted": accepted}
    header = base64.b64encode(json.dumps(payload).encode()).decode()
    r2 = httpx.get(url, params=params,
                   headers={"X-PAYMENT": header}, timeout=60)
    r2.raise_for_status()
    return r2.json()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--branch", required=True)
    ap.add_argument("--query", required=True)
    ap.add_argument("--upstream", default="pubmed")
    ap.add_argument("--gateway", default=os.environ.get("GATEWAY_URL", "http://localhost:8091"))
    args = ap.parse_args()

    pk = os.environ.get("AGENT_PRIVATE_KEY")
    if not pk:
        sys.exit("set AGENT_PRIVATE_KEY (Base Sepolia, USDC faucet)")

    route = {"pubmed": ("/research/pubmed/search", {"term": args.query}),
             "s2": ("/research/semantic-scholar/search", {"query": args.query}),
             "openalex": ("/research/openalex/works", {"search": args.query}),
             "kruse": ("/research/kruse/search", {"q": args.query})}[args.upstream]
    env = pay_and_fetch(args.gateway, route[0], route[1], pk)

    out = pathlib.Path("..") / "branches" / args.branch / f"{args.upstream}-{int(time.time())}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(env, indent=2))
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
