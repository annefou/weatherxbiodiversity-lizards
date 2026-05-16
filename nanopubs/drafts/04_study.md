# 04 — FORRT Replication Study

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify code first:** read the actual reproduction script in `notebooks/03_analysis.py` before writing the methodology field. See `docs/verify-before-drafting.md`.

## Field-by-field draft

### Short URI suffix for study ID (text input, required)

Slug. Use kebab-case.

```
lacertidae-iberia-destine-2020-2039
```

### Label/name of replication study (text input, required)

Human-readable title.

```
Iberian Lacertidae h_r mechanism replication under Destination Earth Climate DT SSP3-7.0 (2020-2039)
```

### Study type (dropdown, required)

- [ ] Reproduction Study — direct reproduction: same methodology, same tools.
- [x] **Replication Study** — replication with different methodology or conditions.
- [ ] Reproduction/Replication Study — both.

**Rationale:** different taxon (Iberian Lacertidae, not the Phrynosomatidae empirical core or the global 34-family projection), different climate-data product (Destination Earth Climate Digital Twin SSP3-7.0 at HEALPix nside=128, not WorldClim 1.4 + NOAA / European Climate Assessment cross-validation at 10 arc-minute resolution), and different time horizon set (2020-2039 only — DestinE does not reach 2050 or 2080). The mechanism (h_r in activity during the critical reproductive period → demographic collapse → local extinction) is held fixed; what changes is the parameterisation, the climate forcing, and the spatial substrate.

### Search for a FORRT claim (search/select, required)

URI of the Claim published in step 03. Pull from `nanopubs/PUBLISHED.md`.

```
TODO_PASTE_STEP_03_CLAIM_URI
```

### Describe what part of the claim is reproduced/replicated (textarea, required)

The **scope** of the claim being tested. Which aspect, what's in/out of scope. NOT methodology. NOT results.

```
The transferability of the Sinervo 2010 h_r mechanism (cumulative daily hours of activity restriction during the critical reproductive period predicting local extinction in heliothermic lizards) to the Iberian Lacertidae assemblage at near-term horizons reachable under the current Destination Earth Climate Digital Twin archive (2020-2039 under SSP3-7.0). In scope: all 47 Iberian Lacertidae species with at least one georeferenced occurrence record in the GBIF download 10.15468/dl.rh4rfn (Spain, Portugal, Andorra, Gibraltar; year >= 1900; hasCoordinate = TRUE; hasGeospatialIssue = FALSE; basisOfRecord IN HUMAN_OBSERVATION/PRESERVED_SPECIMEN/MACHINE_OBSERVATION); the family-calibrated h_r threshold from Sinervo Table 1 (3.1 h for Lacertidae); two T_b prior choices (family mean 35.4 °C from Table 1, Iberolacerta-style cool-adapted 31 °C); three reproductive-window choices (April-May, May-June, April-June); two HEALPix substrates (nside=128 DestinE-native, nside=64 substrate-sensitivity diagnostic). Out of scope: Sinervo's headline 2050 / 2080 projections (not reachable under current DestinE archive); non-heliothermic Iberian lizard families (Gekkonidae, Anguidae, Scincidae — the basking-window mechanism is calibrated for diurnal heliotherms only); species-specific T_b refinement using Iberian-specific records from Carretero / Monasterio / Spanish herpetological literature (deferred to a v0.2.0 iteration).
```

### Describe how the claim is reproduced/replicated (textarea, required)

The **method** in plain prose. Read `notebooks/03_analysis.py` and any config files first. NOT exact numerical results.

```
Pipeline implemented in the four-notebook structure of notebooks/ (01_data_download.py → 02_data_clean.py → 03_analysis.py → 04_figures.py), wired by Snakefile. Inputs: (a) Destination Earth Climate DT t2m field, daily-aggregated from 4-times-daily IFS-NEMO snapshots over 2020-2039 SSP3-7.0 at HEALPix nside=128 NESTED ordering (DestinE-native, no re-projection; 25 GB total, retrieved once via Polytope and symlinked from the sister `weatherxbiodiversity-projection` repository for compute parity); (b) CRU TS 3.24.01 historical Tmax / Tmin NetCDF (Soroye Figshare deposit 10.6084/m9.figshare.10058340; reused for diurnal-cycle baseline); (c) GBIF Lacertidae × Iberia occurrence download (DOI 10.15468/dl.rh4rfn; 136,210 records). Iberian HEALPix cell mask derived from the global nside=128 grid by spatial subset to bbox (-10°, 35°, 4°, 44°) yielding 479 cells. Occurrences assigned to cells via `healpix_geo.nested.lonlat_to_healpix(..., nest=True)`. h_r computed per cell × per day under Sinervo SOM Equation S2 with conditional clamping: `h_r = (0.74 * (T_max − T_b) + 6.1) if T_max > T_b else 0` (the bracket notation h_r[T_e > T_b_preferred] in the SOM is a conditional, not a max-zero clamp — daily T_max <= T_b means no refuge needed). Daily-mean h_r is averaged over the reproductive window per year and compared against the family-calibrated threshold of 3.1 h. A cell-year is flagged as locally extinct when daily-mean h_r > 3.1 h. Per-species local-extinction rate is the fraction of presence cells flagged in each decade (2020-2029, 2030-2039). Six-config sensitivity matrix (2 T_b values × 3 windows) and a substrate-sensitivity diagnostic comparing per-species rankings at HEALPix nside=128 vs nside=64 (downsampled via the NESTED bit-shift parent = pix >> 2). All intermediates persisted as NetCDF or Parquet (no .npz). Headline numbers and the full sensitivity matrix saved to results/headline.json for the Outcome nanopub.
```

