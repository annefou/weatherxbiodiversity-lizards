# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 01 — Data download (Iberian Lacertidae, Sinervo 2010 h_r mechanism)
#
# This notebook fetches **all** input data needed by the cross-taxon
# Sinervo replication. It is self-contained: a fresh clone of the repo
# can run this notebook end-to-end provided the relevant credentials
# (Polytope / DestinE for the climate twin and GBIF for the occurrence
# download) are available as environment variables.
#
# Five artefacts:
#
# 1. **DestinE Climate DT daily T<sub>max</sub>** for 2020–2029 and
#    2030–2039 (SSP3-7.0, IFS-NEMO, HEALPix-NESTED nside=128). Reused
#    from `weatherxbiodiversity-projection`'s already-fetched GRIBs if
#    `WEATHERXBIO_SHARED_DATA_DIR` points at that repo and the files
#    exist; otherwise a fresh polytope retrieve is attempted (credentials
#    required — env vars `POLYTOPE_USER_KEY` or interactive
#    `polytope-client login`).
# 2. **Polytope sub-daily probe** — a tiny one-day hourly Tmax retrieve
#    over Iberia for 2025-07-15. The probe answers: "is sub-daily Climate
#    DT data accessible to this user account?" If yes, downstream code in
#    pass 2 will use real hourly T(t) for the h_r integral; if no, it
#    will fall back to a sinusoidal diurnal-cycle reconstruction from
#    daily T<sub>max</sub> + T<sub>min</sub>. The probe never raises —
#    failures are logged and the boolean result is persisted.
# 3. **CRU TS 3.24.01 historical T<sub>max</sub>** (1901–2015 in decade
#    chunks). Provides the historical climatology / 1975 baseline for
#    calibrating Iberian-Lacertidae thermal-physiology priors. Reused
#    from the Bombus repo's Soroye-figshare extraction if present;
#    otherwise refetched from Soroye 2020 figshare deposit
#    (DOI [10.6084/m9.figshare.10058340](https://doi.org/10.6084/m9.figshare.10058340)).
# 4. **GBIF Lacertidae × Iberia occurrence download** — a fresh download
#    minted against the GBIF API (predicate: family=Lacertidae × country
#    ∈ {ES, PT, AD, GI} × hasCoordinate=True × hasGeospatialIssue=False
#    × basisOfRecord ∈ {HUMAN_OBSERVATION, PRESERVED_SPECIMEN,
#    MACHINE_OBSERVATION} × year≥1900). Per DOMAIN.md "GBIF download
#    DOIs are mandatory" we mint a fresh DOI for the lizards chain rather
#    than reuse the Bombus DOI `10.15468/dl.3frmsq` (reuse would falsify
#    lineage). The DOI is persisted to `data/gbif/download_doi.txt` and
#    the zip to `data/gbif/lacertidae_iberia.zip`; subsequent runs are
#    cached.
# 5. **Source registry** — a single JSON written to
#    `data/raw/sources.json` recording every download's URL/DOI/license/
#    accessed-on date for downstream provenance and the Replication
#    Study draft.
#
# **Credentials needed for fresh downloads** (cached path needs none):
#
# | Source | Env vars | Where to get |
# |---|---|---|
# | DestinE Climate DT | `POLYTOPE_USER_KEY` (or `~/.polytopeapirc` from `polytope-client login`) | https://destination-earth.eu/ — DestinE Data Lake account |
# | GBIF | `GBIF_USER`, `GBIF_PWD`, `GBIF_EMAIL` | https://www.gbif.org/user/profile |
#
# **Behaviour when credentials are absent**: every fresh-fetch path
# detects the missing credential, prints a clear "would fetch …" message,
# logs the intended request, and continues. The notebook therefore
# always exits 0, but does not necessarily produce every artefact in a
# fresh checkout without credentials. Pass-2 cleaning code will raise on
# the missing inputs.

# %%
import json
import os
import shutil
import sys
import time
import traceback
import zipfile
from datetime import date
from pathlib import Path

import requests

