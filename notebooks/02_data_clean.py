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
# # 02 — Data clean (Iberian Lacertidae, HEALPix-NESTED nside=128)
#
# Tidies the three raw inputs that pass-1's `01_data_download.py`
# left on disk into analysis-ready intermediates for the h_r mechanism:
#
# 1. **DestinE Climate DT 2 m temperature** (GRIBs at HEALPix-NESTED
#    nside=128, four 6-hourly instantaneous samples per day) →
#    per-cell × per-day Tmax and Tmin time series for Iberia, saved as
#    NetCDF.
# 2. **CRU TS 3.24.01 tmx / tmn** (regular lat-lon, monthly) → climatology
#    means resampled to the same Iberian HEALPix nside=128 cells,
#    serving as the historical reference and as a Tmin fallback for
#    the diurnal-cycle reconstruction in `03_analysis.py`.
# 3. **GBIF Lacertidae × Iberia occurrences** (tab-delimited CSV) →
#    per-species per-cell presence frame on the same nside=128 substrate,
#    saved as Parquet; sensitivity copy at nside=64 via the NESTED
#    bit-shift parent operation.
#
# All artefacts live under `data/intermediate/`. Naming mirrors the
# Bombus sister repo (`weatherxbiodiversity-projection/healpix_port/
# outputs_iberia/`) where the patterns came from — but the on-disk
# data products serve the **Sinervo 2010 h_r mechanism**, not the
# Soroye TEI/PEI GLMM.
#
# Domain conventions enforced (`DOMAIN.md`):
#
# * HEALPix indexing is always **NESTED** — every healpix-geo call
#   passes `depth = log2(NSIDE)`; the NESTED → NESTED parent op is
#   `parent = child >> 2`. RING is never touched.
# * `healpix-geo` (geo-aware, WGS84) — never `healpy`.
# * Intermediate arrays go to **NetCDF** (≤2 GB) or **Parquet** (tabular).
#   No `.npz`. No `pickle`.

# %%
import json
import zipfile
from datetime import date
from pathlib import Path

import eccodes
import numpy as np
import pandas as pd
import xarray as xr
from healpix_geo import nested as hp_nested

# %% [markdown]
# ## Constants
#
# `NSIDE=128` matches the native DestinE IFS-NEMO standard-resolution
# grid (no resampling, just selection). `NSIDE_COARSE=64` is the
# sensitivity substrate (parent of every nside=128 cell via `>> 2`).
# Iberia bbox matches the Bombus sister repo's
# `scripts/precompute_iberia_pix.py` so the cell list is the same.

# %%
NSIDE = 128
DEPTH = 7                          # log2(128)

NSIDE_COARSE = 64
DEPTH_COARSE = 6                   # log2(64)

ELLIPSOID = "WGS84"                # DestinE Climate DT is WGS84-aware

# Iberia bounding box (lon_min, lat_min, lon_max, lat_max).
IBERIA_LON_MIN, IBERIA_LAT_MIN = -10.0, 35.0
IBERIA_LON_MAX, IBERIA_LAT_MAX = 4.0, 44.0

HORIZONS = {
    "2020_2029": "destine_2020_2029_t2m.grib",
    "2030_2039": "destine_2030_2039_t2m.grib",
}

# %%
ROOT = Path("..").resolve()
DATA = ROOT / "data"
DESTINE_RAW = DATA / "destine" / "raw"
CRU_DIR = DATA / "cru_ts"
GBIF_ZIP = DATA / "gbif" / "lacertidae_iberia.zip"
GBIF_DOI_FILE = DATA / "gbif" / "download_doi.txt"

INTERMEDIATE = DATA / "intermediate"
INTERMEDIATE.mkdir(parents=True, exist_ok=True)

DESTINE_OUT = INTERMEDIATE / "destine_iberia_daily_t2m_nside128.nc"
CRU_OUT = INTERMEDIATE / "cru_iberia_monthly_nside128.nc"
GBIF_CSV_EXTRACTED = INTERMEDIATE / "gbif_lacertidae_iberia.csv"
GBIF_PARQUET_128 = INTERMEDIATE / "gbif_lacertidae_presence_nside128.parquet"
GBIF_PARQUET_64 = INTERMEDIATE / "gbif_lacertidae_presence_nside64.parquet"
CLEAN_REPORT = INTERMEDIATE / "clean_report.json"

