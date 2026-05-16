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
# # 03 — Analysis: Sinervo 2010 h_r mechanism for Iberian Lacertidae
#
# Computes per-cell × per-day **hours of activity restriction** `h_r`
# from SOM Equation S2:
#
#     h_r = max(0, 0.74 × (T_max − T_b) + 6.1)
#
# over the **April–May critical reproductive window** for Iberian
# Lacertidae. A cell is flagged as **locally extinct** in a given year
# if its critical-period h_r exceeds the family-level threshold
# `h̄_r,Lacertidae = 3.1 h` (Table 1 of Sinervo et al. 2010). The
# headline statistic is the fraction of cells per species that exceed
# the threshold in the 2020s and 2030s decades, propagated through the
# GBIF Lacertidae presence frame.
#
# **Methodological deviations from the original paper** (carried into
# the Phase 5 Replication Study draft):
#
# 1. *Climate forcing.* DestinE Climate DT SSP3-7.0 IFS-NEMO at
#    HEALPix nside=128 (~50 km cell width) in 2020-2039, vs Sinervo's
#    WorldClim 1.4 at 10 arc-minute resolution under CCCMA/HADCM3/CSIRO
#    a2a for 1975/2020/2050/2080. Horizon mismatch: Sinervo's headline
#    numbers (6 % global species extinction by 2050, 20 % by 2080) are
#    not directly reachable from DestinE; we report 2020s and 2030s as
#    the lower-horizon transferability test.
# 2. *Thermal-physiology priors.* Family-level Table 1 values
#    (`T_b = 35.4 degC`, `h̄_r = 3.1 h`). Iberian-specific T_b records
#    from Carretero / Monasterio / Spanish herpetological literature
#    are *deferred* to a v0.2.0 iteration — see project README.
# 3. *Reproductive window.* April–May (61 days). Sinervo's SOM
#    page 4 reports March–April for the Sceloporus Mexican calibration
#    ("March and April provided the best fit for both reproductive
#    modes") and says "2 months in the temperate zone" for the global
#    projection; April–May matches typical Iberian Podarcis /
#    Iberolacerta / Timon breeding chronology. **This window is a
#    judgement call** by the replication author; the alternative
#    March–April branch is parameterised below.
# 4. *Diurnal-cycle reconstruction.* DestinE only delivers four
#    6-hourly instantaneous T2m samples per day. The h_r model is a
#    function of daily Tmax already (per Equation S2), so the daily
#    Tmax produced in `02_data_clean.py` is the direct input — no
#    diurnal-cycle reconstruction is needed for the headline statistic.
#    The Tmin field is preserved in the intermediate for downstream
#    sub-daily-probe-successful runs.
#
# **Honest scope** (`DOMAIN.md` § biodiversity is high-precision):
#
# * Per-species local-extinction rates for **rare species (cells < 10)**
#   are grid-coupled (Lobo et al. 2007, Hurlbert & Jetz 2007). The
#   per-species CSV surfaces a `low_N_warning` flag — interpret
#   low-N species cautiously.
# * The h_r mechanism is **the Sinervo 2010 mechanism**, not a
#   novelty of this replication. The novelty is the cross-taxon
#   transfer + DestinE forcing + FAIR chain.

# %%
import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

# %% [markdown]
# ## Constants — Sinervo Table 1 Lacertidae

# %%
T_B_LACERTIDAE = 35.4              # degC, family mean preferred body T
H_R_THRESHOLD_LACERTIDAE = 3.1     # h, calibrated activity-restriction threshold

CRITICAL_MONTHS = (4, 5)           # April–May (61 days, temperate window)

# SOM Equation S2 coefficients.
SLOPE = 0.74
INTERCEPT = 6.1

# Rare-species flag threshold (DOMAIN.md grid-coupling caveat).
LOW_N_CELL_THRESHOLD = 10

DECADES = {
    "2020s": (2020, 2029),
    "2030s": (2030, 2039),
}

