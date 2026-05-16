# Paper summary

> This is a working scratchpad for the paper-analysis phase. The output of this file feeds the Quote / AIDA / Claim drafts. It is not itself a nanopub.

**Reference paper:** Erosion of Lizard Diversity by Climate Change and Altered Thermal Niches

**DOI:** 10.1126/science.1184695

**Authors:** Barry Sinervo, Fausto Méndez-de-la-Cruz, Donald B. Miles, Benoit Heulin, Elizabeth Bastiaans, Maricela Villagrán-Santa Cruz, Rafael Lara-Resendiz, Norberto Martínez-Méndez, Martha Lucía Calderón-Espinosa, Rubi Nelsi Meza-Lázaro, Héctor Gadsden, Luciano Javier Avila, Mariana Morando, Ignacio J. De la Riva, Pedro Victoriano Sepulveda, Carlos Frederico Duarte Rocha, Nora Ibargüengoytía, César Aguilar Puntriano, Manuel Massot, Virginie Lepetz, Tuula A. Oksanen, David G. Chapple, Aaron M. Bauer, William R. Branch, Jean Clobert, Jack W. Sites Jr.

**Year:** 2010

**Journal / venue:** *Science* 328 (5980): 894–899, 14 May 2010.

## Headline claim

The mechanism-anchored sentence that this replication tests. Verbatim from the paper PDF (page 894, column 3, introductory paragraph).

> "However, hours of restriction (h_r) in thermal refuges limit foraging, constraining costly metabolic functions like growth, maintenance, and reproduction, thereby undermining population growth rates and raising extinction risk."

Character count: 227 / 500. Verbatim from page 894 column 3, second paragraph of the main text (the paragraph that introduces the h_r mechanism). Note: the paper sets the subscript "r" of h_r in italics in the original typesetting; we render it as "h_r" in plain text — every other character is preserved including the parenthetical, the comma series, and the "thereby" punctuation.

## Methodology summary

