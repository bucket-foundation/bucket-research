# Provenance — Jack Kruse Corpus

- **Source**: https://jackkruse.com (460 longevity / quantum-biology blog posts)
- **License**: citation-only. Full text remains on the source site. These
  snapshots are retained for canon cross-referencing and offline search.
- **Scraped**: 2026-04 (local working copy at `~/jackkruse/`)
- **Role in canon**: Kruse is *one partial source* within `05-biophysics`, not
  the centre. Biophysics canon draws from many primary sources; Kruse is
  included because he synthesizes a distinctive thesis (light / water / EMF /
  mitochondria) that's underrepresented in PubMed.
- **feed402 merchant**: `gianyrox/feed402` operates a v0.2-compliant dense
  vector index over this corpus (350-word chunks, 50-overlap, OpenAI
  `text-embedding-3-small`). Paid queries at $0.002 (insight) / $0.005 (query)
  / $0.010 (raw) emit citations back to `https://jackkruse.com/<slug>/`.
