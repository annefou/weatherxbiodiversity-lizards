# Snakefile — orchestrates the lizards replication pipeline end-to-end.
#
# Phase-2 pass-2 status: all four notebooks are wired with real input /
# output declarations. `snakemake --cores 1` runs the whole DAG; the
# leaf is `figures/main_result.png` (the Phase-3 headline figure).
#
# Usage:
#   snakemake --cores 1                  # run everything
#   snakemake --cores 1 -n               # dry run
#   snakemake --cores 1 download         # only fetch input data
#   snakemake --cores 1 clean            # 01 + 02
#   snakemake --cores 1 analysis         # 01 + 02 + 03
#   snakemake --cores 1 figures          # 01 + 02 + 03 + 04

NOTEBOOKS = "notebooks"
DATA = "data"
RESULTS = "results"
FIGURES = "figures"

INTERMEDIATE = f"{DATA}/intermediate"


rule all:
    input:
        f"{FIGURES}/main_result.png",
        f"{FIGURES}/h_r_map_2020s.png",
        f"{FIGURES}/h_r_map_2030s.png",
        f"{RESULTS}/headline.json",


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


# ---------- 02: Data clean ----------
# Decodes DestinE GRIBs (HEALPix-NESTED nside=128) message-by-message
# via the eccodes Python API and subsets to ~479 Iberian cells →
# per-cell × per-day Tmax/Tmin NetCDF. Loads CRU TS tmx/tmn (regular
# lat/lon, monthly), restricts to Iberia, samples at HEALPix cell
# centres → monthly NetCDF. Unzips the pre-minted GBIF download,
# assigns occurrences to HEALPix nside=128 cells → per-species per-cell
# presence Parquet (+ sensitivity copy at nside=64 via the NESTED
# parent operation child >> 2).
rule clean:
    input:
        f"{DATA}/raw/sources.json",
        f"{DATA}/destine/raw/destine_2020_2029_t2m.grib",
        f"{DATA}/destine/raw/destine_2030_2039_t2m.grib",
        f"{DATA}/gbif/lacertidae_iberia.zip",
    output:
        destine = f"{INTERMEDIATE}/destine_iberia_daily_t2m_nside128.nc",
        cru = f"{INTERMEDIATE}/cru_iberia_monthly_nside128.nc",
        presence_128 = f"{INTERMEDIATE}/gbif_lacertidae_presence_nside128.parquet",
        presence_64 = f"{INTERMEDIATE}/gbif_lacertidae_presence_nside64.parquet",
        report = f"{INTERMEDIATE}/clean_report.json",
    log:
        f"{RESULTS}/logs/02_data_clean.log",
    shell:
        "mkdir -p $(dirname {log}) " + INTERMEDIATE + " && "
        "cd " + NOTEBOOKS + " && "
        "jupytext --to notebook 02_data_clean.py && "
        "jupyter execute --inplace 02_data_clean.ipynb 2>&1 | tee ../{log}"


# ---------- 03: Analysis ----------
# Applies SOM Equation S2 (h_r = 0.74·(T_max - T_b) + 6.1) to per-cell
# × per-day DestinE Tmax, restricts to the April-May reproductive
# window, sums to cumulative h_r per cell × per year, and flags cells
# exceeding the Lacertidae family threshold h_r = 3.1 h. Aggregates
# to per-species local-extinction rates per decade (2020s vs 2030s).
# Persists the per-cell × per-year extinction mask + per-species CSV
# + headline JSON.
rule analysis:
    input:
        destine = f"{INTERMEDIATE}/destine_iberia_daily_t2m_nside128.nc",
        presence = f"{INTERMEDIATE}/gbif_lacertidae_presence_nside128.parquet",
        presence_n64 = f"{INTERMEDIATE}/gbif_lacertidae_presence_nside64.parquet",
        # Sub-daily probe log is read but not strictly required to be
        # present — the notebook tolerates its absence.
    output:
        mask = f"{INTERMEDIATE}/extinction_mask_nside128.nc",
        per_species = f"{RESULTS}/tables/local_extinction_per_species.csv",
        substrate_sensitivity = f"{RESULTS}/tables/substrate_sensitivity_per_species.csv",
        headline = f"{RESULTS}/headline.json",
    log:
        f"{RESULTS}/logs/03_analysis.log",
    shell:
        "mkdir -p $(dirname {log}) " + RESULTS + "/tables && "
        "cd " + NOTEBOOKS + " && "
        "jupytext --to notebook 03_analysis.py && "
        "jupyter execute --inplace 03_analysis.ipynb 2>&1 | tee ../{log}"


# ---------- 04: Figures ----------
# Produces five figures: the sensitivity-matrix headline (T_b × window
# heatmap, 2020s vs 2030s), a per-species local-extinction lollipop for
# the baseline config, the substrate-sensitivity scatter mirroring the
# Bombus chain-3 pattern (nside=128 vs nside=64), and two Iberia maps
# of decadal daily-mean h_r with the 3.1 h threshold contour.
rule figures:
    input:
        mask = f"{INTERMEDIATE}/extinction_mask_nside128.nc",
        per_species = f"{RESULTS}/tables/local_extinction_per_species.csv",
        headline = f"{RESULTS}/headline.json",
    output:
        main_png = f"{FIGURES}/main_result.png",        # sensitivity matrix
        main_pdf = f"{FIGURES}/main_result.pdf",
        per_species_png = f"{FIGURES}/per_species_rates.png",       # S3a config only
        per_species_pdf = f"{FIGURES}/per_species_rates.pdf",
        substrate_png = f"{FIGURES}/substrate_sensitivity.png",
        substrate_pdf = f"{FIGURES}/substrate_sensitivity.pdf",
        map_2020s = f"{FIGURES}/h_r_map_2020s.png",
        map_2030s = f"{FIGURES}/h_r_map_2030s.png",
    log:
        f"{RESULTS}/logs/04_figures.log",
    shell:
        "mkdir -p $(dirname {log}) " + FIGURES + " && "
        "cd " + NOTEBOOKS + " && "
        "jupytext --to notebook 04_figures.py && "
        "jupyter execute --inplace 04_figures.ipynb 2>&1 | tee ../{log}"