# %% [markdown]
# ## Paths and shared-cache reuse
#
# Anne's local machine already has DestinE GRIBs and the Soroye-figshare
# CRU TS chunks under the sister `weatherxbiodiversity-projection` repo.
# Reuse them to save bandwidth and Polytope quota. Override the cache
# location with `WEATHERXBIO_SHARED_DATA_DIR` if your layout differs.

# %%
ROOT = Path("..").resolve()
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DESTINE_DIR = DATA_DIR / "destine"
DESTINE_RAW_DIR = DESTINE_DIR / "raw"
DESTINE_SUBDAILY_DIR = DESTINE_DIR / "sub_daily"
GBIF_DIR = DATA_DIR / "gbif"
CRU_DIR = DATA_DIR / "cru_ts"

for d in (RAW_DIR, DESTINE_RAW_DIR, DESTINE_SUBDAILY_DIR, GBIF_DIR, CRU_DIR):
    d.mkdir(parents=True, exist_ok=True)

WEATHERXBIO_SHARED_DATA_DIR = Path(
    os.environ.get(
        "WEATHERXBIO_SHARED_DATA_DIR",
        Path.home() / "Documents/ScienceLive/weatherxbiodiversity-projection",
    )
)
SHARED_DESTINE_RAW = WEATHERXBIO_SHARED_DATA_DIR / "data" / "destine" / "raw"
SHARED_CRU_DIR = (
    WEATHERXBIO_SHARED_DATA_DIR
    / "reference"
    / "Bumblebee_repo_wbombusdat"
    / "0_ClimateData"
)

# Single source-registry collector; written at the end of the notebook.
SOURCES: list[dict] = []

# Thresholds: "if the file exists and is bigger than this many bytes,
# treat it as already-fetched". Conservative numbers — small enough to
# always re-fetch obviously broken downloads, large enough to never
# false-positive on a real fetch.
MIN_GRIB_BYTES = 100_000_000  # DestinE decade-t2m GRIBs are ~6.3 GB
MIN_NC_BYTES = 1_000_000      # CRU TS decade tmx is ~few hundred MB
MIN_ZIP_BYTES = 1_000         # GBIF zip is small for taxon-restricted query
MIN_PROBE_BYTES = 1_000       # one-day Iberia hourly grib is tiny

print(f"ROOT = {ROOT}")
print(f"WEATHERXBIO_SHARED_DATA_DIR = {WEATHERXBIO_SHARED_DATA_DIR}")
print(f"  shared DestinE raw : {SHARED_DESTINE_RAW} (exists={SHARED_DESTINE_RAW.exists()})")
print(f"  shared CRU TS dir  : {SHARED_CRU_DIR} (exists={SHARED_CRU_DIR.exists()})")


# %% [markdown]
# ## 1. DestinE Climate DT daily T<sub>max</sub> (2020-2039)
#
# IFS-NEMO standard resolution = HEALPix-NESTED nside=128 (~78 km native
# cell width). Two GRIBs (one per decade), `param=167` (2 m temperature).
# **Locked scope**: Sinervo's h_r mechanism is thermal-only. We do not
# need `tp` (precipitation), so this lizards chain fetches t2m only.
#
# Polytope request shape is identical to the Bombus repo's
# `05_destine_download.py` (see `weatherxbiodiversity-projection/notebooks/`),
# minus the `tp` request. Auth: env var `POLYTOPE_USER_KEY` OR a
# pre-existing `~/.polytopeapirc` written by `polytope-client login`.
#
# The reuse-then-fetch contract:
#
# 1. If `data/destine/raw/destine_<horizon>_t2m.grib` exists locally,
#    use it.
# 2. Else, if the shared Bombus cache file exists, copy (not symlink —
#    notebooks should be self-contained against `WEATHERXBIO_SHARED_DATA_DIR`
#    moving) into `data/destine/raw/`.
# 3. Else, mint a fresh polytope retrieve.
# 4. If credentials are absent at step 3, log "would fetch …" and
#    continue.

