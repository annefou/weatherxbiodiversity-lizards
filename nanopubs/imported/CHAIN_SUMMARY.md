# Prior FORRT chain summary — Iberian *Bombus* constellation

**Entry URI**: https://w3id.org/sciencelive/np/RA1q6c0fG2bMbiozF8Az2UpIfzAzqp8hoVEl6QIzfUpH8
(Synthesis-level CiTO Citation, `cito:qualifies` upstream paper)
**Imported on**: 2026-05-16
**Constellation size (via SPARQL link-walk)**: 14 unique nanopubs (apex CiTO, Synthesis, 3 Outcomes, 3 Research Software, 3 chain-level CiTOs, 2 AIDAs, 1 Quote-with-comment). Studies + Claims are also part of the constellation but are not surfaced by the current import script — see "What this import does NOT include" below.

## Upstream paper

**Soroye, P., Newbold, T., & Kerr, J. (2020).** *Climate change contributes to widespread declines among bumble bees across continents.* **Science** 367(6478), 685–688. **DOI: 10.1126/science.aax8591**

## Why this prior chain matters for the lizards replication

The Bombus constellation tests **the same mechanism class** the Sinervo 2010 lizard paper is built around: **thermal-niche exceedance under climate warming as a driver of local extirpation**. Anne's three-chain constellation tested the mechanism on Iberian *Bombus* under SSP3-7.0 via DestinE Climate DT, with a substrate-sensitivity diagnostic that surfaced a methodological caveat (per-species ranking is grid-coupled for species with ≲10 historical cells).

The lizards replication is the cross-taxon follow-up: same mechanism class, different taxon (Lacertidae instead of *Bombus*), same geographic region (Iberia), same Climate DT data source (DestinE SSP3-7.0).

## Constellation structure

Three sibling FORRT chains aggregated by one Research Synthesis, plus an apex Synthesis-level CiTO Citation that formally `qualifies` Soroye 2020.

| Chain | Substrate | Outcome verdict | Chain-level CiTO relation | Zenodo concept DOI |
|---|---|---|---|---|
| `weatherxbiodiversity-projection` | CEA + HEALPix nside=64 (~92 km cells) | Validated | `cito:confirms` Soroye 2020 | 10.5281/zenodo.20113777 |
| `weatherxbiodiversity-projection-nside128` | HEALPix nside=128 (~46 km cells, DestinE native) | Validated | `cito:confirms` + `cito:extends` (chain 1) | 10.5281/zenodo.20113780 |
| `weatherxbiodiversity-substrate-sensitivity` | Cross-substrate methodological diagnostic | PartiallySupported | `cito:qualifies` Soroye 2020 + `cito:extends` (chains 1+2) | 10.5281/zenodo.20113786 |

**Apex Research Synthesis** (`RA5TJVZ0…`) — aggregates the three Outcomes into a single synthesis-level finding:

> "Synthesising the three sibling FORRT chains on Iberian Bombus (canonical CEA + HEALPix nside=64 replication, HEALPix nside=128 substrate extension, and the cross-substrate substrate-sensitivity methodological diagnostic), Soroye et al. 2020's TEI-based extirpation mechanism is substrate-robust at fit time but grid-coupled at projection time for low-N species."

