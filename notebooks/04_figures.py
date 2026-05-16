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
# # 04 — Figures (Iberian Lacertidae h_r exceedance)
#
# Produces four figures from the analysis outputs:
#
# * **`figures/main_result.png` / `.pdf`** — **sensitivity matrix**. A
#   2×3 heatmap (T_b prior × reproductive-window choice) of the
#   Lacertidae local-extinction rate at 2020s / 2030s. This is the
#   headline Phase-3 figure: it makes the prior-conditional behaviour
#   visible (single-axis perturbations → 0 %; compound worst-plausible
#   → ~3 %).
# * **`figures/per_species_rates.png` / `.pdf`** — per-species
#   local-extinction rate under the baseline config (family-mean T_b,
#   April-May window). 2020s vs 2030s lollipop, low-N species flagged.
# * **`figures/h_r_map_2020s.png`** — Iberian map of decadal mean
#   daily h_r over April-May, with the 3.1 h threshold contour.
# * **`figures/h_r_map_2030s.png`** — same for the 2030s.
#
# Per `USER_PREFERENCES.md`: `plot_style = "seaborn-v0_8-whitegrid"`,
# `plot_dpi = 150`, `plt.show()` *after* `fig.savefig()` so plots appear
# inline in the MyST Jupyter Book build.

# %%
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

import cartopy.crs as ccrs
import cartopy.feature as cfeature

# %%
plt.style.use("seaborn-v0_8-whitegrid")
DPI = 150

ROOT = Path("..").resolve()
INTERMEDIATE = ROOT / "data" / "intermediate"
RESULTS = ROOT / "results"
RESULTS_TABLES = RESULTS / "tables"
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

EXTINCTION_MASK_NC = INTERMEDIATE / "extinction_mask_nside128.nc"
PER_SPECIES_CSV = RESULTS_TABLES / "local_extinction_per_species.csv"
HEADLINE_JSON = RESULTS / "headline.json"

# Sinervo Table 1 Lacertidae reference threshold (for the map contour).
H_R_THRESHOLD = 3.1

# %% [markdown]
# ## Load analysis outputs

# %%
ds = xr.open_dataset(EXTINCTION_MASK_NC)
print(ds)

per_species = pd.read_csv(PER_SPECIES_CSV)
with open(HEADLINE_JSON) as f:
    headline = json.load(f)
print(f"\nHeadline: {headline['lacertidae_family_rates_destine']}")


# %% [markdown]
# ## Figure 1 — Main result: sensitivity matrix
#
# 2×3 heatmap (T_b prior × reproductive-window choice) of the family-wide
# Lacertidae local-extinction rate (fraction of Lacertidae presence cells
# with daily-mean h_r over the reproductive window > 3.1 h). Two panels
# side-by-side for 2020s and 2030s. Each cell annotated with the rate;
# colour ramp emphasises the compound-prior corner where the mechanism
# actually flags cells.

# %%
sens = headline["sensitivity_matrix"]
# Layout: rows = T_b values (35.4 family, 31 Iberolacerta);
# cols = window choices (Apr-May, May-Jun, Apr-Jun).
T_BS = [35.4, 31.0]
WINDOWS = [(4, 5), (5, 6), (4, 5, 6)]
WINDOW_LABELS = ["Apr-May", "May-Jun", "Apr-Jun"]
T_B_LABELS = ["family\nT_b = 35.4 °C", "Iberolacerta\nT_b = 31 °C"]


def _grid(decade: str) -> np.ndarray:
    out = np.full((len(T_BS), len(WINDOWS)), np.nan, dtype=float)
    key = f"local_extinction_{decade}"
    for row in sens.values():
        if row["t_b_degC"] in T_BS and tuple(row["months"]) in WINDOWS:
            i = T_BS.index(row["t_b_degC"])
            j = WINDOWS.index(tuple(row["months"]))
            out[i, j] = row[key]
    return out