### Describe any deviations from original methodology (textarea, optional)

What's different from the original method. Verify against the actual code, don't guess.

```
Six explicit deviations from Sinervo 2010, ordered by interpretive significance:

(1) Climate forcing. DestinE Climate Digital Twin SSP3-7.0 IFS-NEMO at HEALPix nside=128 (~46 km), 2020-2039. Sinervo used WorldClim 1.4 at 10 arc-minute resolution interpolated between 1975 and 2020 baselines and projected to 2050 / 2080 under IPCC AR3 scenarios (CCCMA / HADCM3 / CSIRO a2a). The DestinE archive's near-term-only horizons mean Sinervo's headline 24 % / 46 % Lacertidae projections for 2050 / 2080 cannot be tested directly — only the mechanism's behaviour at 2020s and 2030s horizons.

(2) Taxon. Iberian Lacertidae (47 species across 264 presence cells in the Iberian Peninsula). Sinervo's empirical calibration used 48 Mexican Sceloporus (Phrynosomatidae) at 200 sites with a 1975 baseline census; the global projection used 587 species across 34 families with the Lacertidae row of Table 1 (n=89 records, n_spp=279) as the family parameterisation we inherit.

(3) Thermal-physiology priors. Used the family-level Lacertidae Table 1 row (T_b = 35.4 +/- 0.31 °C, h_r threshold = 3.1 h, heliothermic mode) as the baseline. Iberian-specific T_b records from the Spanish herpetological literature (Carretero, Monasterio et al.) were not incorporated in v0.1.0 — explicitly deferred to v0.2.0. A sensitivity branch substitutes Iberolacerta-style cool-adapted T_b = 31 °C to test prior-conditional behaviour.

(4) Reproductive-window choice. Default April-May (the conservative single-point estimate for Iberian temperate-zone Lacertidae). Sinervo's Sceloporus calibration used March-April; SOM page 4 specifies "2 months in the temperate zone" generically without an Iberian-specific source. Sensitivity branches test May-June (closer to actual Iberian Podarcis / Iberolacerta breeding chronology) and April-June (extended-window dilution).

(5) Diurnal-cycle reconstruction. Not applied. SOM Equation S2 is parameterised in daily T_max; DestinE 6-hourly snapshots are aggregated to daily max in 02_data_clean.py, then fed directly to the h_r formula. The sub-daily Polytope-access probe in 01_data_download.py returned "credentials absent" (recorded in results/headline.json::config.subdaily_probe_status); the sinusoidal Tmin-Tmax diurnal-cycle reconstruction scoped under locked-decision-3 fallback was not needed because the mechanism is daily-Tmax-driven, not hourly-integration-driven.

(6) Spatial substrate. HEALPix-NESTED nside=128 throughout, matching Bombus chain-2 substrate. A substrate-sensitivity diagnostic mirroring Bombus chain 3 runs the same h_r computation at HEALPix nside=64 (downsampled via NESTED bit-shift) under the S3a config — the only sensitivity-matrix config that produces non-zero rates and is therefore the only config where the substrate comparison is non-degenerate. Sinervo's spatial substrate is the WorldClim 10 arc-minute lat-lon grid; this is not a like-for-like substrate comparison but is documented to enable interpretation of the substrate-sensitivity diagnostic across the wider FORRT constellation.
```

### Search keywords (Wikidata) (multi-select, optional)

Provide labels (not QIDs) — the Wikidata search picks up labels.

- _Label 1:_ thermal physiology
- _Label 2:_ Lacertidae
- _Label 3:_ Iberian Peninsula
- _Label 4:_ climate change
- _Label 5:_ HEALPix
- _Label 6:_ Destination Earth

### Search discipline (Wikidata) (search, optional)

Provide labels.

- _Discipline label:_ ecology
- _Discipline label:_ herpetology
- _Discipline label:_ climate science

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.

## Drafting notes (not part of the nanopub)

- **Method ≠ Results.** The methodology field describes how the claim is tested (h_r computation, threshold comparison, decadal aggregation). Numerical results (0 % baseline, 3.56 % S3a, etc.) live only in the Outcome (step 05). See `docs/pico-study-outcome-levels.md`.
- **Scope ≠ Method.** What is reproduced (scope) is the *transferability* of the mechanism to Iberian Lacertidae at DestinE-reachable horizons. How it's reproduced (method) is the deterministic h_r pipeline. Conflating the two would make the chain non-composable.
- **Substrate-sensitivity diagnostic is part of the method, not the result.** The result of the diagnostic (Spearman rho = 0.951 for n_cells >= 10) belongs in the Outcome.
- **Honest framing** — the methodology field attributes every component to its source (Sinervo SOM Eq. S2, Bombus chain-2/chain-3 patterns, Lobo 2007 / Hurlbert & Jetz 2007 for the rare-species caveat). No part of the method is framed as novel.
