# 05 — FORRT Replication Outcome

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify the actual numerical results first** by reading `results/headline.json`, `results/tables/local_extinction_per_species.csv`, and `notebooks/03_analysis.py`. Don't quote numbers from memory. See `docs/verify-before-drafting.md`.

## Field-by-field draft

### Short URI suffix for outcome ID (text input, required)

Slug. Use kebab-case.

```
lacertidae-iberia-h-r-replication-2026-v0-1-0
```

### Plain-text label for the outcome (text input, required)

Descriptive title.

```
Iberian Lacertidae h_r mechanism replication — DestinE 2020-2039
```

### Search for a FORRT replication study (search/select, required)

URI of the Replication Study published in step 04. Pull from `nanopubs/PUBLISHED.md` once published.

```
TODO — paste step-04 Replication Study URI after publishing
```

### Repository URL (text input, required)

```
https://github.com/annefou/weatherxbiodiversity-lizards
```

### Completion date (date picker, required)

```
2026-05-16
```

### Validation status (dropdown, required)

- [ ] Validated
- [x] **PartiallySupported**
- [ ] Contradicted

This dropdown maps to the CiTO intention in step 06: Validated → `confirms`, PartiallySupported → `qualifies`, Contradicted → `disputes`. **For this replication the CiTO relation is `cito:extends` per locked decision 5** (cross-taxon × new-horizon × FAIR-workflow application), not `qualifies` — the headline 2050 / 2080 numbers Sinervo reports are not reachable under the DestinE-DT horizons available to us, so we extend the mechanism's applicability map rather than verdict-against the original headline. The `PartiallySupported` value here reflects that the mechanism *transfers* (deterministic h_r model applies to Lacertidae without modification) but the *predictions* are prior-conditional in a way the source paper's single-figure headline does not surface.

### Confidence level (dropdown, required)

_Vocabulary not yet captured — leave per instructions._

```

```

### Describe the overall conclusion about the original claim (textarea, required)

```
Under family-mean Lacertidae priors (T_b = 35.4 °C, Sinervo Table 1) and a conservative April-May reproductive window, the Sinervo 2010 h_r mechanism predicts no Iberian Lacertidae local extinction at DestinE-reachable horizons (2020-2039 under SSP3-7.0). Under the worst-plausible compound prior (cool-adapted Iberolacerta T_b = 31 °C and the actual May-June breeding chronology of Iberian Podarcis / Iberolacerta), the mechanism flags 2.88-3.56 % of Lacertidae cell-years — tail-dominated by extreme single years rather than monotonic decadal warming. The DestinE-reachable horizon does not extend to Sinervo's 2050 projection year (Sinervo Table 1: Lacertidae 24.1 % by 2050, 46.0 % by 2080); this Outcome therefore extends rather than confirms or disputes Sinervo's headline number. Three substantive findings: (i) mechanism applicability is prior-conditional — single-axis perturbations of T_b OR window keep the signal at 0 %, only the compound worst-plausible flags cells; (ii) the gap between DestinE-reachable horizons and Sinervo's 2050 / 2080 projection horizons is itself a finding about the operational reach of climate-digital-twin replications; (iii) the mechanism is event-dominated under Iberian conditions, qualitatively different from the mean-thermal-exceedance pattern Soroye et al. 2020 reported for Iberian Bombus under the same DestinE archive.
```

### Describe the evidence that supports your conclusion (textarea, required)

Numerical results read directly from `results/headline.json`.

```
Sensitivity matrix (lizard-biology priors × DestinE Climate DT SSP3-7.0 daily Tmax, 2020-2039):

CONFIG                                    2020s    2030s    max(daily-mean h_r)   N cell-years > 3.1 h
Baseline (family T_b=35.4, Apr-May)        0.00 %   0.00 %    0.46 h               0
S1a: family T_b, May-Jun window            0.00 %   0.00 %    2.61 h               0
S1b: family T_b, Apr-Jun window            0.00 %   0.00 %    1.75 h               0
S2:  Iberolacerta T_b=31, Apr-May          0.00 %   0.00 %    1.88 h               0
S3a: Iberolacerta T_b=31, May-Jun          3.56 %   2.88 %    5.60 h               170
S3b: Iberolacerta T_b=31, Apr-Jun          0.30 %   0.08 %    3.82 h               10

Geographical extent: 264 Lacertidae presence cells at HEALPix nside=128 across the Iberian Peninsula, drawn from a GBIF download of 136,210 Lacertidae × Iberia occurrence records since 1900 (DOI 10.15468/dl.rh4rfn). 47 Lacertidae species in scope; 22 of 47 species are low-N (n_cells < 10) and flagged in the per-species CSV as grid-coupled per Lobo et al. 2007 / Hurlbert & Jetz 2007 — interpret per-species rates for low-N species with the published rare-species ranking caveat in mind. Threshold (3.1 h) is the Sinervo Table 1 Lacertidae family-calibrated h_r; mean is the daily-mean over the reproductive window per the SOM Eq. S2 conditional clamping h_r[T_e > T_b_preferred] = 0.74 × (T_max − T_b) + 6.1. Reference Sinervo Table 1 Lacertidae values: 3.4 % local extinction by 2009 (observed-period baseline), 24.1 % by 2050, 46.0 % by 2080 — none of these horizons is reachable by the current DestinE Climate DT archive.

Per-species detail (baseline config): figures/per_species_rates.png. Sensitivity matrix headline figure: figures/main_result.png. Iberia decadal h_r maps: figures/h_r_map_2020s.png, figures/h_r_map_2030s.png.
```