grid_2020s = _grid("2020s")
grid_2030s = _grid("2030s")
vmax = float(np.nanmax([grid_2020s, grid_2030s]))
if vmax == 0:
    vmax = 0.05  # ensure a visible colour ramp even when all zero

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
for ax, grid, decade in zip(axes, [grid_2020s, grid_2030s], ["2020s", "2030s"]):
    im = ax.imshow(grid, cmap="Reds", vmin=0, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(WINDOWS)))
    ax.set_xticklabels(WINDOW_LABELS)
    ax.set_yticks(range(len(T_BS)))
    ax.set_yticklabels(T_B_LABELS)
    ax.set_title(f"{decade}", fontsize=12)
    # Annotate each cell with the rate.
    for i in range(len(T_BS)):
        for j in range(len(WINDOWS)):
            v = grid[i, j]
            txt_colour = "white" if v > vmax * 0.55 else "black"
            ax.text(
                j, i,
                f"{v*100:.2f}%",
                ha="center", va="center",
                fontsize=11, color=txt_colour, fontweight="bold",
            )
    ax.set_xlabel("Reproductive window")

axes[0].set_ylabel("Preferred body temperature")
fig.colorbar(im, ax=axes, shrink=0.85, label="Local-extinction rate")
fig.suptitle(
    "Iberian Lacertidae h_r mechanism — sensitivity to lizard-biology priors\n"
    "Sinervo 2010 SOM Eq. S2 applied under DestinE Climate DT SSP3-7.0",
    fontsize=12,
)

fig.savefig(FIG_DIR / "main_result.png", dpi=DPI, bbox_inches="tight")
fig.savefig(FIG_DIR / "main_result.pdf", bbox_inches="tight")
plt.show()
print(f"Wrote {FIG_DIR / 'main_result.png'} and .pdf")


# %% [markdown]
# ## Figure 2 — Per-species local-extinction rate (baseline config)
#
# A two-column dot plot, species on the y axis (sorted by 2020s rate),
# horizontal lollipops for 2020s and 2030s. Low-N species (n_cells < 10)
# are shown in a paler colour with a small marker. Sinervo Table 1
# Lacertidae 2050 / 2080 reference values are shown as vertical
# reference lines for context (with a clear "different horizon" caveat).
# Uses the baseline config (family T_b = 35.4 °C, April-May window);
# see Figure 1 for the full sensitivity matrix.

# %%
df = per_species.copy()
# Drop species with zero presence cells (defensive — shouldn't happen).
df = df[df["n_cells"] > 0].copy()
df = df.sort_values("local_ext_2020s", ascending=True).reset_index(drop=True)

n_spp = len(df)
fig, ax = plt.subplots(figsize=(9, max(5, 0.22 * n_spp + 2)))

y = np.arange(n_spp)
colour_2020s = "#1f77b4"
colour_2030s = "#d62728"
faint_alpha = 0.4

for i, (_, row) in enumerate(df.iterrows()):
    rare = bool(row["low_N_warning"])
    alpha = faint_alpha if rare else 1.0
    ax.plot(
        [row["local_ext_2020s"], row["local_ext_2030s"]],
        [i, i],
        color="grey", lw=1, alpha=0.35 if rare else 0.6, zorder=1,
    )
    ax.scatter(
        row["local_ext_2020s"], i, s=42 if not rare else 22,
        color=colour_2020s, alpha=alpha, zorder=3,
        label="2020s" if i == 0 else None,
    )
    ax.scatter(
        row["local_ext_2030s"], i, s=42 if not rare else 22,
        color=colour_2030s, alpha=alpha, zorder=3,
        label="2030s" if i == 0 else None,
    )

ax.set_yticks(y)
ax.set_yticklabels(
    [f"{s} (n={int(n)})" for s, n in zip(df["species"], df["n_cells"])],
    fontsize=8,
)
ax.set_xlabel(
    f"Local-extinction rate "
    f"(fraction of presence cells with cumulative April-May h_r > {H_R_THRESHOLD} h)"
)
ax.set_xlim(-0.02, 1.02)
ax.axvline(
    headline["sinervo_reference_table1"]["lacertidae_local_extinction_2050"],
    ls="--", color="grey", lw=1, alpha=0.6,
)
ax.text(
    headline["sinervo_reference_table1"]["lacertidae_local_extinction_2050"],
    n_spp - 0.5,
    " Sinervo 2050 (Lacertidae)",
    fontsize=8, va="top", color="grey",
)
ax.axvline(
    headline["sinervo_reference_table1"]["lacertidae_local_extinction_2080"],
    ls="--", color="grey", lw=1, alpha=0.6,
)
ax.text(
    headline["sinervo_reference_table1"]["lacertidae_local_extinction_2080"],
    n_spp - 0.5,
    " Sinervo 2080",
    fontsize=8, va="top", color="grey",
)
ax.set_title(
    "Iberian Lacertidae — local-extinction rate per species (DestinE SSP3-7.0)\n"
    f"family-wide: {headline['lacertidae_family_rates_destine']['local_extinction_2020s']:.1%} (2020s) | "
    f"{headline['lacertidae_family_rates_destine']['local_extinction_2030s']:.1%} (2030s)",
    fontsize=11,
)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, axis="x", alpha=0.4)
ax.grid(False, axis="y")