# %%
ROOT = Path("..").resolve()
INTERMEDIATE = ROOT / "data" / "intermediate"
RESULTS = ROOT / "results"
RESULTS_TABLES = RESULTS / "tables"
RESULTS_TABLES.mkdir(parents=True, exist_ok=True)
(RESULTS / "logs").mkdir(parents=True, exist_ok=True)

DESTINE_NC = INTERMEDIATE / "destine_iberia_daily_t2m_nside128.nc"
GBIF_PARQUET = INTERMEDIATE / "gbif_lacertidae_presence_nside128.parquet"
SUBDAILY_PROBE_LOG = ROOT / "data" / "destine" / "sub_daily" / "probe.log"

EXTINCTION_MASK_NC = INTERMEDIATE / "extinction_mask_nside128.nc"
HR_PER_CELL_NC = INTERMEDIATE / "hr_per_cell_year_nside128.nc"
PER_SPECIES_CSV = RESULTS_TABLES / "local_extinction_per_species.csv"
HEADLINE_JSON = RESULTS / "headline.json"

# %% [markdown]
# ## Sub-daily availability check
#
# Pass-1 `01_data_download.py` left a marker at
# `data/destine/sub_daily/probe.log`. If it contains "SUCCESS" we
# *could* use real hourly T(t); for this pass the brief locks the
# sinusoidal-fallback decision (locked decision 3). Because Equation S2
# is parameterised in *daily Tmax* — not in an hourly integral —
# the daily Tmax is the direct input regardless of the probe. The
# probe outcome is logged below for the Phase 5 deviations field.

# %%
probe_text = (
    SUBDAILY_PROBE_LOG.read_text().strip()
    if SUBDAILY_PROBE_LOG.exists() else "probe log absent"
)
subdaily_success = probe_text.startswith("SUCCESS")
print(f"Sub-daily probe status: {'SUCCESS' if subdaily_success else 'unavailable'}")
print(f"  message: {probe_text!r}")

# %% [markdown]
# ## Load DestinE daily Tmax + GBIF presence

# %%
print(f"\nLoading {DESTINE_NC}")
ds = xr.open_dataset(DESTINE_NC)
print(f"  dims: {dict(ds.sizes)}")
print(f"  time: {pd.Timestamp(ds.time.values[0]).date()} .. "
      f"{pd.Timestamp(ds.time.values[-1]).date()}")

tmax_daily = ds["tmax_daily"]       # (time, cell), degC
cells = ds["cell"].values.astype(np.int64)
n_cells = cells.size

print(f"\nLoading {GBIF_PARQUET}")
presence = pd.read_parquet(GBIF_PARQUET)
print(f"  rows: {len(presence):,}, species: {presence['species'].nunique()}, "
      f"cells: {presence['cell_id_nside128'].nunique()}")

# Sanity: every presence cell must be in the DestinE cell list.
cells_set = set(cells.tolist())
unknown_cells = set(presence["cell_id_nside128"]) - cells_set
if unknown_cells:
    print(f"  WARNING: {len(unknown_cells)} presence cells absent from DestinE grid "
          f"(will be dropped from extinction calculation)")
    presence = presence[presence["cell_id_nside128"].isin(cells_set)].copy()


# %% [markdown]
# ## Compute h_r per cell × per day (Equation S2)
#
# `h_r(cell, day) = (0.74 × (Tmax_daily − T_b) + 6.1)  if  Tmax_daily > T_b`
# `                 0                                    otherwise`
#
# Vectorised in xarray. The conditional clamping follows Sinervo SOM
# Equation S2 (pages 3-4). The bracket notation `h_r[T_e > T_b_preferred]`
# in the SOM is a *conditional*: h_r is the cumulative hours per day when
# operative temperature exceeds preferred body temperature. When daily
# T_max ≤ T_b the lizard does not need refuge, so h_r = 0 for that day.
# The regression intercept (6.1 h) is meaningful only in the regime where
# T_max > T_b — extrapolating below T_b would produce spurious positive
# h_r in the warm-but-tolerable range (T_b − 8.24°C < T_max < T_b), an
# implementation pitfall caught when Pass 2's first headline came out
# ~10× too high relative to the Sinervo Table 1 Lacertidae 2050 reference.

