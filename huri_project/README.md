# HuRI vs Lit-BM network topology (CB 5313, Topic 5)

## Question
HuRI (Luck et al. 2020, *Nature* 580:402) was built by systematically screening protein pairs by yeast two-hybrid.
Lit-BM is curated from hypothesis-driven literature. Do their global topologies differ, and which differences go
beyond what their degree sequences alone produce?

## Data source
HuRI (52,569 interactions) and Lit-BM (13,441 interactions) binary PPI edge lists (Ensembl gene IDs) from the
CCSB Human Reference Interactome portal, http://www.interactome-atlas.org/download (CC BY 4.0).
`src/download_data.py` fetches them into `data/` (falling back to the Netzschleuder mirror,
https://networks.skewed.de/net/huri, if the direct link fails). Raw data is git-ignored.
You can also download `HuRI.tsv` and `Lit-BM.tsv` manually from the portal and place them in `data/`.

## How to run
```
conda env create -f environment.yml && conda activate huri-topology     # or: pip install -r requirements.txt
python src/download_data.py
jupyter nbconvert --to notebook --execute HuRI_topology.ipynb            # or open the notebook and Run All
```
Runtime is a few minutes on a laptop CPU. Outputs are written to `results/`.

## What was done beyond a tutorial
Lit-BM comparator; degree-preserving rewiring null; hub/random node-removal sweep; k-core sweep; hub-overlap check;
density-matched control (HuRI subsampled to Lit-BM's edge count). Every notebook cell has an observation note under it.

## Results (summary; full interpretation in the notebook's last section)
- HuRI: 8,245 proteins / 52,068 edges (self-loops removed); Lit-BM: 5,956 / 12,758.
- Both have ~1.6-1.75x the clustering of a degree-preserving null and are disassortative beyond it.
- Hub removal (10% of proteins): largest component 63.6% (HuRI) vs 30.8% (Lit-BM); a density-matched HuRI keeps 50.1%,
  so most, not all, of the gap is density.
- Max coreness 27 vs 14; Lit-BM's 10-core is a small (67 proteins), very dense module.
- Shared proteins have nearly uncorrelated degree (Spearman 0.056); 1 of the top-50 hubs overlaps.

## Limitations
Topology only; HuRI covers an estimated 2-11% of the binary interactome and Y2H has limited sensitivity; one isoform
per gene; no per-gene publication counts, so study bias is suggested, not proven; static hub attack; 30 null replicates.

## AI use
Code scaffold and notebook notes drafted with Claude (Anthropic), then executed and checked on the real data.