fig.tight_layout()
fig.savefig(FIG_DIR / "per_species_rates.png", dpi=DPI, bbox_inches="tight")
fig.savefig(FIG_DIR / "per_species_rates.pdf", bbox_inches="tight")
plt.show()
print(f"Wrote {FIG_DIR / 'per_species_rates.png'} and .pdf")


# %% [markdown]
# ## Figure 3 — Substrate-sensitivity diagnostic (S3a config)
#
# Mirrors the Bombus chain-3 `weatherxbiodiversity-substrate-sensitivity`
# pattern. One point per Lacertidae species; x = local-extinction rate
# at HEALPix nside=128 (DestinE native), y = same at nside=64
# (downsampled via NESTED bit-shift parent = pix >> 2). Diagonal is
# y = x; deviation = substrate-coupled ranking. Spearman ρ annotated
# for the full set and the well-sampled (n_cells ≥ 10) subset.
#
# Run under S3a (Iberolacerta T_b = 31 °C, May-Jun window) — the only
# sensitivity-matrix config that produces non-zero rates. Under baseline
# + the other four configs both substrates report 0 % for every
# species, so the diagnostic is degenerate.

# %%
SUBSTRATE_CSV = RESULTS_TABLES / "substrate_sensitivity_per_species.csv"
subs = pd.read_csv(SUBSTRATE_CSV)
subs_summary = headline["substrate_sensitivity"]

fig, ax = plt.subplots(figsize=(7.2, 6.5))

x_n128 = subs["local_ext_2020s_n128"].values
y_n64 = subs["local_ext_2020s_n64"].values
low_n_mask = subs["low_N_warning_n128"].values

# y = x diagonal reference.
hi = float(max(x_n128.max(), y_n64.max())) * 1.05 if max(x_n128.max(), y_n64.max()) > 0 else 0.05
ax.plot([0, hi], [0, hi], color="grey", lw=1, ls="--", alpha=0.6, zorder=1, label="y = x")

# Points: low-N vs well-sampled.
ax.scatter(
    x_n128[~low_n_mask], y_n64[~low_n_mask],
    s=60, color="#1f77b4", alpha=0.85, zorder=3,
    label=f"n_cells ≥ 10 (n={int((~low_n_mask).sum())})",
)
ax.scatter(
    x_n128[low_n_mask], y_n64[low_n_mask],
    s=40, color="grey", alpha=0.6, zorder=2,
    label=f"n_cells < 10 (n={int(low_n_mask.sum())}) — low-N, ranking grid-coupled",
)

ax.set_xlim(-hi*0.05, hi)
ax.set_ylim(-hi*0.05, hi)
ax.set_xlabel("Per-species local-extinction rate, 2020s — HEALPix nside=128 (DestinE native)")
ax.set_ylabel("Per-species local-extinction rate, 2020s — HEALPix nside=64 (downsampled)")
ax.set_aspect("equal", adjustable="box")

rho_all = subs_summary["spearman_rho_all_species"]
rho_high = subs_summary["spearman_rho_n_cells_ge_10"]
rho_low = subs_summary["spearman_rho_n_cells_lt_10"]
rho_low_txt = "n/a (zero variance)" if pd.isna(rho_low) else f"{rho_low:.3f}"

ax.text(
    0.04, 0.96,
    f"Spearman ρ (per-species rate, 2020s, n128 vs n64):\n"
    f"  all species (n={subs_summary['n_species_joined']}):    {rho_all:.3f}\n"
    f"  n_cells ≥ 10 (n={subs_summary['n_species_n_cells_ge_10']}):                  {rho_high:.3f}\n"
    f"  n_cells < 10 (n={subs_summary['n_species_n_cells_lt_10']}):                  {rho_low_txt}",
    transform=ax.transAxes, ha="left", va="top",
    fontsize=8.5, family="monospace",
    bbox=dict(facecolor="white", edgecolor="grey", lw=0.5, alpha=0.92, pad=4),
)

