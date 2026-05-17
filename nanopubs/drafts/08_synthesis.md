# 08 — Research Synthesis (cross-taxon constellation apex)

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Scope check:** this Synthesis is the apex of a **cross-taxon constellation**, not just this chain. It aggregates findings from the three Iberian *Bombus* sibling chains (`weatherxbiodiversity-projection`, `…-nside128`, `…-substrate-sensitivity`) AND this `weatherxbiodiversity-lizards` chain into a single cross-replication statement about how the thermal-niche-exceedance mechanism class transfers across taxa under the Destination Earth Climate DT archive. The Bombus chains already have their own apex Synthesis (`RA5TJVZ0…`) at the family level; this Synthesis sits one level above that as the *constellation* apex.

**Form heading:** *"Science Live Research Synthesis — Synthesise findings across multiple replication outcomes with conclusions, recommendations, conditions, and limitations."*

## Field-by-field draft

### Short URI suffix for synthesis ID (text input, required)

Slug. Use kebab-case.

```
mediterranean-thermal-niche-exceedance-constellation-iberia
```

### Label of the synthesis (text input, required)

A one-line summary.

```
Iberian thermal-niche-exceedance constellation — Bombus (Soroye 2020) + Lacertidae (Sinervo 2010) under Destination Earth Climate DT SSP3-7.0
```

### Conclusion of the synthesis (textarea, required)

The aggregate finding across the underlying outcomes.

```
Thermal-niche-exceedance replicates as a class of mechanism across pollinators and ectotherms in Iberia, but operational extinction projections depend on parameter choices and time horizon in ways the source papers' headline figures do not surface. The two-taxon constellation shows: (i) Soroye 2020's TEI-based extirpation mechanism for Iberian Bombus is substrate-robust at fit time (GLMM coefficient sc_TEI_delta = +0.454 at HEALPix nside=64, +0.347 at nside=128 — both within ~30 % of the published continental +0.479) but grid-coupled at projection time for low-N species, surfaced operationally by the substrate-sensitivity sibling chain; (ii) Sinervo 2010's h_r mechanism for Iberian Lacertidae predicts zero local extinction at DestinE-reachable horizons (2020-2039) under family-mean priors, and only ~3 % at compound worst-plausible priors (Iberolacerta T_b + May-June reproductive window), with the per-species substrate-sensitivity diagnostic confirming substrate-robust rankings for well-sampled species (Spearman rho = 0.951 for n_cells >= 10). Across both taxa, three constellation-level claims emerge: (a) the mechanism class transfers cross-taxon when properly operationalised, but operational predictions are prior-conditional in ways the original papers' single-figure headlines do not surface; (b) DestinE-reachable horizons (2020-2039) sit below the activation thresholds for the lizards mechanism, so Sinervo's 24 % / 46 % / 2050 / 2080 projections cannot be tested under current archive coverage — the gap between near-term-DestinE and source-paper-projection horizons is itself a finding about the operational reach of climate-digital-twin replications; (c) the per-species rare-species-ranking grid-coupling caveat (Lobo et al. 2007; Hurlbert & Jetz 2007) manifests differently across taxa — as ranking-shuffle at non-zero rates in the Bombus chain, as signal-collapse below threshold in the Lacertidae chain — both consistent with the established literature, neither novel.
```

### Recommendations (textarea, required)

Actionable guidance for practitioners.

```
For practitioners testing thermal-niche-exceedance mechanisms in new taxa or under new climate-digital-twin archives:

(1) Report sensitivity matrices, not single-point headline figures. A 2 x 3 cross-product of T_b prior and reproductive-window choice (or analogous parameter axes) surfaces prior-conditional behaviour that single-figure headlines hide. This applies even when the baseline result is zero — the value of the matrix is showing the boundary of the parameter space where the mechanism activates.

(2) Run a substrate-sensitivity diagnostic at two HEALPix resolutions whenever per-species rankings are reported. Use the NESTED bit-shift parent = pix >> 2 for the downsample (no re-projection, free of regridding error). Report Spearman rho separately for well-sampled species (n_cells >= 10) and the low-N subset; the latter is expected to be grid-coupled per Lobo 2007 / Hurlbert & Jetz 2007, but the diagnostic confirms it operationally for the specific dataset.

(3) Honestly scope CiTO citation type to the projection horizon. Use `cito:extends` (not `cito:confirms` / `disputes`) when the digital-twin archive does not cover the source paper's projection horizon. The mechanism's behaviour at reachable horizons is a separate Outcome from the source paper's headline projection; conflating them produces over-claiming.

(4) Publish a cross-taxon constellation Synthesis whenever two or more chains share a mechanism class and a regional / temporal scope. The constellation-level statement (this nanopub) is qualitatively different from any single chain's Outcome, and the cross-chain consistency or divergence is itself a finding.

(5) Mirror prior chains' substrate, env, and pinning conventions wherever possible. The Bombus constellation established HEALPix-NESTED nside=128 as the DestinE-native substrate and a specific environment.yml pinning philosophy (lower-bounds + arviz<0.22 ceiling). The lizards chain reused both with no modification, which made the cross-replication composition trivial — the constellation Synthesis benefits operationally from this consistency.
```