### Describe what limits the conclusions of the study (textarea, optional)

```
Five limitations, ordered by interpretive importance:

(1) Tail-dominated event structure. The h_r > threshold signal under the only configuration that flags cells (S3a) is concentrated in a small number of single-year extremes — 170 cell-years out of 5,280 total. The 2020s > 2030s direction (3.56 > 2.88 %) is not a monotonic-cooling anomaly but reflects interannual variability in extreme-heat-day frequency on a single DestinE realisation. Reporting both decades as point estimates (rather than as a 2020s → 2030s trend statement) is honest; reading the difference as a trend would over-interpret a single climate realisation.

(2) Prior-conditional mechanism applicability. The headline finding depends on lizard-biology parameter choices in a way the source paper's single 24 % / 2050 figure does not surface. Single-axis perturbations (T_b alone OR window alone) keep the signal at zero; only the compound worst-plausible combination flags cells. Defensible alternative parameterisations (Iberian-specific species T_b records from Carretero, Monasterio, Spanish herpetological literature; species-specific breeding chronologies for Pyrenean Iberolacerta vs Mediterranean Timon) would refine this — explicitly deferred to a v0.2.0 iteration.

(3) Projection-horizon mismatch. DestinE Climate DT exposes 2020-2039 in the current archive; Sinervo's headline projections are at 2050 and 2080. The Outcome cannot speak to the headline 24 % / 46 % numbers directly — only verify that the mechanism does not predict premature collapse at near-term horizons (and it does not, under any family-mean configuration). Sinervo's 2050 / 2080 figures remain testable only under future DestinE archive expansion.

(4) Reproductive-window heuristic. Default April-May matches Sinervo SOM's "2 months in the temperate zone" generic guidance but not the Iberian-Lacertidae-specific breeding chronology, which extends into May-June for most Iberian Podarcis / Iberolacerta species. The May-June and April-June sensitivities (S1a, S1b, S3a, S3b) are stress-tests against this heuristic; the April-May baseline is the conservative single-point estimate.

(5) Daily Tmax vs hourly trace. SOM Eq. S2 is parameterised in daily Tmax and computed daily; we use the same form. The sub-daily Polytope-access probe attempted in 01_data_download.py returned "credentials absent — fallback unused"; sinusoidal diurnal-cycle reconstruction was scoped but not needed because the mechanism is daily-Tmax-driven, not hourly-integration-driven. Recorded in headline.json `config.subdaily_probe_status` and `deviations.diurnal_reconstruction`.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.

## Drafting notes (for Anne's review — not part of the nanopub)

- **Vocabulary substitution:** Anne's verbatim recommendation in the kickoff briefing used "Iberian extirpation". The paper-analyst's locked vocabulary rule (from `00_paper_summary.md` "Extinction vs extirpation vocabulary" — *"The paper does not use 'extirpation'. Downstream drafts (Claim, Study, Outcome) MUST use the paper's 'local extinction' / 'species extinction' pair"*) requires "local extinction" instead. The Outcome above substitutes "local extinction" throughout; the substantive framing is identical.
- **Pending fields:** the step-04 Replication Study URI in the Search/Select field is `TODO` until that nanopub is published. The Confidence level dropdown vocabulary was not captured in the template — left blank.
- **Validation status `PartiallySupported`** reflects that the mechanism transfers but predictions are prior-conditional. The CiTO relation in step 06 stays at `cito:extends` (locked decision 5), not `cito:qualifies` — see the Validation-status rationale paragraph above.
- **Cross-replication synthesis** (Bombus constellation comparison) is **out of scope for this Outcome** — that lives in the Synthesis nanopub (step 08) at the apex of the chain. The Outcome here speaks only to the Iberian Lacertidae replication's own findings.