ax.set_title(
    "Substrate-sensitivity diagnostic — Iberian Lacertidae\n"
    "S3a config (T_b = 31 °C, May-Jun); mirrors Bombus chain-3 pattern",
    fontsize=11,
)
ax.legend(loc="lower right", fontsize=9, framealpha=0.92)
ax.grid(True, alpha=0.35)

fig.tight_layout()
fig.savefig(FIG_DIR / "substrate_sensitivity.png", dpi=DPI, bbox_inches="tight")
fig.savefig(FIG_DIR / "substrate_sensitivity.pdf", bbox_inches="tight")
plt.show()
print(f"Wrote {FIG_DIR / 'substrate_sensitivity.png'} and .pdf")


# %% [markdown]
# ## Figures 4 & 5 — Iberia maps of daily-mean h_r per decade
#
# Show the decadal mean of April-May daily-mean h_r per HEALPix cell.
# Cells above the 3.1 h threshold are highlighted; below-threshold
# cells use a softer ramp. The map statistic (mean of daily h_r over
# the 61-day window, decadal-mean across years) matches the threshold
# semantics (mean daily restriction hours during the critical period).
#
# We render the HEALPix cells as a scatter of cell centres with
# square markers sized to the cell area at this latitude. This is the
# simplest rendering that matches the Bombus sister repo's
# `04h_figures_healpix` pattern and avoids the cartopy + healpix-plot
# tile-edge gotchas (cartopy doesn't natively reproject HEALPix tiles).

# %%
def plot_h_r_map(label: str, y_start: int, y_end: int, vmax: float):
    sel = (ds["year"] >= y_start) & (ds["year"] <= y_end)
    h_r_decade = ds["h_r_mean_critical"].isel(year=sel).mean(dim="year")
    lon = ds["lon"].values
    lat = ds["lat"].values

    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-10, 4, 35, 44], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE.with_scale("50m"), lw=0.7)
    ax.add_feature(cfeature.BORDERS.with_scale("50m"), lw=0.4, alpha=0.6)
    ax.add_feature(cfeature.OCEAN.with_scale("50m"), color="#eaf4fb", zorder=0)
    ax.add_feature(cfeature.LAND.with_scale("50m"), color="#f5f1ea", zorder=0)

    sc = ax.scatter(
        lon, lat,
        c=h_r_decade.values,
        s=20,
        marker="s",
        cmap="YlOrRd",
        vmin=0, vmax=vmax,
        transform=ccrs.PlateCarree(),
        edgecolors="none",
    )

    above = h_r_decade.values > H_R_THRESHOLD
    if above.any():
        ax.scatter(
            lon[above], lat[above],
            s=24, marker="s", facecolors="none", edgecolors="black",
            lw=0.4, transform=ccrs.PlateCarree(),
        )

    cb = plt.colorbar(sc, ax=ax, orientation="vertical", shrink=0.85, pad=0.03)
    cb.set_label(f"April-May daily-mean h_r (h) — decadal mean")
    cb.ax.axhline(H_R_THRESHOLD, color="black", lw=1)
    cb.ax.text(
        1.5, H_R_THRESHOLD, f" h_r = {H_R_THRESHOLD} h (Lacertidae threshold)",
        fontsize=8, va="center", transform=cb.ax.get_yaxis_transform(),
    )

    ax.set_title(
        f"Iberia — daily-mean April-May h_r, {label} (DestinE SSP3-7.0)\n"
        f"{int(above.sum())} of {len(lon)} cells > {H_R_THRESHOLD} h",
        fontsize=11,
    )
    gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False,
                      lw=0.3, alpha=0.4)
    gl.top_labels = False
    gl.right_labels = False

    out_png = FIG_DIR / f"h_r_map_{label}.png"
    fig.savefig(out_png, dpi=DPI, bbox_inches="tight")
    plt.show()
    print(f"Wrote {out_png}")


# Shared vmax across the two decades so the colour ramp is comparable.
both = ds["h_r_mean_critical"].values
vmax_shared = float(np.percentile(both, 99))
print(f"Shared colour-ramp max (99th percentile): {vmax_shared:.2f} h")

plot_h_r_map("2020s", 2020, 2029, vmax_shared)
plot_h_r_map("2030s", 2030, 2039, vmax_shared)
