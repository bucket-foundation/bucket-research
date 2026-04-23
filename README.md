# bucket-research

**The canonical research index for Bucket Foundation. Dual-mirrored with
[BucketDrive](https://drive.google.com/open?id=12QjkHYFqzVNm30kvkW-upi0kqa_Kri2B) on Google Drive.**

Any research artifact Gian ever produces lands in this tree — paid x402
envelopes, canon PDFs, Figma pulls, scraped corpora, annotated bibliographies.
One index, eight canon branches, forever.

## Tree

```
branches/
├── 01-mathematics/   axioms, real math
├── 02-physics/       laws, first principles
├── 03-chemistry/     periodic / quantum / thermo
├── 04-information/   computation, information theory
├── 05-biophysics/    mitochondria, light, quantum biology (Kruse = one partial source)
├── 06-cosmology/     spacetime, large-scale structure
├── 07-mind/          neuroscience, cognition, consciousness
├── 08-earth/         geosciences, climate, biosphere
├── _intake/          holding area — branch not yet decided
└── _archive/         superseded versions (YYYY-MM subdirs)
```

## Rules

- **Canon = foundations.** Axioms, laws, primary derivations, principles.
  Outcomes (longevity, disease, cognition) are downstream applications — they
  cross-mirror into `05-biophysics/sub-outcomes/` but don't define the branch.
- **Idempotent.** Re-running any ingestion pipeline must converge, not duplicate.
- **Citeable forever.** Every artifact carries a feed402 §3 envelope
  (`data + citation + receipt`) or canonical URL back to its primary source.
- **No PII, no credentials, no drafts, no `.env` files.**
- **Mirror both ways.** Anything pushed to this repo must also land in
  `gdrive:BucketDrive/<same-branch>/`, and vice versa.

## Pay-to-ingest

```bash
cd consumer
pip install -r requirements.txt
export GATEWAY_URL=https://research.agfarms.dev
export AGENT_PRIVATE_KEY=0x...    # Base Sepolia, USDC faucet balance
python ingest.py --branch 05-biophysics --query "circadian DHA mitochondria" --upstream pubmed
```

The consumer writes the feed402 envelope into `branches/<branch>/` and
(optionally) `rclone copy`s it into `gdrive:BucketDrive/<branch>/`.

## Protocol

- [`gianyrox/feed402`](https://github.com/gianyrox/feed402) — canonical spec (MIT code, CC0 intent)
- [`gianyrox/x402-research-gateway`](https://github.com/gianyrox/x402-research-gateway) — reference merchant, 7+ live upstreams on Base