# %%
print("\n--- Computing h_r per cell x per day (Equation S2) ---")
h_r_daily = xr.apply_ufunc(
    lambda t: np.where(
        t > T_B_LACERTIDAE,
        SLOPE * (t - T_B_LACERTIDAE) + INTERCEPT,
        0.0,
    ),
    tmax_daily,
    dask="allowed",
).rename("h_r_daily")
h_r_daily.attrs.update({
    "units": "hours",
    "long_name": "daily hours of activity restriction (Sinervo SOM Eq. S2)",
    "T_b_used_degC": T_B_LACERTIDAE,
    "formula": (
        f"({SLOPE} * (Tmax - T_b) + {INTERCEPT}) if Tmax > T_b else 0"
    ),
})


# %% [markdown]
# ## Restrict to the reproductive window and aggregate per year
#
# Two statistics are derived per cell × per year, both indexed on the
# 61-day April-May window:
#
# * **`h_r_mean_critical`** — mean of daily h_r over April-May. **This is
#   the headline statistic.** Sinervo SOM page 4: *"a value of h_r = 3.85 h
#   provides the best fit … h_r = 3.85 h during critical reproductive
#   periods may be general for heliothermic Sceloporus species"* — the
#   threshold is the *typical daily restriction hours during the critical
#   period*, calibrated per family. Lacertidae threshold = 3.1 h (paper
#   Table 1).
# * **`h_r_sum_critical`** — sum over April-May, preserved for a
#   sensitivity reading. Save side-by-side so a follow-up can swap
#   interpretations without recomputation.

# %%
print("\n--- Aggregating h_r over April-May per year ---")
months = pd.DatetimeIndex(h_r_daily["time"].values).month
window_mask = np.isin(months, list(CRITICAL_MONTHS))
print(f"  critical-window days kept: {int(window_mask.sum())} "
      f"of {len(months)} total days")

h_r_window = h_r_daily.isel(time=window_mask)
window_year_da = h_r_window["time"].dt.year

h_r_per_year_sum = (
    h_r_window.groupby(window_year_da.rename("year"))
              .sum(dim="time")
              .rename("h_r_sum_critical")
)
h_r_per_year_mean = (
    h_r_window.groupby(window_year_da.rename("year"))
              .mean(dim="time")
              .rename("h_r_mean_critical")
)
print(f"  h_r_sum_critical:  {h_r_per_year_sum.shape}, range "
      f"{float(h_r_per_year_sum.min()):.2f} .. {float(h_r_per_year_sum.max()):.2f} h "
      f"(mean {float(h_r_per_year_sum.mean()):.2f})")
print(f"  h_r_mean_critical: {h_r_per_year_mean.shape}, range "
      f"{float(h_r_per_year_mean.min()):.3f} .. {float(h_r_per_year_mean.max()):.3f} h")


# %% [markdown]
# ## Threshold comparison: cell-year extinction mask
#
# `extinct = h_r_mean_critical > 3.1 h` — per Sinervo SOM page 4, the
# family-calibrated threshold is the typical daily h_r during the
# critical reproductive period, not a cumulative-over-the-window total.

# %%
extinction_mask = (h_r_per_year_mean > H_R_THRESHOLD_LACERTIDAE).rename("extinct")
extinction_mask.attrs.update({
    "long_name": "Cell-year flag: h_r_mean_critical > h_r threshold (Lacertidae)",
    "threshold_h": H_R_THRESHOLD_LACERTIDAE,
})

frac_extinct_year = extinction_mask.mean(dim="cell")
print("\nFraction of Iberian cells exceeding threshold, per year:")
print(pd.DataFrame({
    "year": frac_extinct_year["year"].values,
    "frac": frac_extinct_year.values.round(3),
}).to_string(index=False))