### Conditions under which the synthesis applies (textarea, required)

Scope: data types, methods, domains, regions, time periods.

```
Region: Iberian Peninsula (Spain, Portugal, Andorra, Gibraltar — bbox roughly -10°W to 4°E, 35°N to 44°N).

Climate forcing: Destination Earth Climate Digital Twin SSP3-7.0 IFS-NEMO at HEALPix nside=128 native, 2020-2039 archive coverage. Single climate realisation (no ensemble). Daily-aggregated from 4-times-daily 2m temperature snapshots.

Taxa: heliothermic / diurnal-active ectotherms (Lacertidae lizards via Sinervo 2010) and warm-adapted social insects (Bombus pollinators via Soroye 2020). The mechanism class (thermal-niche exceedance under climate warming as a driver of local extirpation/extinction) is conserved across the two replications; the operational instantiation differs (h_r threshold for Lacertidae, TEI-delta GLMM coefficient for Bombus).

Methods: deterministic h_r threshold comparison (Lacertidae chain) and Bayesian GLMM TEI fit (Bombus chain). Both implemented in Python (xarray + healpix-geo + cfgrib + pygbif) with Snakefile pipelines, MIT-licensed and Zenodo-archived. Both follow the same FORRT chain shape (Quote → AIDA → Claim → Replication Study → Replication Outcome → CiTO Citation + Research Software).

Time period of validity: 2020-2039 only for the projection-horizon component; 2026-05 for the FAIR-archive / nanopub-network state. Future DestinE archive expansion may enable testing of Sinervo's 2050 / 2080 horizons.

Pinning: HEALPix NESTED ordering throughout; geographic data uses healpix-geo (NOT healpy, per DOMAIN.md); arviz<0.22 for PyMC compatibility; numpy 2.x; pymc 5.25+.
```

### Limitations of the synthesis (textarea, required)

What was not tested? What might not generalise?

```
Five limitations bounding the synthesis statement, ordered by interpretive importance:

(1) Single climate realisation. Both chains used a single DestinE Climate DT SSP3-7.0 IFS-NEMO realisation. Interannual variability in extreme-heat-day frequency (which dominates the Lacertidae signal under S3a) cannot be separated from forced trend on a single realisation. Cross-realisation ensemble would refine the constellation's quantitative statements about decadal direction and tail behaviour.

(2) Cross-taxon generalisation. Two taxa (Bombus, Lacertidae) is a small cross-taxon sample. The constellation conclusion ("mechanism class transfers but predictions are prior-conditional") is supported by these two cases but should be re-tested as further taxa join the constellation. Candidate next-taxon chains: amphibians (Iberian Salamandridae / Discoglossidae), other diurnal heliotherms (Iberian Anguidae if their physiology is in scope), other warm-adapted insects (Iberian Apidae beyond Bombus).

(3) Family-level priors. Both replications used family-level priors as the baseline. The Lacertidae chain explicitly flagged species-specific T_b (Iberian Podarcis / Iberolacerta / Timon) as deferred to a future iteration; the Bombus chain similarly used family-level GLMM coefficients rather than species-specific refits. Constellation-level conclusions about prior-conditional behaviour would tighten under species-specific refinement.

(4) DestinE-horizon limit. The 2020-2039 archive coverage does not extend to Sinervo's 2050 / 2080 headline-year projections nor to the multi-decadal climate-trajectory regimes where both source papers' mechanisms ramp up. The constellation's statement that "mechanism does not trigger at near-term horizons" is honest for the reachable archive but does not preclude triggering at longer horizons. Re-running the constellation against an expanded DestinE archive when 2050+ becomes available is the natural follow-up.

(5) Sub-daily climate-twin access. Sinervo SOM Equation S2 is operationally daily-Tmax-based, but the mechanism's underlying physiology is intra-day (basking-window thermal restriction). The Polytope sub-daily probe across both chains returned "credentials absent — fallback unused" status; the sinusoidal Tmin-Tmax diurnal-cycle reconstruction was scoped but not exercised. If sub-daily access becomes available, the lizards mechanism may activate at lower compound-prior thresholds than reported here.
```

### Completion date (date picker, required)

```
2026-05-16
```

### Supporting sources (repeatable group, required ≥1)

Each entry is a URL — typically the FORRT Outcome URIs being synthesised. Pull from `nanopubs/PUBLISHED.md` (and/or registries from sibling repos).

