"""Download HuRI and Lit-BM (Luck et al. 2020) as Ensembl-gene-ID edge lists -> data/HuRI.tsv, data/Lit-BM.tsv.

Source 1 (primary, CCSB):  http://www.interactome-atlas.org/download   (CC BY 4.0)
Source 2 (fallback mirror): https://networks.skewed.de/net/huri        (Netzschleuder, same data, CSV zip)
Raw data is NOT committed to git. Run:  python src/download_data.py
If the CCSB direct URL fails, the script automatically falls back to the mirror.
"""
import io, pathlib, zipfile, requests
import pandas as pd

OUT = pathlib.Path(__file__).resolve().parent.parent / "data"
ATLAS = {"HuRI": "http://www.interactome-atlas.org/data/HuRI.tsv",
         "Lit-BM": "http://www.interactome-atlas.org/data/Lit-BM.tsv"}
MIRROR = {"HuRI": "https://networks.skewed.de/net/huri/files/HuRI.csv.zip",
          "Lit-BM": "https://networks.skewed.de/net/huri/files/Lit-BM.csv.zip"}

def from_atlas(name):
    r = requests.get(ATLAS[name], timeout=120); r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text), sep="\t", header=None, usecols=[0, 1], comment="#", dtype=str)
    df = df[df[0].str.startswith("ENSG", na=False) & df[1].str.startswith("ENSG", na=False)]  # drops any header row
    if df.empty: raise ValueError("no ENSG rows found")
    return df

def from_mirror(name):
    r = requests.get(MIRROR[name], timeout=120); r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    edges = pd.read_csv(z.open("edges.csv"), header=None, comment="#", usecols=[0, 1])
    nodes = pd.read_csv(z.open("nodes.csv"), header=None, comment="#", usecols=[0, 1], dtype={1: str})
    m = dict(zip(nodes[0], nodes[1]))                      # node index -> Ensembl gene ID
    return pd.DataFrame({0: edges[0].map(m), 1: edges[1].map(m)}).dropna()

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name in ATLAS:
        dest = OUT / f"{name}.tsv"
        if dest.exists(): print("exists:", dest); continue
        try:
            df, src = from_atlas(name), "interactome-atlas.org"
        except Exception as e:
            print(f"{name}: atlas failed ({e}); using Netzschleuder mirror")
            df, src = from_mirror(name), "networks.skewed.de"
        df.to_csv(dest, sep="\t", header=False, index=False)
        print(f"saved {dest}  ({len(df)} rows, source: {src})")