ds_out = xr.Dataset(
    data_vars={
        "h_r_sum_critical": h_r_per_year_sum.astype(np.float32),
        "h_r_mean_critical": h_r_per_year_mean.astype(np.float32),
        "extinct": extinction_mask.astype(np.int8),
    },
    coords={
        "year": h_r_per_year_sum["year"].values,
        "cell": ("cell", cells,
                 {"long_name": "HEALPix NESTED pixel index (nside=128)"}),
        "lon": ("cell", ds["lon"].values),
        "lat": ("cell", ds["lat"].values),
    },
    attrs={
        "title": "Per-cell x per-year h_r and extinction mask (Iberian Lacertidae)",
        "history": (
            f"Created {date.today().isoformat()} by notebooks/03_analysis.py"
        ),
        "T_b_used_degC": T_B_LACERTIDAE,
        "h_r_threshold_h": H_R_THRESHOLD_LACERTIDAE,
        "critical_months": list(CRITICAL_MONTHS),
        "subdaily_probe_status": "SUCCESS" if subdaily_success else "unavailable",
        "Conventions": "CF-1.10",
    },
)
ds_out.to_netcdf(
    EXTINCTION_MASK_NC, engine="netcdf4",
    encoding={v: {"zlib": True, "complevel": 4} for v in ds_out.data_vars},
)
print(f"\nSaved {EXTINCTION_MASK_NC}  "
      f"({EXTINCTION_MASK_NC.stat().st_size / 1e6:.2f} MB)")


# %% [markdown]
# ## Per-species local-extinction rate per decade
#
# For each species in the GBIF presence frame: fraction of its presence
# cells that are flagged extinct in each decade (decadal mean of
# per-year extinction flags within the decade).

# %%
print("\n--- Per-species local-extinction rate per decade ---")
decade_means = {}
for label, (y_start, y_end) in DECADES.items():
    sel = (extinction_mask["year"] >= y_start) & (extinction_mask["year"] <= y_end)
    # Per-cell decadal frequency of being above threshold.
    decade_means[label] = (
        extinction_mask.isel(year=sel)
                       .mean(dim="year")
                       .astype(np.float32)
    )

# Build per-cell DataFrame for the merge.
per_cell_df = pd.DataFrame({
    "cell_id_nside128": cells,
    **{
        f"extinction_freq_{label}": decade_means[label].values
        for label in DECADES
    },
})

# Merge presence (species x cell) with per-cell decadal frequencies.
joined = presence.merge(per_cell_df, on="cell_id_nside128", how="left")

per_species = (
    joined.groupby("species")
          .agg(
              n_cells=("cell_id_nside128", "nunique"),
              n_records=("n_records", "sum"),
              **{
                  f"local_ext_{label}": (f"extinction_freq_{label}", "mean")
                  for label in DECADES
              },
          )
          .reset_index()
          .sort_values("species")
)
per_species["low_N_warning"] = per_species["n_cells"] < LOW_N_CELL_THRESHOLD
per_species.to_csv(PER_SPECIES_CSV, index=False)
print(f"Saved {PER_SPECIES_CSV}")
print(per_species.round(4).to_string(index=False))


# %% [markdown]
# ## Aggregate family-wide Lacertidae rate (baseline config)
#
# Aggregate across species, weighting by number of presence cells. This
# is the family-level baseline (single config: family-mean T_b = 35.4 °C,
# April-May window). The sensitivity-matrix section below cross-products
# this against alternative T_b and window choices.

# %%
# Cells where ≥1 Lacertidae species was recorded — the "Lacertidae cell
# universe" for Iberia. Local extinction is the fraction of those cells
# above threshold (decadal mean), which matches the Sinervo Table 1
# semantics of "local extinction = fraction of populations lost".
presence_cells = sorted(presence["cell_id_nside128"].unique().tolist())
print(f"\nLacertidae cell universe: {len(presence_cells)} cells "
      f"(of {n_cells} Iberian HEALPix cells)")