# %%
POLYTOPE_COLLECTION = "destination-earth"
POLYTOPE_ADDRESS = "https://polytope.lumi.apps.dte.destination-earth.eu"

DESTINE_HORIZONS = {
    "2020_2029": ("20200101", "20291231"),
    "2030_2039": ("20300101", "20391231"),
}


def has_polytope_credentials() -> bool:
    """Bombus-repo `_tier2_guard` detection logic, narrowed to Polytope."""
    if os.environ.get("POLYTOPE_USER_KEY"):
        return True
    if Path("~/.polytopeapirc").expanduser().exists():
        return True
    if Path("~/.destine/auth.toml").expanduser().exists():
        return True
    return False


def build_destine_t2m_request(start_date: str, end_date: str) -> dict:
    """Polytope request body — daily 2 m temperature, SSP3-7.0, IFS-NEMO,
    standard (HEALPix-NESTED nside=128).

    Matches the verified-working shape from
    `weatherxbiodiversity-projection/notebooks/05_destine_download.py`.
    No `area` key: DestinE IFS-NEMO is HEALPix-archived and MARS cannot
    crop HEALPix data with a lat/lon bbox. We retrieve globally and
    subset Iberia in 02_data_clean (pass 2).
    """
    return {
        "class": "d1",
        "dataset": "climate-dt",
        "activity": "ScenarioMIP",
        "experiment": "SSP3-7.0",
        "expver": "0001",
        "generation": "1",
        "realization": "1",
        "model": "IFS-NEMO",
        "resolution": "standard",
        "type": "fc",
        "stream": "clte",
        "levtype": "sfc",
        "param": "167",                  # 2 m temperature
        "date": f"{start_date}/to/{end_date}",
        "time": "0000/0600/1200/1800",   # 4x/day instantaneous
    }


def fetch_destine_t2m(horizon: str, start: str, end: str) -> Path:
    target = DESTINE_RAW_DIR / f"destine_{horizon}_t2m.grib"

    # Step 1: already in this repo's cache?
    if target.exists() and target.stat().st_size > MIN_GRIB_BYTES:
        print(f"  [cached]  {target}  ({target.stat().st_size:,} bytes)")
        return target

    # Step 2: try the shared Bombus-repo cache.
    shared = SHARED_DESTINE_RAW / f"destine_{horizon}_t2m.grib"
    if shared.exists() and shared.stat().st_size > MIN_GRIB_BYTES:
        print(f"  [reuse ]  {shared} -> {target}")
        # Use symlink rather than copy: avoids duplicating 6.3 GB per
        # decade. If the shared file later disappears, downstream code
        # will fail loudly via FileNotFoundError. The downloader contract
        # remains satisfied because `target` is present.
        try:
            if target.is_symlink() or target.exists():
                target.unlink()
            target.symlink_to(shared)
        except OSError:
            print(f"    symlink failed; copying instead ({shared.stat().st_size:,} bytes)")
            shutil.copy2(shared, target)
        return target

    # Step 3: fresh polytope retrieve.
    if not has_polytope_credentials():
        print(
            f"  [skip  ]  {target.name} — no Polytope credentials.\n"
            f"            set POLYTOPE_USER_KEY env var or run "
            f"'polytope-client login' first.\n"
            f"            would request: {build_destine_t2m_request(start, end)}"
        )
        return target

    # Lazy import so the notebook does not require polytope-client to
    # parse / partially execute.
    from polytope.api import Client  # type: ignore

    request = build_destine_t2m_request(start, end)
    print(f"  [fetch ]  {target.name}")
    print(f"            request = {request}")
    client = Client(address=POLYTOPE_ADDRESS)
    client.retrieve(
        POLYTOPE_COLLECTION, request,
        output_file=str(target),
        asynchronous=False,
    )
    print(f"            saved {target} ({target.stat().st_size:,} bytes)")
    return target


print("\n--- 1. DestinE Climate DT daily T2M ---")
destine_paths: dict[str, Path] = {}
for horizon, (start, end) in DESTINE_HORIZONS.items():
    destine_paths[horizon] = fetch_destine_t2m(horizon, start, end)

