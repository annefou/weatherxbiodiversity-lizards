# Snakefile — orchestrates the lizards replication pipeline end-to-end.
#
# Phase-2 pass-1 status: only `download` is fully wired. Rules `clean`,
# `analysis`, `figures` are placeholders to keep the DAG shape visible —
# they will be filled in pass-2 once 02/03/04 notebooks land. Each pass-2
# stub is marked `# TODO pass 2`.
#
# Usage:
#   snakemake --cores 1                  # run everything (pass 2 onward)
#   snakemake --cores 1 -n               # dry run
#   snakemake --cores 1 download         # only fetch input data

NOTEBOOKS = "notebooks"
DATA = "data"
RESULTS = "results"
FIGURES = "figures"


rule all:
    input:
        # Final figure and headline statistic land in pass 2; for now the
        # DAG's leaf is the source registry written by 01_data_download.
        f"{DATA}/raw/sources.json",
        # TODO pass 2 — restore these once 03/04 are written:
        # f"{RESULTS}/headline_statistic.json",
        # f"{FIGURES}/main_result.png",


# ---------- 01: Data download ----------
# Self-contained: fetches DestinE Climate DT t2m (2020-2039), CRU TS
# 3.24.01 historical Tmax, GBIF Lacertidae × Iberia occurrences, and
# runs the polytope sub-daily probe. Credentials needed for fresh
# fetches (POLYTOPE_USER_KEY for DestinE; GBIF_USER/GBIF_PWD/GBIF_EMAIL
# for GBIF). When credentials are absent the notebook logs "would
# fetch ..." and continues — see notebooks/01_data_download.py for the
# full skip semantics.
rule download:
    output:
        # Source registry is always written; other outputs (DestinE
        # GRIBs, GBIF zip, CRU NetCDFs) are conditional on credentials
        # and shared-cache availability, so we deliberately do not
        # declare them here. The source registry's `skipped` /
        # `would_fetch` entries are the provenance trail downstream
        # code reads.
        f"{DATA}/raw/sources.json",
    log:
        f"{RESULTS}/logs/01_data_download.log",
    shell:
        "mkdir -p $(dirname {log}) && "
        "cd " + NOTEBOOKS + " && "
        "jupytext --to notebook 01_data_download.py && "
        "jupyter execute --inplace 01_data_download.ipynb 2>&1 | tee ../{log}"


# ---------- 02: Data clean (TODO pass 2) ----------
# Will: decode DestinE GRIBs (HEALPix-NESTED nside=128) → aggregate to
# daily Tmax per cell over Iberia; load CRU TS tmx; tidy the GBIF
# Lacertidae occurrence dump into a clean per-species presence frame.
rule clean:
    input:
        f"{DATA}/raw/sources.json",
    output:
        # TODO pass 2 — declare the real outputs once 02_data_clean.py
        # is written. Likely candidates (mirror Bombus repo layout):
        #   data/intermediate/destine_t2m_iberia_nside128.nc
        #   data/intermediate/lacertidae_iberia_clean.parquet
        #   data/intermediate/cru_ts_tmx_iberia.nc
        touch(f"{DATA}/intermediate/.clean_done"),
    log:
        f"{RESULTS}/logs/02_data_clean.log",
    shell:
        # TODO pass 2 — port to:
        # "mkdir -p $(dirname {log}) && cd " + NOTEBOOKS + " && "
        # "jupytext --to notebook 02_data_clean.py && "
        # "jupyter execute --inplace 02_data_clean.ipynb 2>&1 | tee ../{log}"
        "mkdir -p $(dirname {log}) $(dirname {output}) && "
        "echo 'TODO pass 2: 02_data_clean.py not yet written' "
        "| tee {log} && touch {output}"


# ---------- 03: Analysis (TODO pass 2) ----------
# Will: compute h_r per cell per day via the SOM Equation S2
# (h_r = 0.74 × (T_max − T_b) + 6.1) for Iberian Lacertidae; integrate
# over the family critical reproductive window; compare against
# Sinervo Table 1 Lacertidae threshold h_r = 3.1 h to flag at-risk
# cells. Headline statistic = fraction of cells exceeding the
# threshold under each decade (2020-2029 vs 2030-2039).
rule analysis:
    input:
        f"{DATA}/intermediate/.clean_done",
    output:
        # TODO pass 2 — declare the real outputs once 03_analysis.py
        # is written. Likely candidate:
        #   results/headline_statistic.json
        #   results/hr_per_cell.nc
        touch(f"{RESULTS}/.analysis_done"),
    log:
        f"{RESULTS}/logs/03_analysis.log",
    shell:
        "mkdir -p $(dirname {log}) $(dirname {output}) && "
        "echo 'TODO pass 2: 03_analysis.py not yet written' "
        "| tee {log} && touch {output}"


# ---------- 04: Figures (TODO pass 2) ----------
# Will: produce figures/main_result.png — Iberia map of fraction-of-
# cells-at-risk per Lacertidae species, comparing 2020-2029 vs
# 2030-2039. Also a side comparison against the Sinervo Table 1
# Lacertidae 2050 projection (0.241 local extinction) as the headline
# extrapolation anchor.
rule figures:
    input:
        f"{RESULTS}/.analysis_done",
    output:
        # TODO pass 2 — declare the real outputs once 04_figures.py
        # is written. Likely candidate:
        #   figures/main_result.png
        touch(f"{FIGURES}/.figures_done"),
    log:
        f"{RESULTS}/logs/04_figures.log",
    shell:
        "mkdir -p $(dirname {log}) $(dirname {output}) && "
        "echo 'TODO pass 2: 04_figures.py not yet written' "
        "| tee {log} && touch {output}"