- _Source URL 1 (Lizards Outcome from this chain):_ `TODO_PASTE_STEP_05_OUTCOME_URI`
- _Source URL 2 (Bombus apex Synthesis-level Research Synthesis):_ `https://w3id.org/sciencelive/np/RA5TJVZ0_5Knzxd4OtOoZgO6ZspWHwVCSLWNNd7V9H6QQ` — aggregates the three Iberian Bombus chains. Synthesizing across this URL (rather than across the three individual Bombus Outcomes) preserves the chain-internal hierarchy: the Bombus constellation already synthesised itself at the family level, and this cross-taxon Synthesis synthesises across that family-level Synthesis plus the lizards Outcome.
- _Source URL 3 (Bombus apex Synthesis-level CiTO Citation):_ `https://w3id.org/sciencelive/np/RA1q6c0fG2bMbiozF8Az2UpIfzAzqp8hoVEl6QIzfUpH8` — the CiTO that asserts the Bombus apex Synthesis `cito:qualifies` Soroye 2020. Included as a supporting source because the constellation conclusion's framing depends on it (the "mechanism is substrate-robust at fit time but grid-coupled at projection time" finding lives in that CiTO's `personal comment` field; the constellation Synthesis quotes this verbatim in the conclusion above).
- _Source URL 4 (this chain's Lizards Research Software nanopub):_ `TODO_PASTE_STEP_07_RESEARCH_SOFTWARE_URI` — included for FAIR4RS-compliant constellation provenance (the software artefact that produced the Lizards Outcome).
- _Source URL 5 (Bombus chain-1 Research Software):_ `https://w3id.org/sciencelive/np/RAKH9XeZn3CUr9WaFKMC3O2pT_HJJ96c3jTa6v6dWEE3c` — same FAIR4RS provenance for the canonical Bombus chain.
- _Source URL 6 (Bombus chain-2 Research Software):_ `https://w3id.org/sciencelive/np/RA-GY814xxcpEsUWozEJKHGG39bDV8gkbor7OhX8QpVPE`
- _Source URL 7 (Bombus chain-3 Research Software):_ `https://w3id.org/sciencelive/np/RAfdV1yB1JksVJ7dJYwECRHVMhNzbGcjUAa6UreqG_fM4`

### Search topics (Wikidata) (multi-select, optional)

Provide labels (not QIDs).

- _Label 1:_ thermal physiology
- _Label 2:_ climate change ecology
- _Label 3:_ Iberian Peninsula
- _Label 4:_ Lacertidae
- _Label 5:_ Bombus
- _Label 6:_ Destination Earth
- _Label 7:_ HEALPix
- _Label 8:_ FAIR data
- _Label 9:_ Open Science
- _Label 10:_ replication study

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 08.

## Drafting notes (not part of the nanopub)

- **Cross-taxon scope is the locked decision** — the Synthesis aggregates Bombus + Lizards, NOT just the lizards chain. The single-chain apex is the lizards Outcome itself; the cross-taxon apex is THIS Synthesis. Both layers are legitimate.
- **Hierarchical synthesis structure** — this Synthesis aggregates across the Bombus apex Synthesis (`RA5TJVZ0…`) + the Lizards Outcome (TBD). It does NOT re-aggregate the three individual Bombus Outcomes (that's what the Bombus apex Synthesis already did). Preserving the chain-internal hierarchy keeps the citation graph clean.
- **Honest framing — mechanism is not novel; cross-taxon transfer is what we test.** The conclusion attributes both mechanisms to their source papers (Soroye 2020 TEI; Sinervo 2010 h_r). The recommendations attribute the rare-species caveat to established literature (Lobo 2007; Hurlbert & Jetz 2007). The constellation-level recommendation #4 (publish cross-taxon constellations) is methodologically advocated as a pattern, not a novel methodological contribution.
- **Vocabulary** — "local extinction" / "local extirpation" used interchangeably across the two source papers (Sinervo uses "local extinction"; Soroye uses "local extirpation"). The Synthesis conclusion preserves both terms where they appear in source-paper contexts but the constellation-level synthesis statement defaults to "local extirpation/extinction" with the slash explicit so neither source vocabulary is misrepresented.
- **CITATION.cff cross-link** — the Bombus Research Software URIs (`RAKH9X…`, `RA-GY814…`, `RAfdV1y…`) come from CHAIN_SUMMARY.md. Verify against each sister repo's `nanopubs/PUBLISHED.md` before publishing this Synthesis.
- **TODO placeholders** — three `TODO_PASTE_*` fields (Outcome URI, Research Software URI). Publish the lizards Outcome (step 05) and Research Software (step 07) first; then come back to this draft and paste the URIs in before publishing.