SOURCES.append({
    "name": "Destination Earth Climate DT — SSP3-7.0 IFS-NEMO t2m",
    "doi": None,
    "url": POLYTOPE_ADDRESS,
    "license": "DestinE Data Lake terms (https://destination-earth.eu/)",
    "accessed_on": date.today().isoformat(),
    "horizons": list(DESTINE_HORIZONS.keys()),
    "request_keys": {
        "class": "d1", "dataset": "climate-dt",
        "experiment": "SSP3-7.0", "model": "IFS-NEMO",
        "resolution": "standard", "param": "167",
    },
    "local_paths": [str(p.relative_to(ROOT)) for p in destine_paths.values()],
    "reused_from": str(SHARED_DESTINE_RAW) if SHARED_DESTINE_RAW.exists() else None,
})


# %% [markdown]
# ## 2. Polytope sub-daily probe (one-day hourly T<sub>max</sub> over Iberia)
#
# **Untested — runs on first execution against the live Polytope
# endpoint.** This is a *probe*: it answers a single question — "does my
# Polytope account have access to sub-daily Climate DT data?" — and
# never raises. Output:
#
# * `data/destine/sub_daily/probe.log` — full traceback on failure or
#   `SUCCESS: sub-daily access available` on success.
# * `data/destine/sub_daily/probe.grib` — the tiny sample retrieve (only
#   written on success).
#
# Bounding box: 38°-40°N, 4°W-2°W (~220 km × 175 km over central Iberia).
# Date: 2025-07-15. Variable: 2m temperature, hourly (`time=0000/to/2300/by/0100`).

# %%
SUBDAILY_PROBE_LOG = DESTINE_SUBDAILY_DIR / "probe.log"
SUBDAILY_PROBE_GRIB = DESTINE_SUBDAILY_DIR / "probe.grib"


def polytope_subdaily_probe() -> bool:
    """Probe sub-daily Climate DT access. Always returns a boolean.
    Never raises; logs the full traceback on failure."""
    if not has_polytope_credentials():
        msg = "probe skipped — credentials absent"
        print(f"  [skip  ]  {msg}")
        SUBDAILY_PROBE_LOG.write_text(msg + "\n")
        return False

    # Lazy import inside the try/except so even an import-time failure
    # is logged rather than raised.
    try:
        from polytope.api import Client  # type: ignore

        request = {
            "class": "d1",
            "dataset": "climate-dt",
            "activity": "ScenarioMIP",
            "experiment": "SSP3-7.0",
            "expver": "0001",
            "generation": "1",
            "realization": "1",
            "model": "IFS-NEMO",
            "resolution": "standard",
            "type": "fc",
            "stream": "clte",
            "levtype": "sfc",
            "param": "167",
            "date": "20250715",
            "time": "0000/to/2300/by/0100",   # hourly
            # `area` is N/W/S/E; even though MARS cannot crop HEALPix
            # with a lat/lon bbox in standard retrieves, the probe
            # request shape mirrors what a future high-resolution
            # gridded retrieve would use. If polytope rejects the
            # `area` key it falls through to the except below — that
            # is itself the answer we want.
            "area": "40/-4/38/-2",
        }
        print(f"  [probe ]  hourly t2m over Iberia, 2025-07-15")
        print(f"            request = {request}")
        client = Client(address=POLYTOPE_ADDRESS)
        client.retrieve(
            POLYTOPE_COLLECTION, request,
            output_file=str(SUBDAILY_PROBE_GRIB),
            asynchronous=False,
        )
        if (
            SUBDAILY_PROBE_GRIB.exists()
            and SUBDAILY_PROBE_GRIB.stat().st_size > MIN_PROBE_BYTES
        ):
            msg = (
                f"SUCCESS: sub-daily access available "
                f"({SUBDAILY_PROBE_GRIB.stat().st_size:,} bytes "
                f"-> {SUBDAILY_PROBE_GRIB})"
            )
            print(f"  [ok    ]  {msg}")
            SUBDAILY_PROBE_LOG.write_text(msg + "\n")
            return True
        msg = (
            "FAILURE: polytope returned no error but the output GRIB is "
            f"absent or too small ({SUBDAILY_PROBE_GRIB})"
        )
        print(f"  [fail  ]  {msg}")
        SUBDAILY_PROBE_LOG.write_text(msg + "\n")
        return False
    except Exception:  # noqa: BLE001 — probe must never raise
        tb = traceback.format_exc()
        msg = f"FAILURE: sub-daily probe raised:\n{tb}"
        print(f"  [fail  ]  sub-daily probe raised (see {SUBDAILY_PROBE_LOG})")
        SUBDAILY_PROBE_LOG.write_text(msg)
        return False


