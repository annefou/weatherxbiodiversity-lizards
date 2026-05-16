# 02 — AIDA Sentence

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"AIDA Sentence — Make structured scientific claims following the AIDA model"*

## Field-by-field draft

### AIDA sentence (textarea, required)

Atomic, Independent, Declarative, Absolute. One empirical finding. Must end with a full stop.

> The Quote in step 01 (Sinervo 2010 page 894 column 3) describes the *mechanism* (h_r → metabolic constraint → population decline → extinction risk). The AIDA below is the *single atomic empirical finding* the mechanism supports — the one this replication tests.

```
Heliothermic lizard populations experience local extinction when the cumulative daily hours of activity restriction during the critical reproductive period (h_r, computed as the hours per day when operative temperature exceeds the species' preferred body temperature) exceed a family-specific threshold.
```

### Select related topics/tags (dropdown, optional)

Predefined topic vocabulary — list the labels you intend to pick from the dropdown.

```
thermal physiology
lizards (Lacertidae)
climate change ecology
species distribution
local extinction
```

### Relates to this nanopublication (text input, required)

URI of the nanopub the AIDA derives from. For this paper-rooted chain: the Quote-with-comment URI (from step 01).

Pull the URI from `nanopubs/PUBLISHED.md` once step 01 is published.

```
TODO_PASTE_STEP_01_QUOTE_URI
```

### Supported by datasets (repeatable group, optional)

DOIs/URLs of datasets that ground the AIDA claim.

- _DOI 1:_ `https://doi.org/10.15468/dl.rh4rfn` (GBIF Lacertidae × Iberia occurrence download, 136,210 records, the empirical support for the Iberian-Lacertidae scope of the AIDA)

### Supported by other publications (repeatable group, optional)

DOIs/URLs of publications that support the AIDA claim — e.g. peer-reviewed methods papers, or the original paper if not already cited via the Quote.

- _DOI 1:_ `https://doi.org/10.1126/science.1184695` (Sinervo et al. 2010 — the paper from which the AIDA is extracted; cited explicitly here as the support for the threshold-calibration component)

> **Known platform bug (2026-04-26):** if both *Supported by datasets* AND *Supported by other publications* are populated and publishing fails, fall back to publishing this AIDA via Nanodash. The URI namespace becomes `https://w3id.org/np/...` (still valid and citable).

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 02.

## Drafting notes (not part of the nanopub)

- **Atomicity check** — the sentence states *one* empirical finding (h_r-threshold-exceedance → local extinction). It does NOT bundle the second mechanism layer ("h_r → metabolic constraint → population decline"), even though the Quote does — those are properly *evidence for the mechanism*, not separate empirical findings to be tested.
- **Absoluteness** — "heliothermic lizards" is the universal-form scope; Lacertidae specifically is the *test taxon* for the replication, which lives in step 04 Study and step 05 Outcome (not in the AIDA).
- **Honest framing** — the mechanism is NOT novel (same class of thermal-niche-exceedance mechanism as Soroye et al. 2020 for *Bombus*). The AIDA states the Sinervo finding as a testable proposition; the replication's novelty is the cross-taxon application, not the mechanism itself.
