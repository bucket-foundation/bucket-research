# bucket-research

Public research index for Bucket Foundation. Consumer of the feed402 /
x402-research-gateway paid data rail.

## What this is

- One repo, eight canon branches (mirrors `bucket-canon/` on gdrive)
- Python consumer in `consumer/` that pays the gateway over x402 and writes
  citeable envelopes (`data + citation + receipt`) into the matching branch
- MIT code, CC0 intent on the index itself

## Canon branches

1. `01-mathematics` — axioms, real math
2. `02-physics` — laws, first principles
3. `03-chemistry` — periodic / quantum / thermo
4. `04-information` — computation, information theory
5. `05-biophysics` — mitochondria, light, quantum biology (Kruse = one partial source)
6. `06-cosmology` — spacetime, large-scale structure
7. `07-mind` — neuroscience, cognition, consciousness
8. `08-earth` — geosciences, climate, biosphere

## Pay-to-ingest

```bash
cd consumer
pip install -r requirements.txt
export GATEWAY_URL=https://research.agfarms.dev
export AGENT_PRIVATE_KEY=0x...    # Base Sepolia, USDC faucet balance
python ingest.py --branch 05-biophysics --query "circadian DHA mitochondria" --upstream pubmed
```

## Protocol

See [`gianyrox/feed402`](https://github.com/gianyrox/feed402) (canonical spec)
and [`gianyrox/x402-research-gateway`](https://github.com/gianyrox/x402-research-gateway)
(reference merchant, 7 live upstreams).