print("\n--- 2. Polytope sub-daily probe ---")
subdaily_available = polytope_subdaily_probe()
print(f"  sub-daily available = {subdaily_available}")

SOURCES.append({
    "name": "Polytope sub-daily probe",
    "doi": None,
    "url": POLYTOPE_ADDRESS,
    "license": "DestinE Data Lake terms",
    "accessed_on": date.today().isoformat(),
    "result": "available" if subdaily_available else "unavailable_or_skipped",
    "log_path": str(SUBDAILY_PROBE_LOG.relative_to(ROOT)),
    "sample_path": (
        str(SUBDAILY_PROBE_GRIB.relative_to(ROOT)) if SUBDAILY_PROBE_GRIB.exists() else None
    ),
})


# %% [markdown]
# ## 3. CRU TS 3.24.01 historical T<sub>max</sub>
#
# Provides the historical climatology underpinning the Lacertidae
# Table 1 priors (mean T<sub>max</sub> = 25.6°C). Sinervo et al. 2010
# used WorldClim 1.4 plus the European Climate Assessment for Europe;
# CRU TS 3.24.01 is the closest pre-aggregated gridded product that the
# upstream Bombus chain (`weatherxbiodiversity-projection`) has already
# vendored. We reuse those NetCDFs to keep h_r calibration consistent
# across the chain.
#
# Only `tmx` is strictly needed for h_r; `tmn` is included optionally
# (diurnal-cycle reconstruction in pass 2 if the sub-daily probe fails).
#
# Soroye 2020 figshare deposit: DOI
# [10.6084/m9.figshare.10058340](https://doi.org/10.6084/m9.figshare.10058340).
# If the shared cache is absent and a fresh fetch is needed, the
# notebook downloads the full Bumblebee_repo.zip (~1.1 GB).

# %%
SOROYE_FIGSHARE_API = "https://api.figshare.com/v2/articles/10058340"
SOROYE_FIGSHARE_DOI = "10.6084/m9.figshare.10058340"

CRU_TMX_GLOB = "cru_ts3.24.01.*.tmx.dat.nc"
CRU_TMN_GLOB = "cru_ts3.24.01.*.tmn.dat.nc"


def _collect_cru_files(directory: Path, glob: str) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob(glob))