family_rates: dict[str, float] = {}
for label in DECADES:
    sel = extinction_mask["cell"].isin(presence_cells)
    rate = float(
        decade_means[label]
        .isel(cell=sel)
        .mean()
        .values
    )
    family_rates[f"local_extinction_{label}"] = rate
    print(f"  Lacertidae local-extinction rate, {label}: {rate:.4f}")

# Reference values from Sinervo Table 1.
sinervo_reference = {
    "lacertidae_local_extinction_2009": 0.034,
    "lacertidae_local_extinction_2050": 0.241,
    "lacertidae_local_extinction_2080": 0.460,
}
print("\nReference (Sinervo et al. 2010 Table 1, Lacertidae):")
for k, v in sinervo_reference.items():
    print(f"  {k}: {v}")
print("Note: 2020s and 2030s horizons are not directly comparable to "
      "Sinervo's 2009/2050/2080 timepoints; reported here for context.")

# %% [markdown]
# ## Sensitivity matrix — prior-conditional mechanism applicability
#
# The baseline result uses family-mean Lacertidae priors (T_b = 35.4 °C
# from Table 1) and an April-May reproductive window. This section
# stress-tests the headline against two defensible lizard-biology
# alternatives:
#
# - **T_b shift**: family-mean (35.4 °C) vs Iberolacerta-style cool-adapted
#   (31 °C). Pyrenean endemics (*I. aranica*, *I. bonnali*, *I. galani*)
#   sit closer to 31 °C; warm-adapted *Timon lepidus* / *Podarcis algirus*
#   sit closer to 36 °C. The family mean is dominated by boreal
#   *L. vivipara* at the low end.
# - **Reproductive window shift**: April-May (default, conservative) vs
#   May-June (Iberian *Podarcis* / *Iberolacerta* actual breeding
#   chronology, warmer) vs April-June (extended, includes the cool April
#   days that dilute the mean).
#
# Reports six configurations: baseline + 5 single- and compound-axis
# perturbations. This is bake-the-matrix-into-the-Outcome work that the
# brief locked — the cross-product surfaces the mechanism's
# prior-conditional behaviour that the source paper's single 24 % / 2050
# figure does not.

# %%
print("\n--- Sensitivity matrix: prior-conditional mechanism applicability ---")


def _h_r_extinction_rates(t_b: float, months: tuple[int, ...]) -> dict:
    """Compute Lacertidae local-extinction rates under (T_b, window) config.

    Returns decadal 2020s / 2030s rates restricted to Lacertidae presence
    cells, plus the worst-cell-year h_r_mean value reached.
    """
    hr_daily_c = xr.where(
        tmax_daily > t_b,
        SLOPE * (tmax_daily - t_b) + INTERCEPT,
        0.0,
    )
    months_arr = pd.DatetimeIndex(hr_daily_c["time"].values).month
    window_c = np.isin(months_arr, list(months))
    hr_window_c = hr_daily_c.isel(time=window_c)
    yr_da = hr_window_c["time"].dt.year
    hr_mean_c = (
        hr_window_c.groupby(yr_da.rename("year")).mean(dim="time")
    )
    extinct_c = hr_mean_c > H_R_THRESHOLD_LACERTIDAE
    cell_mask = np.isin(hr_mean_c["cell"].values, presence_cells)
    extinct_lac = extinct_c.isel(cell=cell_mask)
    hr_mean_lac = hr_mean_c.isel(cell=cell_mask)
    yrs_arr = extinct_lac["year"].values
    d20 = float(
        extinct_lac.isel(year=(yrs_arr >= 2020) & (yrs_arr < 2030))
        .mean(dim=("year", "cell"))
    )
    d30 = float(
        extinct_lac.isel(year=(yrs_arr >= 2030) & (yrs_arr < 2040))
        .mean(dim=("year", "cell"))
    )
    return {
        "t_b_degC": t_b,
        "months": list(months),
        "local_extinction_2020s": d20,
        "local_extinction_2030s": d30,
        "max_h_r_mean_h": float(hr_mean_lac.max()),
        "n_cell_years_above_threshold": int((hr_mean_lac > H_R_THRESHOLD_LACERTIDAE).sum()),
    }