print(f"ROOT  = {ROOT}")
print(f"NSIDE = {NSIDE} (depth={DEPTH}); coarse NSIDE = {NSIDE_COARSE} (depth={DEPTH_COARSE})")

report: dict = {"written_on": date.today().isoformat()}


# %% [markdown]
# ## Iberian HEALPix-NESTED cell set
#
# Enumerate all 12·nside² global cells, transform centre coordinates
# back to lon/lat, and keep the ones whose centre falls in the Iberia
# bbox. Computed once at each resolution; the nside=128 list is the
# subset key used for both the DestinE GRIB decode and the CRU/GBIF
# alignment. Per the parent invariant
# (`parent = child >> 2`, NESTED only) every nside=128 cell maps to
# exactly one nside=64 parent, so the sensitivity branch needs no
# separate enumeration.

# %%
def iberian_pix(depth: int, nside: int) -> np.ndarray:
    """All NESTED cells at `depth` whose centre falls in the Iberia bbox."""
    pix = np.arange(12 * nside * nside, dtype=np.int64)
    lon, lat = hp_nested.healpix_to_lonlat(pix, depth, ELLIPSOID)
    lon = np.where(lon > 180.0, lon - 360.0, lon)
    mask = (
        (lon >= IBERIA_LON_MIN) & (lon <= IBERIA_LON_MAX)
        & (lat >= IBERIA_LAT_MIN) & (lat <= IBERIA_LAT_MAX)
    )
    return pix[mask]


IBERIA_PIX_128 = iberian_pix(DEPTH, NSIDE)
N_128 = len(IBERIA_PIX_128)
print(f"Iberian nside={NSIDE} cells: {N_128}")

# Centres for the cells we keep — used for the CRU regridding step
# (nearest-neighbour lat-lon → HEALPix centre) and for the lon/lat
# coords on the output NetCDFs.
CELL_LON_128, CELL_LAT_128 = hp_nested.healpix_to_lonlat(
    IBERIA_PIX_128.astype(np.uint64), DEPTH, ELLIPSOID
)
CELL_LON_128 = np.where(CELL_LON_128 > 180.0, CELL_LON_128 - 360.0, CELL_LON_128)

report["iberia"] = {
    "bbox_lon": [IBERIA_LON_MIN, IBERIA_LON_MAX],
    "bbox_lat": [IBERIA_LAT_MIN, IBERIA_LAT_MAX],
    "n_cells_nside128": int(N_128),
}


# %% [markdown]
# ## 1. DestinE GRIB → per-day Tmax / Tmin per Iberian nside=128 cell
#
# The two GRIBs are HEALPix-NESTED nside=128 globally. We decode message
# by message using the eccodes Python API directly (cfgrib's Geoiterator
# is RING-only and would break the NESTED ordering invariant). Each
# message is one 6-hourly instantaneous t2m field. We subset to the
# Iberian cell index at decode time so memory stays bounded.
#
# Daily Tmax/Tmin per cell = max/min over that day's four samples
# (00/06/12/18 UTC). Output: an xarray Dataset with dims
# (`time`, `cell`) saved to NetCDF, ~tens of MB after Iberia masking.