def fetch_cru_ts() -> Path:
    # Step 1: this repo's own data/cru_ts/ already populated?
    tmx_local = _collect_cru_files(CRU_DIR, CRU_TMX_GLOB)
    if tmx_local and all(p.stat().st_size > MIN_NC_BYTES for p in tmx_local):
        print(f"  [cached]  {len(tmx_local)} tmx NetCDFs already under {CRU_DIR}")
        return CRU_DIR

    # Step 2: shared Bombus-repo extraction.
    tmx_shared = _collect_cru_files(SHARED_CRU_DIR, CRU_TMX_GLOB)
    tmn_shared = _collect_cru_files(SHARED_CRU_DIR, CRU_TMN_GLOB)
    if tmx_shared:
        print(f"  [reuse ]  symlinking {len(tmx_shared)} tmx + {len(tmn_shared)} tmn "
              f"from {SHARED_CRU_DIR} -> {CRU_DIR}")
        for src in tmx_shared + tmn_shared:
            dst = CRU_DIR / src.name
            if dst.exists() or dst.is_symlink():
                dst.unlink()
            try:
                dst.symlink_to(src)
            except OSError:
                shutil.copy2(src, dst)
        return CRU_DIR

    # Step 3: fresh fetch from figshare. The deposit is large (~1.1 GB);
    # do it only if no other path exists.
    print(f"  [fetch ]  no cache found — fetching Soroye figshare deposit")
    print(f"            api: {SOROYE_FIGSHARE_API}")
    r = requests.get(SOROYE_FIGSHARE_API, timeout=120)
    r.raise_for_status()
    meta = r.json()
    files = meta.get("files", [])
    target_file = next(
        (f for f in files if f["name"].lower().startswith("bumblebee")),
        files[0] if files else None,
    )
    if not target_file:
        raise RuntimeError(f"No files in figshare article: {meta}")
    bumblebee_zip = CRU_DIR.parent / "Bumblebee_repo.zip"
    print(f"            resolving {target_file['name']} ({target_file['size']:,} bytes)")
    with requests.get(
        target_file["download_url"], stream=True, timeout=3600, allow_redirects=True
    ) as resp:
        resp.raise_for_status()
        with open(bumblebee_zip, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    print(f"            extracting → {CRU_DIR}")
    with zipfile.ZipFile(bumblebee_zip) as zf:
        for member in zf.namelist():
            if "0_ClimateData/" not in member:
                continue
            name = Path(member).name
            if not name:
                continue
            if not (name.endswith(".tmx.dat.nc") or name.endswith(".tmn.dat.nc")):
                continue
            with zf.open(member) as src, open(CRU_DIR / name, "wb") as dst:
                shutil.copyfileobj(src, dst)
    return CRU_DIR


print("\n--- 3. CRU TS 3.24.01 historical T2M ---")
cru_dir = fetch_cru_ts()
cru_tmx_files = _collect_cru_files(cru_dir, CRU_TMX_GLOB)
cru_tmn_files = _collect_cru_files(cru_dir, CRU_TMN_GLOB)
print(f"  tmx files = {len(cru_tmx_files)}, tmn files = {len(cru_tmn_files)}")

SOURCES.append({
    "name": "CRU TS 3.24.01 — monthly Tmax/Tmin",
    "doi": SOROYE_FIGSHARE_DOI,
    "url": f"https://doi.org/{SOROYE_FIGSHARE_DOI}",
    "license": "CC-BY-4.0 (figshare deposit terms)",
    "accessed_on": date.today().isoformat(),
    "n_tmx_chunks": len(cru_tmx_files),
    "n_tmn_chunks": len(cru_tmn_files),
    "local_path": str(cru_dir.relative_to(ROOT)),
    "reused_from": str(SHARED_CRU_DIR) if SHARED_CRU_DIR.exists() else None,
})


# %% [markdown]
# ## 4. GBIF Lacertidae × Iberia occurrence download (pre-minted via UI)
#
# **Bombus-style pattern (matches `weatherxbiodiversity-projection`):** the
# Lacertidae × Iberia download is minted *out-of-band* via the GBIF web
# UI (one-time, by the user). Once minted, the key and DOI are hardcoded
# in the cell below and the zip is fetched by URL — **no GBIF credentials
# needed at notebook execution time**. This makes the notebook
# reproducible in CI and on fresh checkouts without env-var injection.
#
# Per DOMAIN.md "GBIF download DOIs are mandatory" a *fresh* download is
# minted for the lizards chain (do NOT reuse the Bombus DOI
# `10.15468/dl.3frmsq` — reuse would falsify the lizards data lineage).
#
# **To mint** (one-time, the FIRST time this notebook is set up):
#
#   1. Open the pre-filtered search URL below in a browser.
#   2. Click *Download → Simple* (SIMPLE_CSV).
#   3. Wait for the DOI to be minted (~5-15 min).
#   4. Paste the new download key into `GBIF_DL_KEY` and the new DOI
#      into `GBIF_DL_DOI` below.
#
# **Pre-filtered search URL** (Lacertidae taxonKey 5201, resolved via
# `https://api.gbif.org/v1/species/match?name=Lacertidae&rank=family`):
#
#   https://www.gbif.org/occurrence/search?taxon_key=5201&country=ES&country=PT&country=AD&country=GI&has_coordinate=true&has_geospatial_issue=false&basis_of_record=HUMAN_OBSERVATION&basis_of_record=PRESERVED_SPECIMEN&basis_of_record=MACHINE_OBSERVATION&occurrence_year=1900,2030
#
# **Predicates** (the filters above, restated for the source registry):
#
#   * taxonKey = 5201 (Lacertidae, ACCEPTED, family, class Squamata)
#   * country IN (ES, PT, AD, GI) — Spain, Portugal, Andorra, Gibraltar
#   * hasCoordinate = TRUE
#   * hasGeospatialIssue = FALSE
#   * basisOfRecord IN (HUMAN_OBSERVATION, PRESERVED_SPECIMEN, MACHINE_OBSERVATION)
#   * year >= 1900
#
# Outputs:
#
#   * `data/gbif/lacertidae_iberia.zip` — the fetched SIMPLE_CSV download
#   * `data/gbif/download_doi.txt` — the minted DOI
#   * `data/gbif/download_key.txt` — the GBIF download key (for re-fetch)
#   * `data/gbif/lacertidae_iberia_metadata.json` — full metadata

# %%
# Pre-minted via the GBIF UI on 2026-05-16 by Anne Fouilloux.
# Citation: GBIF.org (16 May 2026) GBIF Occurrence Download
# https://doi.org/10.15468/dl.rh4rfn (193,476 records, SIMPLE/CSV, CC-BY-NC-4.0).
GBIF_DL_KEY = "0021363-260507073636908"
GBIF_DL_DOI = "10.15468/dl.rh4rfn"
GBIF_DL_URL = f"https://api.gbif.org/v1/occurrence/download/request/{GBIF_DL_KEY}.zip"

GBIF_ZIP_PATH = GBIF_DIR / "lacertidae_iberia.zip"
GBIF_DOI_PATH = GBIF_DIR / "download_doi.txt"
GBIF_KEY_PATH = GBIF_DIR / "download_key.txt"
GBIF_META_PATH = GBIF_DIR / "lacertidae_iberia_metadata.json"


def fetch_gbif_lacertidae() -> dict:
    """Fetch the pre-minted Lacertidae × Iberia GBIF download by URL.
    Returns a metadata dict; writes the zip + DOI + key to disk."""
    # Already on disk? Reuse.
    if (
        GBIF_ZIP_PATH.exists()
        and GBIF_ZIP_PATH.stat().st_size > MIN_ZIP_BYTES
        and GBIF_DOI_PATH.exists()
        and GBIF_KEY_PATH.exists()
    ):
        doi = GBIF_DOI_PATH.read_text().strip()
        key = GBIF_KEY_PATH.read_text().strip()
        print(f"  [cached]  download key = {key}")
        print(f"  [cached]  DOI          = {doi}")
        print(f"  [cached]  zip          = {GBIF_ZIP_PATH} "
              f"({GBIF_ZIP_PATH.stat().st_size:,} bytes)")
        return {"key": key, "doi": doi, "zip": str(GBIF_ZIP_PATH)}

    if GBIF_DL_KEY.startswith("TODO_"):
        print(
            "  [skip  ]  GBIF download not yet minted.\n"
            "            Mint via the GBIF web UI (see markdown above),\n"
            "            then paste the new key + DOI into\n"
            "            GBIF_DL_KEY and GBIF_DL_DOI in this cell."
        )
        return {"key": None, "doi": None, "zip": None, "skipped": True}

    # Pre-minted: fetch the zip directly — no credentials needed.
    print(f"  fetching {GBIF_DL_URL}")
    r = requests.get(GBIF_DL_URL, stream=True, timeout=600, allow_redirects=True)
    r.raise_for_status()
    with open(GBIF_ZIP_PATH, "wb") as f:
        for chunk in r.iter_content(chunk_size=1 << 16):
            f.write(chunk)
    print(f"  saved {GBIF_ZIP_PATH} ({GBIF_ZIP_PATH.stat().st_size:,} bytes)")

    GBIF_DOI_PATH.write_text(GBIF_DL_DOI + "\n")
    GBIF_KEY_PATH.write_text(GBIF_DL_KEY + "\n")
    meta = {
        "download_key": GBIF_DL_KEY,
        "doi": GBIF_DL_DOI,
        "doi_url": f"https://doi.org/{GBIF_DL_DOI}",
        "source_url": GBIF_DL_URL,
    }
    GBIF_META_PATH.write_text(json.dumps(meta, indent=2))
    print(f"  DOI          = {GBIF_DL_DOI}")
    return {"key": GBIF_DL_KEY, "doi": GBIF_DL_DOI, "zip": str(GBIF_ZIP_PATH)}


print("\n--- 4. GBIF Lacertidae × Iberia occurrence download (pre-minted) ---")
gbif_result = fetch_gbif_lacertidae()

SOURCES.append({
    "name": "GBIF Lacertidae × Iberia occurrence download (pre-minted)",
    "doi": gbif_result.get("doi"),
    "url": (
        f"https://doi.org/{gbif_result['doi']}"
        if gbif_result.get("doi") else None
    ),
    "license": "CC-BY-NC-4.0 (per individual GBIF datasets)",
    "accessed_on": date.today().isoformat(),
    "download_key": gbif_result.get("key"),
    "predicates": {
        "taxonKey": 5201,
        "taxonKey_resolution": "Lacertidae (family, ACCEPTED) — https://api.gbif.org/v1/species/match?name=Lacertidae&rank=family",
        "country": ["ES", "PT", "AD", "GI"],
        "hasCoordinate": True,
        "hasGeospatialIssue": False,
        "basisOfRecord": [
            "HUMAN_OBSERVATION", "PRESERVED_SPECIMEN", "MACHINE_OBSERVATION",
        ],
        "year_min": 1900,
    },
    "local_path": gbif_result.get("zip"),
    "skipped": gbif_result.get("skipped", False),
})


# %% [markdown]
# ## 5. Source registry
#
# A single JSON file at `data/raw/sources.json` recording every
# download's URL/DOI/license/accessed-on date and any "would fetch" /
# "skipped" status. This file is the provenance contract that the
# Replication Study draft (Phase 5 step 04) cites.

# %%
SOURCES_JSON = RAW_DIR / "sources.json"
with open(SOURCES_JSON, "w") as f:
    json.dump({"sources": SOURCES, "written_on": date.today().isoformat()}, f, indent=2)
print(f"\n--- 5. Wrote source registry → {SOURCES_JSON}")


# %% [markdown]
# ## Summary

# %%
print("\nArtefact inventory:")
artefacts = [
    ("DestinE 2020-2029 t2m GRIB", destine_paths.get("2020_2029")),
    ("DestinE 2030-2039 t2m GRIB", destine_paths.get("2030_2039")),
    ("Sub-daily probe log",        SUBDAILY_PROBE_LOG),
    ("Sub-daily probe sample",     SUBDAILY_PROBE_GRIB),
    ("CRU TS dir",                 cru_dir),
    ("GBIF Lacertidae zip",        GBIF_ZIP_PATH),
    ("GBIF DOI",                   GBIF_DOI_PATH),
    ("GBIF download key",          GBIF_KEY_PATH),
    ("Source registry JSON",       SOURCES_JSON),
]
for name, p in artefacts:
    if p is None:
        print(f"  ----  {name:<32} (not produced)")
        continue
    if p.exists():
        size = (
            p.stat().st_size if p.is_file()
            else sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
        )
        print(f"  ok    {name:<32} {size:>15,} bytes  {p.relative_to(ROOT)}")
    else:
        print(f"  MISS  {name:<32} {'?':>15}        {p.relative_to(ROOT)}")