sensitivity_configs = [
    ("baseline_family_aprmay",  35.4, (4, 5)),
    ("s1a_family_mayjun",       35.4, (5, 6)),
    ("s1b_family_aprjun",       35.4, (4, 5, 6)),
    ("s2_iberolacerta_aprmay",  31.0, (4, 5)),
    ("s3a_iberolacerta_mayjun", 31.0, (5, 6)),
    ("s3b_iberolacerta_aprjun", 31.0, (4, 5, 6)),
]
sensitivity_matrix = {
    name: _h_r_extinction_rates(t_b, months)
    for name, t_b, months in sensitivity_configs
}
print(f"{'CONFIG':30s}  2020s    2030s    max_h_r   n_above")
print("-" * 80)
for name, row in sensitivity_matrix.items():
    print(
        f"{name:30s}  "
        f"{row['local_extinction_2020s']*100:5.2f}%   "
        f"{row['local_extinction_2030s']*100:5.2f}%   "
        f"{row['max_h_r_mean_h']:5.2f}h   "
        f"{row['n_cell_years_above_threshold']}"
    )


# %% [markdown]
# ## Headline numbers — Lacertidae-wide rate (baseline) + sensitivity matrix

# %%
headline = {
    "written_on": date.today().isoformat(),
    "config": {
        "T_b_degC": T_B_LACERTIDAE,
        "h_r_threshold_h": H_R_THRESHOLD_LACERTIDAE,
        "critical_months": list(CRITICAL_MONTHS),
        "subdaily_probe_status": "SUCCESS" if subdaily_success else "unavailable",
        "n_iberian_cells_nside128": int(n_cells),
        "n_lacertidae_presence_cells": int(len(presence_cells)),
        "n_species": int(presence["species"].nunique()),
    },
    "lacertidae_family_rates_destine": family_rates,
    "sensitivity_matrix": sensitivity_matrix,
    "sinervo_reference_table1": sinervo_reference,
    "rare_species_flag": {
        "low_N_cell_threshold": LOW_N_CELL_THRESHOLD,
        "n_low_N_species": int(per_species["low_N_warning"].sum()),
        "low_N_species_list": per_species.loc[
            per_species["low_N_warning"], "species"
        ].tolist(),
        "note": (
            "Rare-species per-species rates (n_cells < 10) are grid-coupled "
            "(Lobo et al. 2007, Hurlbert & Jetz 2007); interpret with caution."
        ),
    },
    "deviations": {
        "tb_source": (
            "Lacertidae family-level Table 1 (T_b=35.4 degC). "
            "Iberian-specific T_b records deferred to v0.2.0."
        ),
        "critical_window": (
            "April-May (61 days, Iberian Podarcis/Iberolacerta/Timon "
            "breeding chronology). Sinervo SOM Sceloporus calibration "
            "uses March-April; SOM says '2 months in temperate zone'."
        ),
        "climate_forcing": (
            "DestinE Climate DT SSP3-7.0 IFS-NEMO at HEALPix nside=128, "
            "2020-2039 (vs Sinervo WorldClim 1.4 + CCCMA/HADCM3/CSIRO a2a, "
            "1975/2020/2050/2080)."
        ),
        "diurnal_reconstruction": (
            "Not applied. Sinervo SOM Eq. S2 is parameterised in daily Tmax; "
            "DestinE 6-hourly samples are aggregated to daily max in "
            "02_data_clean. Sub-daily probe outcome: "
            f"{'SUCCESS' if subdaily_success else 'unavailable - sinusoidal fallback unused'}."
        ),
    },
}
with open(HEADLINE_JSON, "w") as f:
    json.dump(headline, f, indent=2)
print(f"\nSaved {HEADLINE_JSON}")
print(json.dumps(headline, indent=2))