**Synthesis-level CiTO Citation** (`RA1q6c0f…`, this constellation's apex) — `cito:qualifies` Soroye 2020 with the statement:

> "Soroye et al. 2020's TEI-based extirpation mechanism is substrate-robust at fit time but grid-coupled at projection time for low-N species; here is the diagnostic and the recommended reporting protocol."

## Per-chain content (from the imported nanopubs)

### Chain 1 — canonical CEA + HEALPix nside=64 replication

- **Outcome** (`RAPZMgc…`): *Validated*. Headline GLMM coefficient `sc_TEI_delta` = +0.454 (HEALPix nside=64), within ±30 % of the published continental value (+0.479 on CEA). The mechanism replicates and intensifies on Iberia.
- **CiTO** (`RALbHA-…`): `cito:confirms` Soroye 2020 on Iberian Bombus.
- **Research Software** (`RAKH9X…`): the weatherxbiodiversity-projection codebase.

### Chain 2 — nside=128 substrate extension

- **Outcome** (`RAa4QR…`): *Validated*. Headline coefficient at HEALPix nside=128 = +0.347 (95 % HDI [+0.139, +0.533]). Substrate-robust to the canonical sibling. Per-species ranking under SSP3-7.0 is substrate-stable for species with n_cells ≥ 10 historical cells (Spearman ρ vs nside=64 = +0.97).
- **CiTO** (`RAhw9m0B…`): `cito:confirms` + `cito:extends`.
- **Research Software** (`RA-GY81…`): the nside=128 sibling codebase.

### Chain 3 — substrate-sensitivity methodological diagnostic

- **Outcome** (`RAD19jy…`): *PartiallySupported*. The mechanism is substrate-robust at the fit step but **per-species risk ranking under SSP3-7.0 is grid-coupled for species with ≲10 historical grid cells**. Reshuffling happens specifically for the Pyrenean specialists and alpine *Bombus* that conservation prioritisation cares most about.
- **CiTO** (`RAumfa30…`): `cito:qualifies` Soroye 2020.
- **Research Software** (`RAfdV1y…`): the diagnostic toolkit.

## Quote-with-comment (shared backbone, `RAErLL_…`)

The verbatim Quote sentence from Soroye 2020 that all three chains anchor on (canonical Quote for the constellation). The lizards replication will quote a *different* verbatim sentence from Sinervo 2010 (anchoring on the basking-window mechanism, not the 2080 projection — per the kickoff decisions). The two Quote nanopubs are independent.

## AIDA sentences in the prior constellation

- **AIDA mech** (`RAgb6p…`) — "TEI_delta positive" / thermal-niche exceedance predicts extirpation in Iberian Bombus.
- **AIDA substrate-sensitivity** (`RAwGAt…`) — "projection grid-coupled" / per-species ranking reshuffles with HEALPix resolution for low-N species.

## External DOIs cited across the constellation

- `https://doi.org/10.1126/science.aax8591` — Soroye 2020 paper
- `https://doi.org/10.15468/dl.3frmsq` — GBIF Iberian *Bombus* download
- `https://doi.org/10.5281/zenodo.20113777` — Chain 1 Zenodo
- `https://doi.org/10.5281/zenodo.20113780` — Chain 2 Zenodo
- `https://doi.org/10.5281/zenodo.20113786` — Chain 3 Zenodo
- `https://doi.org/10.6084/m9.figshare.10058340` — Soroye Figshare deposit (CRU TS climate baseline)
- (Plus three other Zenodo records cross-referenced by the chains.)

## What this new replication can do

Given the prior Bombus constellation, the natural positioning options for the lizards replication:

- **`cito:extends`** the apex Synthesis-level CiTO (`RA1q6c0f…`) — testing the same mechanism class on a different taxon (Lacertidae) using the same workflow. This is the cleanest CiTO relation; signals cross-taxon transfer of the workflow.
- **`cito:extends`** one of the chain-level CiTOs (e.g. `RALbHA-…` for the canonical-substrate chain) — if the lizards replication mirrors the canonical-substrate design specifically.
- **`cito:qualifies`** Sinervo 2010 directly (NOT Soroye 2020) — Sinervo is the upstream paper for this chain; the apex CiTO of the lizards chain qualifies its own upstream paper, not Soroye's.

Per the kickoff decisions on file (`weatherxbiodiversity-projection` substrate-sensitivity sibling pattern), the lizards chain shape will mirror Chain 1 of the Bombus constellation. If a methodological diagnostic chain becomes warranted later (similar to Chain 3), it would be a separate sibling repo.

## Methodological precedents to inherit from the Bombus constellation

When drafting `nanopubs/drafts/04_study.md` and `05_outcome.md` for the lizards chain, mirror the Bombus chains' conventions:

1. **Outcome.hasDeviationDescription** — each Bombus Outcome documents 7–10 explicit deviations from Soroye 2020 (CRU TS climate baseline, HEALPix-NESTED vs CEA, GLMM specification, prior choices, projection-grid alignment, DestinE archive coverage, daily-vs-sub-daily approximation, etc.). The lizards Outcome should document analogous deviations from Sinervo 2010 — especially the DestinE-horizon constraint (no 2080 projection) which is already kickoff-decided.

2. **Outcome.hasLimitationsDescription** — Bombus Outcomes are explicit about (a) grid-coupling for low-N species; (b) reporting on linear-predictor η rather than logistic-transformed p_extirp; (c) negative-η species reflecting random intercepts; (d) sampling-effort caveats; (e) Tmax/Tmin from sub-daily approximations. Each of these has a Sinervo analogue.

3. **Study.hasMethodologyDescription** — the Bombus Studies cite specific GLMM formulae (`extinction ~ continent + sc_sampling + sc_TEI_bs + sc_TEI_delta + …`) and specific inference engines (statsmodels VB + bambi/PyMC NUTS, 4 chains × 2000 samples). The lizards Study should follow the same shape but for Sinervo's basking-window thermal-exceedance mechanism.

4. **Chain CiTO `extends` relation** — chain 2's CiTO `extends` chain 1's CiTO (substrate refit); chain 3's CiTO `extends` both. The lizards chain should `extends` the apex Synthesis-level CiTO (`RA1q6c0f…`) — signalling that this is the next-step cross-taxon application of the same workflow.

## What this import does NOT include (architectural limitation)

The SPARQL-driven importer found 14 of the constellation's ~19 expected nanopubs. Missing:

- **3 FORRT Replication Studies** (one per chain) — these exist but are not surfaced by the current `npa:refersToNanopub` graph indexing of SL-specific predicates (`isOutcomeOf`, `targetsClaim`).
- **2 FORRT Claims** (mechanism + substrate-sensitivity) — same reason.

These will be reachable cleanly once the proposed `GET /api/np/{uri}/constellation` endpoint in `science-live-platform/docs/plans/nanopub-query-api.md` ships. For now, the Studies and Claims are available by browsing each chain's repository directly:

- `https://github.com/annefou/weatherxbiodiversity-projection/blob/main/nanopubs/PUBLISHED.md`
- `https://github.com/annefou/weatherxbiodiversity-projection-nside128/blob/main/nanopubs/PUBLISHED.md`
- `https://github.com/annefou/weatherxbiodiversity-substrate-sensitivity/blob/main/nanopubs/PUBLISHED.md`

(The third repo's `PUBLISHED.md` is the canonical cross-chain registry for the whole Bombus constellation.)

## Open questions for the Phase 1 paper-analyst run

Once the verbatim Sinervo 2010 quote is in `nanopubs/drafts/01_quote.md`, the answers below shape the chain's framing:

1. The Quote sentence should anchor on Sinervo's mechanism statement (basking-window thermal-exceedance predicts extinction risk), NOT on the "20 % by 2080" headline projection — DestinE Climate DT does not currently cover 2080 (see kickoff decision 2 in `paper/sinervo-2010.pdf` + kickoff prompt).
2. The CiTO for this chain should `extends` the apex Bombus Synthesis-level CiTO (`https://w3id.org/sciencelive/np/RA1q6c0fG2bMbiozF8Az2UpIfzAzqp8hoVEl6QIzfUpH8`) AND `extends` or `qualifies` Sinervo 2010 — depending on what the Outcome verdict turns out to be.
3. If the Outcome is `Validated`, the CiTO relation to Sinervo 2010 is likely `cito:confirms` (mechanism transfers to Mediterranean Lacertidae). If `PartiallySupported`, it is `cito:qualifies`. The constellation-extension relation to the Bombus apex is `cito:extends` regardless.