# %%
def stream_grib_iberia(grib_path: Path):
    """Yield (timestamp_day, hhmm, values_iberia_K) per message in `grib_path`.

    Defensive checks on the first message — Nside must be 128 and
    orderingConvention 'nested'; mismatches raise immediately so a
    wrong grid never silently feeds downstream.
    """
    with open(grib_path, "rb") as f:
        first = True
        while True:
            gid = eccodes.codes_grib_new_from_file(f)
            if gid is None:
                break
            try:
                if first:
                    nside_seen = eccodes.codes_get(gid, "Nside")
                    order = eccodes.codes_get(gid, "orderingConvention")
                    if nside_seen != NSIDE:
                        raise RuntimeError(
                            f"GRIB Nside={nside_seen}; expected {NSIDE}"
                        )
                    if order != "nested":
                        raise RuntimeError(
                            f"GRIB orderingConvention={order!r}; expected 'nested'"
                        )
                    first = False
                yyyymmdd = eccodes.codes_get(gid, "dataDate")
                hhmm = eccodes.codes_get(gid, "dataTime")
                values_global = eccodes.codes_get_array(gid, "values")
                vals_iberia = values_global[IBERIA_PIX_128].astype(np.float64, copy=True)
            finally:
                eccodes.codes_release(gid)
            day = pd.Timestamp(
                year=yyyymmdd // 10000,
                month=(yyyymmdd // 100) % 100,
                day=yyyymmdd % 100,
            )
            yield day, hhmm, vals_iberia


def aggregate_daily_t2m(grib_path: Path) -> xr.Dataset:
    """Per-day Tmax/Tmin per Iberian nside=128 cell (in degC)."""
    print(f"  decoding {grib_path.name} ...")
    daily_max: dict[pd.Timestamp, np.ndarray] = {}
    daily_min: dict[pd.Timestamp, np.ndarray] = {}
    daily_n: dict[pd.Timestamp, int] = {}
    n_msgs = 0
    for day, _hhmm, vals in stream_grib_iberia(grib_path):
        if day in daily_max:
            np.maximum(daily_max[day], vals, out=daily_max[day])
            np.minimum(daily_min[day], vals, out=daily_min[day])
            daily_n[day] += 1
        else:
            daily_max[day] = vals.copy()
            daily_min[day] = vals.copy()
            daily_n[day] = 1
        n_msgs += 1
        if n_msgs % 2000 == 0:
            print(f"    {n_msgs:>6} messages, {len(daily_max):>5} days so far")
    print(f"    decoded {n_msgs} messages -> {len(daily_max)} days")
    days = sorted(daily_max.keys())
    tmax = np.stack([daily_max[d] for d in days], axis=0) - 273.15
    tmin = np.stack([daily_min[d] for d in days], axis=0) - 273.15
    return xr.Dataset(
        data_vars={
            "tmax_daily": (("time", "cell"), tmax.astype(np.float32),
                           {"units": "degC",
                            "long_name": "daily Tmax (max of 6-hourly samples)"}),
            "tmin_daily": (("time", "cell"), tmin.astype(np.float32),
                           {"units": "degC",
                            "long_name": "daily Tmin (min of 6-hourly samples)"}),
        },
        coords={
            "time": pd.DatetimeIndex(days),
            "cell": ("cell", IBERIA_PIX_128.astype(np.int64),
                     {"long_name": f"HEALPix NESTED pixel index (nside={NSIDE})"}),
            "lon": ("cell", CELL_LON_128.astype(np.float32),
                    {"units": "degrees_east", "long_name": "cell-centre longitude"}),
            "lat": ("cell", CELL_LAT_128.astype(np.float32),
                    {"units": "degrees_north", "long_name": "cell-centre latitude"}),
        },
    )


print("\n--- 1. DestinE GRIB -> daily Tmax/Tmin per Iberian cell ---")
ds_parts = []
for horizon, grib_name in HORIZONS.items():
    grib_path = DESTINE_RAW / grib_name
    if not grib_path.exists():
        raise FileNotFoundError(f"Expected DestinE GRIB at {grib_path}")
    ds_h = aggregate_daily_t2m(grib_path)
    ds_h.attrs["horizon"] = horizon
    ds_parts.append(ds_h)
ds_destine = xr.concat(ds_parts, dim="time")
ds_destine.attrs.update({
    "title": "Iberian daily Tmax/Tmin from DestinE Climate DT (nside=128 NESTED)",
    "source": "DestinE Climate DT SSP3-7.0 IFS-NEMO standard, param 167 (2t)",
    "history": (
        f"Created {date.today().isoformat()} by notebooks/02_data_clean.py "
        f"(eccodes-direct decode -> subset {N_128} Iberian cells -> daily max/min "
        "across 6-hourly samples)"
    ),
    "Conventions": "CF-1.10",
    "ellipsoid": ELLIPSOID,
    "healpix_ordering": "NESTED",
    "healpix_nside": NSIDE,
})
encoding = {v: {"zlib": True, "complevel": 4} for v in ds_destine.data_vars}
ds_destine.to_netcdf(DESTINE_OUT, engine="netcdf4", encoding=encoding)
size_mb = DESTINE_OUT.stat().st_size / 1e6
print(f"  saved {DESTINE_OUT}  ({size_mb:,.1f} MB)")
report["destine"] = {
    "output": str(DESTINE_OUT.relative_to(ROOT)),
    "n_days": int(ds_destine.sizes["time"]),
    "n_cells": int(ds_destine.sizes["cell"]),
    "tmax_global_min_max_degC": [
        float(ds_destine["tmax_daily"].min().values),
        float(ds_destine["tmax_daily"].max().values),
    ],
    "size_mb": round(size_mb, 1),
}


# %% [markdown]
# ## 2. CRU TS tmx / tmn → monthly climatology resampled to nside=128
#
# Loads all decade chunks of CRU TS 3.24.01 (1901-2015) for both `tmx`
# and `tmn`, restricts to the Iberia bbox in lat/lon space, then samples
# each variable at the HEALPix nside=128 cell centre via nearest-
# neighbour. This serves three downstream needs:
#
# * Historical reference for the Iberian climate
#   (mean Tmax 1971-2000 etc).
# * Tmin source for the **sinusoidal diurnal-cycle reconstruction**
#   used in `03_analysis.py` when the DestinE sub-daily probe failed —
#   we use CRU monthly tmn climatology rather than the DestinE-derived
#   daily Tmin to keep the diurnal range consistent with the
#   historical baseline.
# * Per-month Iberian climatology for figure annotations.

# %%
def load_cru(directory: Path, var: str) -> xr.DataArray:
    """Open all decade chunks of one CRU variable, restricted to Iberia."""
    files = sorted(directory.glob(f"cru_ts3.24.01.*.{var}.dat.nc"))
    if not files:
        raise FileNotFoundError(f"No CRU TS {var} files in {directory}")
    parts = []
    for fp in files:
        ds = xr.open_dataset(fp)
        sub = ds[var].sel(
            lon=slice(IBERIA_LON_MIN - 0.5, IBERIA_LON_MAX + 0.5),
            lat=slice(IBERIA_LAT_MIN - 0.5, IBERIA_LAT_MAX + 0.5),
        )
        parts.append(sub.load())
        ds.close()
    return xr.concat(parts, dim="time").sortby("time")


def cru_to_healpix(da: xr.DataArray) -> np.ndarray:
    """Nearest-neighbour sample of `da(time, lat, lon)` at HEALPix cell centres.

    Returns array of shape (n_time, N_128). Nearest-neighbour is the
    correct choice for a 0.5-degree CRU grid sampled onto ~0.5-degree
    HEALPix cells at nside=128 (cell width ~50 km) — bilinear adds
    smoothing that obscures local climate gradients which the h_r
    threshold is sensitive to.
    """
    sampled = da.sel(
        lon=xr.DataArray(CELL_LON_128, dims="cell"),
        lat=xr.DataArray(CELL_LAT_128, dims="cell"),
        method="nearest",
    )
    return sampled.values.astype(np.float32)


print("\n--- 2. CRU TS -> monthly Iberia at HEALPix nside=128 ---")
cru_tmx = load_cru(CRU_DIR, "tmx")
cru_tmn = load_cru(CRU_DIR, "tmn")
print(f"  tmx: {cru_tmx.shape}, time {cru_tmx.time.values[0]} .. {cru_tmx.time.values[-1]}")
print(f"  tmn: {cru_tmn.shape}, time {cru_tmn.time.values[0]} .. {cru_tmn.time.values[-1]}")

tmx_hp = cru_to_healpix(cru_tmx)
tmn_hp = cru_to_healpix(cru_tmn)
ds_cru = xr.Dataset(
    data_vars={
        "tmx": (("time", "cell"), tmx_hp,
                {"units": "degC",
                 "long_name": "monthly mean of daily max T from CRU TS"}),
        "tmn": (("time", "cell"), tmn_hp,
                {"units": "degC",
                 "long_name": "monthly mean of daily min T from CRU TS"}),
    },
    coords={
        "time": cru_tmx["time"].values,
        "cell": ("cell", IBERIA_PIX_128.astype(np.int64),
                 {"long_name": f"HEALPix NESTED pixel index (nside={NSIDE})"}),
        "lon": ("cell", CELL_LON_128.astype(np.float32),
                {"units": "degrees_east"}),
        "lat": ("cell", CELL_LAT_128.astype(np.float32),
                {"units": "degrees_north"}),
    },
    attrs={
        "title": "CRU TS 3.24.01 tmx/tmn resampled to Iberian HEALPix nside=128",
        "source": "CRU TS 3.24.01 (figshare 9956471) at 0.5deg lat-lon",
        "regrid_method": "nearest-neighbour at HEALPix cell centre",
        "history": (
            f"Created {date.today().isoformat()} by notebooks/02_data_clean.py"
        ),
        "Conventions": "CF-1.10",
        "ellipsoid": ELLIPSOID,
        "healpix_ordering": "NESTED",
        "healpix_nside": NSIDE,
    },
)
ds_cru.to_netcdf(
    CRU_OUT, engine="netcdf4",
    encoding={v: {"zlib": True, "complevel": 4} for v in ds_cru.data_vars},
)
print(f"  saved {CRU_OUT}  ({CRU_OUT.stat().st_size / 1e6:.1f} MB)")
report["cru"] = {
    "output": str(CRU_OUT.relative_to(ROOT)),
    "n_months": int(ds_cru.sizes["time"]),
    "n_cells": int(ds_cru.sizes["cell"]),
}


# %% [markdown]
# ## 3. GBIF Lacertidae × Iberia → per-species presence on nside=128
#
# The pre-minted GBIF zip is unpacked once (idempotent). Tab-delimited
# CSV; relevant columns: `species`, `decimalLatitude`, `decimalLongitude`,
# `year`, `gbifID`, `basisOfRecord`. We:
#
# 1. Drop rows with missing species / coordinates.
# 2. Restrict to the Iberia bbox (the GBIF download was already filtered
#    to ES/PT/AD/GI, but a bbox guard removes the rare overseas-territory
#    point that slipped through).
# 3. Assign each occurrence to an nside=128 HEALPix NESTED cell via
#    `healpix_geo.nested.lonlat_to_healpix`.
# 4. Aggregate to a per-(species, cell) presence frame with record
#    counts. Saved as Parquet (tabular intermediate, per `DOMAIN.md`).

# %%
def extract_gbif_csv() -> Path:
    """Unpack the cached GBIF zip into a single CSV under data/intermediate/."""
    if GBIF_CSV_EXTRACTED.exists():
        return GBIF_CSV_EXTRACTED
    with zipfile.ZipFile(GBIF_ZIP) as zf:
        candidates = [n for n in zf.namelist() if n.endswith(".csv")]
        if not candidates:
            raise RuntimeError(f"No CSV inside {GBIF_ZIP}")
        member = candidates[0]
        print(f"  extracting {member} from {GBIF_ZIP.name}")
        with zf.open(member) as src, open(GBIF_CSV_EXTRACTED, "wb") as dst:
            dst.write(src.read())
    return GBIF_CSV_EXTRACTED


print("\n--- 3. GBIF Lacertidae x Iberia -> per-species presence ---")
csv_path = extract_gbif_csv()
gbif = pd.read_csv(
    csv_path,
    sep="\t",
    usecols=[
        "gbifID", "species", "decimalLatitude", "decimalLongitude",
        "year", "basisOfRecord", "countryCode",
    ],
    dtype={"gbifID": "Int64", "year": "Int64", "countryCode": "string"},
    low_memory=False,
)
print(f"  raw rows: {len(gbif):,}")
gbif = gbif.dropna(subset=["species", "decimalLatitude", "decimalLongitude"]).copy()
print(f"  after dropna(species, lat, lon): {len(gbif):,}")

lon = gbif["decimalLongitude"].astype(float).values
lat = gbif["decimalLatitude"].astype(float).values
in_bbox = (
    (lon >= IBERIA_LON_MIN) & (lon <= IBERIA_LON_MAX)
    & (lat >= IBERIA_LAT_MIN) & (lat <= IBERIA_LAT_MAX)
)
gbif = gbif.iloc[in_bbox].copy()
print(f"  after Iberia bbox filter:     {len(gbif):,}")

# HEALPix nside=128 NESTED cell assignment via healpix-geo.
gbif["cell_id_nside128"] = hp_nested.lonlat_to_healpix(
    gbif["decimalLongitude"].astype(float).values,
    gbif["decimalLatitude"].astype(float).values,
    DEPTH,
    ELLIPSOID,
).astype(np.int64)

# Restrict to cells that fall inside the Iberian HEALPix set (the bbox
# at lon/lat space and the bbox at HEALPix-centre space don't perfectly
# coincide for cells straddling the bbox edge).
iberian_set_128 = set(IBERIA_PIX_128.tolist())
gbif = gbif[gbif["cell_id_nside128"].isin(iberian_set_128)].copy()
print(f"  after Iberian HEALPix-cell filter: {len(gbif):,}")

# Per-species per-cell presence (record count).
presence = (
    gbif.groupby(["species", "cell_id_nside128"], as_index=False)
        .agg(n_records=("gbifID", "count"),
             first_year=("year", "min"),
             last_year=("year", "max"))
)
presence.to_parquet(GBIF_PARQUET_128, index=False)
print(f"  saved {GBIF_PARQUET_128}  ({GBIF_PARQUET_128.stat().st_size / 1e6:.2f} MB)")
print(f"  species: {presence['species'].nunique()}, "
      f"cells with >=1 record: {presence['cell_id_nside128'].nunique()}")

# Sensitivity: nside=64 parents — pure bit-shift, no re-projection.
presence_64 = presence.copy()
presence_64["cell_id_nside64"] = (
    presence_64["cell_id_nside128"].astype(np.int64).values >> 2
)
presence_64 = (
    presence_64.groupby(["species", "cell_id_nside64"], as_index=False)
               .agg(n_records=("n_records", "sum"),
                    first_year=("first_year", "min"),
                    last_year=("last_year", "max"))
)
presence_64.to_parquet(GBIF_PARQUET_64, index=False)
print(f"  saved {GBIF_PARQUET_64}  ({GBIF_PARQUET_64.stat().st_size / 1e6:.2f} MB)")

# Per-species record counts — referenced by the rare-species `low_N`
# flag in `03_analysis.py`.
species_counts = (
    presence.groupby("species")
            .agg(n_cells=("cell_id_nside128", "nunique"),
                 n_records=("n_records", "sum"))
            .sort_values("n_records", ascending=False)
)
print("\n  top 10 species by record count:")
print(species_counts.head(10).to_string())
print("\n  bottom 10 species by record count:")
print(species_counts.tail(10).to_string())

gbif_doi = GBIF_DOI_FILE.read_text().strip() if GBIF_DOI_FILE.exists() else None
report["gbif"] = {
    "doi": gbif_doi,
    "n_records_after_clean": int(len(gbif)),
    "n_species": int(presence["species"].nunique()),
    "n_cells_nside128_with_records": int(presence["cell_id_nside128"].nunique()),
    "n_cells_nside64_with_records": int(presence_64["cell_id_nside64"].nunique()),
    "parquet_nside128": str(GBIF_PARQUET_128.relative_to(ROOT)),
    "parquet_nside64": str(GBIF_PARQUET_64.relative_to(ROOT)),
}


# %% [markdown]
# ## 4. Clean report — counts that pass-3 will sanity-check against

# %%
with open(CLEAN_REPORT, "w") as f:
    json.dump(report, f, indent=2, default=str)
print(f"\n--- Clean report -> {CLEAN_REPORT}")
print(json.dumps(report, indent=2, default=str))