- **Data sources — empirical (Mexican Sceloporus) component:** Resurvey of 48 Mexican *Sceloporus* lizard species at 200 sites originally censused in 1975–1995; resurveys conducted 2002–2008. Sites were limited to those with intact habitat to exclude habitat-modification confounds. Authors quadrupled sampling effort relative to historical surveys to reduce false extinctions. 99 Mexican weather stations provided historical *T*<sub>max</sub> from 1973–2008, plus parametric climate surfaces (table S3).
- **Data sources — global-projection component:** N=1216 geo-referenced *T*<sub>b</sub> records (587 species across 34 lizard families) compiled from the literature via Google Scholar. WorldClim 1.4 surfaces at 10 arc-minute resolution provided *T*<sub>max</sub> for 1975, 2020, 2050, and 2080 under three IPCC AR3 scenarios (CCCMA, HADCM3, CSIRO a2a; figures present CCCMA a2a). NOAA temperature trends (1200 km smoothing) were used as cross-validation; the European Climate Assessment database (324 stations) was used to refine *T*<sub>max</sub> over Europe.
- **Mechanism — *hours of restriction* (*h<sub>r</sub>*) model:** *h<sub>r</sub>* is defined as the cumulative hours per day when operative temperature *T*<sub>e</sub> exceeds the species' preferred body temperature *T*<sub>b,preferred</sub> (for *S. serrifer*, *T*<sub>b,preferred</sub> = 31°C; ground-truthed at 4 Yucatán sites using grey-painted PVC-pipe operative-temperature models attached to HOBOTEMP loggers, January–May 2009). The operational regression linking *h<sub>r</sub>* to weather-station *T*<sub>max</sub> is Equation S2: **h_r = 0.74 × (T_max − T_b) + 6.1**, computed daily over the critical reproductive period (2 months in the temperate zone, 5–6 months in the wet–dry tropics, 12 months in the equatorial zone). A site is declared extinct in year *Y* if the cumulative *h<sub>r</sub>* over that reproductive window exceeds a family-specific threshold *h̄<sub>r,family</sub>* (Table 1 of the paper). The threshold is calibrated per family by iteratively varying *h<sub>r</sub>* until 95% of populations in that family are extant in the 1975 baseline.
- **Statistical model:** Logistic regression of binary extinct/extant outcomes against Δelevation, Δlatitude, Δlongitude, reproductive mode (oviparous vs viviparous), *T*<sub>b</sub>, *T*<sub>air</sub>; phylogenetic-independent-contrast (PIC) regressions on a Sceloporine super-tree to control for shared ancestry. Goodness-of-fit χ² tests compare observed vs predicted extinctions at the calibrated *h<sub>r</sub>*.
- **Sample sizes:** 48 Mexican *Sceloporus* species at 200 sites (empirical); 24 observed local extinctions = 12% of resurveyed sites by 2009 (Table S1). Global projection covers 34 families, N=1216 geo-referenced sites, N=587 species. Cross-continental validation: Lacertidae N=46 (broader N=117) European *Lacerta vivipara* sites; Liolaemidae N=3155 South American sites; Cordylidae+Gerrhosauridae N=165 African sites + N=122 Madagascar; *Egernia* group N=2841 Australian sites.
- **Time windows:** baseline 1975, observed 2009, projections 2050 and 2080.
- **Headline numerical results (to be compared against the replication):**
  - 12% of Mexican *Sceloporus* sites locally extinct by 2009 (24 of 200) — empirical, page 894.
  - 4% of local populations worldwide already extinct by 2009 — projection-validated, page 894 abstract.
  - 39% local extinctions worldwide projected by 2080 (assuming 1-month reproductive shift in temperate zones; rises to 40% without shift) — page 894 abstract; supporting global average 30% by 2080 (page 897).
  - **6% global species extinction by 2050; 20% global species extinction by 2080** (paper's conclusion sentence, page 897) — these are the famous headline numbers.
  - 58% Mexican *Sceloporus* species-level extinction by 2080 (paper page 895).
  - Family-specific Lacertidae projections (Table 1): local extinction 0.034 (2009) → 0.241 (2050) → 0.460 (2080); species extinction 0.085 (2050) → 0.420 (2080).
  - **Mechanism threshold for Sceloporus (Mexican calibration): *h<sub>r</sub>* = 3.85 h** during March–April critical reproductive period (SOM page 4); global mean *h̄<sub>r</sub>* = 4.55 h across heliotherms (Fig. 3 caption); **Lacertidae-specific *h<sub>r</sub>* = 3.1 h (Table 1)**.

### Thermal-physiology priors from the SI

These are the per-species or per-family parameters the model consumes. Every entry on this list will need an Iberian-Lacertidae source in Phase 2.

| Parameter | Symbol | SI source / role | Species × parameter coverage in original |
|---|---|---|---|
| Mean activity body temperature | *T*<sub>b</sub> | Mean ± SE per family (Table 1); per-species records in Table S4 / Table S6 | N=1216 geo-referenced records, N=587 species, 34 families |
| Preferred body temperature | *T*<sub>b,preferred</sub> | Laboratory thermal-gradient measure; rare in the literature, so substituted by *T*<sub>b</sub> when missing (SOM page 4) | N=151 records where both *T*<sub>b</sub> and *T*<sub>b,preferred</sub> measured (R² = 0.587) |
| Critical thermal maximum | CT<sub>max</sub> | Death threshold; used in PIC analysis of Phrynosomatidae and in the alternative *T*<sub>e</sub> > CT<sub>max</sub> formulation rejected by the authors (SOM Fig. S4C) | N=11 Phrynosomatidae (Table S5); broader but sparse across other families |
| Operative temperature | *T*<sub>e</sub> | Ground-truth via PVC-pipe HOBOTEMP models in Yucatán; calibrates the *h<sub>r</sub>* regression | 4 Yucatán sites only (2 persistent, 2 extinct *S. serrifer*) |
| Calibrated activity-restriction threshold | *h̄<sub>r,family</sub>* | Family-specific extinction threshold in Table 1 | 34 families; Lacertidae value = 3.1 h |
| Body-temperature range | *T*<sub>b</sub> range | Per-family lower/upper bound in Table 1 | 34 families; Lacertidae = 26.7–40.2°C |
| Mean maximum air temperature occupied | *T̄*<sub>max</sub> | Per-family climate envelope in 1975 (Table 1) | 34 families; Lacertidae = 25.6°C |
| Mode of thermoregulation | — | Heliothermic / forest thermoconformer / leaf-litter thermoconformer / fossorial / nocturnal — drives whether the *T*<sub>e</sub> > *T*<sub>b</sub> formulation or the *T*<sub>air</sub> > *T*<sub>b</sub> formulation is applied (SOM page 11) | All 34 families classified; Lacertidae = Heliothermic |
| Reproductive mode | — | Oviparous vs viviparous; affects logistic regression weighting | All 48 Mexican species classified; Lacertidae mixed (*L. vivipara* is viviparous) |
| Critical reproductive months | — | Latitude-dependent window over which *h<sub>r</sub>* is integrated (March–April at 24° lat → June–July at 60° lat; 2 months temperate, 5–6 months wet-dry tropics, 12 months equatorial) | Per-zone, not per-species |
| Lay date heritability | *h²* | Sets the rate of evolutionary tracking of reproductive timing under climate change (used in 38% vs 39% sensitivity test) | *h²* = 0.17 from *Sceloporus occidentalis* lab estimate (paper page 895) |

For Iberian Lacertidae, the family-level Table 1 row already gives a starting point (*T̄*<sub>b</sub> = 35.4 ± 0.31, *T̄*<sub>max</sub> = 25.6, *h<sub>r</sub>* = 3.1, n = 89, n_spp = 279), but Iberian-specific *T*<sub>b</sub> records and reproductive timing will need to be sourced — likely from the Spanish herpetological literature (e.g. Carretero et al., Monasterio et al.) and the European Climate Assessment.

## Replication design choice

- [ ] **Reproduction Study** — direct reproduction: same methodology, same tools.
- [x] **Replication Study** — replication with different methodology or conditions.
- [ ] **Reproduction/Replication Study** — both.

**Justification.** This work applies Sinervo et al.'s *h<sub>r</sub>* mechanism to a different taxon (Iberian Lacertidae rather than the Phrynosomatidae empirical core or the global 34-family projection), a different climate-data product (Destination Earth Climate Digital Twin, which exposes ~5 km daily fields, instead of WorldClim 1.4 at 10 arc-minute resolution backed by NOAA / European Climate Assessment for cross-validation), and a different time horizon set (the 2020s and 2030s, the only horizons DestinE currently exposes — neither 2050 nor 2080 is reachable). The mechanism (*h<sub>r</sub>* in activity during the critical reproductive period → demographic collapse → local extinction) is held fixed; what changes is the parameterisation (Iberian-Lacertidae thermal-physiology priors), the climate forcing (a digital twin, not statistically-downscaled IPCC AR3 scenarios), and the spatial resolution. This is therefore a **Replication Study** under the FORRT three-type vocabulary, not a Reproduction Study. The CiTO relationship to the original paper will be `extends`, not `confirms` or `disputes` directly, because the replication tests a transfer of the mechanism rather than re-running the original analysis.

## Notes for downstream drafts

- **Where the mechanism is stated.** The mechanism sentence in the introductory paragraph of the main paper (page 894, column 3) is the cleanest verbatim source for the Quote — it states the physiological causal chain directly. The full operational definition of *h<sub>r</sub>* (as *T*<sub>e</sub> > *T*<sub>b,preferred</sub> cumulative hours over a 2-month critical reproductive period) is *only* spelled out in the SOM (pages 3–5), not in the main paper. The main paper says "hours of restriction" but does not give the formula. This means the AIDA and Claim drafts (steps 02 and 03) can quote the main paper for the mechanism statement, but Phase 2 code must implement the SOM definition.
- **Extinction vs extirpation vocabulary.** The paper does **not** rigorously distinguish "extinction" from "extirpation". It uses "local extinction" (population-level loss at a site) and "species extinction" (range-wide loss) as the two scales, and maps the relationship between them in Table S8. The 6%/20% headline numbers refer to **species extinction**; the 4%/16%/30%/39% numbers refer to **local extinction**. Downstream drafts (Claim, Study, Outcome) MUST use the paper's "local extinction" / "species extinction" pair and avoid the word "extirpation" to keep vocabulary aligned with the source.
- **Threshold universality.** The activity-restriction threshold *h<sub>r</sub>* is **family-specific**, not universal. Table 1 of the paper lists a different *h<sub>r</sub>* for each of the 34 lizard families (Lacertidae = 3.1, Phrynosomatidae = 7.0 in the table — note this is the calibrated family value, distinct from the 3.85 h Sceloporus-genus value used for the Mexican empirical calibration). This means Iberian Lacertidae **can** be parameterised under the original mechanism: the Lacertidae family-level *h<sub>r</sub>* = 3.1 h, *T̄*<sub>b</sub> = 35.4°C, *T̄*<sub>max</sub> = 25.6°C from Table 1 supply a defensible starting point, but the Iberian-specific *T*<sub>b</sub> distribution is likely warmer than the family mean (which is dominated by the boreal *Lacerta vivipara*). Phase 2 needs to confirm whether to re-calibrate *h<sub>r</sub>* for the Iberian subset using the same 95%-of-populations-extant-in-1975 procedure, or to inherit the Table 1 value verbatim.
- **DestinE horizon limit.** DestinE Climate DT does not currently expose 2050 or 2080; the closest reachable horizons are the 2020s and 2030s. The Quote and AIDA must therefore avoid anchoring on the 2080 numbers — see the Quote-anchoring constraint in the agent brief. The Outcome (step 05) will explicitly call out that the replication's horizon mismatch precludes a direct test of the headline 6%/20% projections.
- **WorldClim vs DestinE — climatology baseline.** Sinervo et al.'s 1975 baseline is an interpolated WorldClim climatology, not station data; the rate of change is a linear interpolation between 1975 and 2020 WorldClim layers, cross-checked against NOAA 1200 km maps. DestinE provides a higher-resolution, model-derived climate-twin field. The Outcome drafting must acknowledge that this is not a like-for-like climate comparison.

## Quote alternatives considered

In case Anne prefers a different mechanism anchor:

- **Alt 1 (selected):** "However, hours of restriction (h_r) in thermal refuges limit foraging, constraining costly metabolic functions like growth, maintenance, and reproduction, thereby undermining population growth rates and raising extinction risk." — page 894, column 3. Mechanism-direct, 234 chars.
- **Alt 2:** "Lizards retreat to cool refuges rather than risk death by overheating." — page 894, column 3 (sentence preceding Alt 1). Shorter (69 chars), states the behavioural mechanism, but does not name *h<sub>r</sub>* or extinction risk. Reads more like a framing statement than a causal claim.
- **Alt 3:** "Therefore, our findings indicate that lizards have already crossed a threshold for extinctions caused by climate change." — page 894, abstract (also page 897, last line of discussion). Strong empirical claim, 121 chars, but tied to the 2009 observation rather than the mechanism per se; risks committing the replication to defending the threshold-already-crossed framing for a region (Iberian Peninsula) where the replication has not yet measured local extinctions. Less safe than Alt 1.
- **Alt 4:** "Lizards cannot evolve rapidly enough to track current climate change because of constraints arising from the genetic architecture of thermal preference." — page 895, column 2. 154 chars. Stronger as a Claim than a Quote — it asserts a mechanism (low *h²* on *T*<sub>b</sub>) the replication does not test in this iteration.

Alt 1 is the recommended choice and is the version paired with `01_quote.md`.
