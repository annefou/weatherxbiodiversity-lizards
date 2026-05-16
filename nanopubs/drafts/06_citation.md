# 06 — CiTO Citation

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Description:** *"Declare citations between papers or other works, using Citation Typing Ontology"*

## Field-by-field draft

### Identifier for the citing creative work (text input, required)

URI of the Outcome published in step 05. Pull from `nanopubs/PUBLISHED.md`.

```
TODO_PASTE_STEP_05_OUTCOME_URI
```

### List citations (repeatable group, required ≥1)

This Outcome cites **two** prior works — the original paper being replicated AND the apex Synthesis-level CiTO of the Bombus constellation (the sister chain whose workflow this replication transfers cross-taxon, per `nanopubs/imported/CHAIN_SUMMARY.md`).

#### Citation 1 — back to Sinervo et al. 2010 (the original paper)

##### Citation Type (dropdown)

```
extends
```

**Rationale (locked-decision-5 framing):** `cito:extends` rather than `confirms` / `qualifies` / `disputes`. The replication's Outcome cannot speak to Sinervo's headline 24 % (2050) / 46 % (2080) Lacertidae projections directly because the Destination Earth Climate DT archive does not reach those horizons. What we *can* speak to is the mechanism's behaviour at 2020-2039 horizons, applied to a different taxon (Iberian Lacertidae rather than the empirical Mexican Sceloporus core or the global 34-family projection), with a sensitivity matrix that surfaces prior-conditional behaviour. This is properly a *cross-taxon × new-horizon × FAIR-workflow extension* of the source paper, not a verdict on its headline number — `extends` captures that scoping honestly.

##### DOI or other URL of the cited work (text input)

```
https://doi.org/10.1126/science.1184695
```

#### Citation 2 — to the Bombus constellation apex CiTO Citation

##### Citation Type (dropdown)

```
extends
```

**Rationale:** the Bombus apex Synthesis-level CiTO (URI below) is the apex of three sibling FORRT chains (`weatherxbiodiversity-projection`, `…-nside128`, `…-substrate-sensitivity`) that tested the *same class of mechanism* (thermal-niche exceedance under climate warming → local extirpation) on Iberian *Bombus* under the same DestinE Climate DT SSP3-7.0 archive. This lizards Outcome explicitly extends that workflow cross-taxon to Iberian Lacertidae under the Sinervo 2010 h_r operationalisation. The `cito:extends` relation signals workflow-and-evidence transfer; the relationship to Sinervo (citation 1 above) signals the source-paper-and-mechanism transfer. Both extensions are independently meaningful; both go in the same CiTO nanopub because both have the lizards Outcome as the citing creative work.

##### DOI or other URL of the cited work (text input)

```
https://w3id.org/sciencelive/np/RA1q6c0fG2bMbiozF8Az2UpIfzAzqp8hoVEl6QIzfUpH8
```

#### Additional citations (optional)

If the Outcome cites methods papers, related replications, or upstream tools, add them here.

- **Type:** `citesAsAuthority` → **URL:** `https://doi.org/10.1146/annurev.ecolsys.36.102003.152636` (Lobo et al. 2007 — rare-species ranking grid-coupling caveat, cited explicitly in the Outcome's `hasLimitationsDescription` as established literature, not a novel finding of this work)
- **Type:** `citesAsAuthority` → **URL:** `https://doi.org/10.1111/j.0906-7590.2007.04881.x` (Hurlbert & Jetz 2007 — same caveat, complementary literature citation)

> **Note:** verify the Lobo 2007 / Hurlbert & Jetz 2007 DOIs against the actual papers before publishing — these are best-recollection DOIs and have not been verified against a live resolver in this draft. If the platform's CiTO dropdown does not include `citesAsAuthority`, fall back to `cites` and note the intent in any free-text field the form provides.

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 06.

This completes the six-step FORRT chain. Optional next layers:

- **Research Software** (`drafts/07_research_software.md`) — the codebase as a citable artefact, cites this chain's Claim back via `cito:usesMethodIn` style one-way reference.
- **Research Synthesis** (`drafts/08_synthesis.md`) — the **cross-taxon constellation** Synthesis aggregating the Iberian Bombus chains + this lizards chain (the "Mediterranean climate-extirpation constellation"). The Synthesis is the chain apex for the constellation, not for this chain alone.

## Drafting notes (not part of the nanopub)

- **`cito:extends` is the locked decision-5 relation** for the Sinervo citation. Do NOT change to `confirms` / `qualifies` / `disputes` even if a reviewer suggests it: the DestinE-horizon constraint makes those framings dishonest.
- **The two `extends` citations are intentional** — Sinervo (the source-paper extension) and the Bombus apex CiTO (the workflow-and-constellation extension). Both are valid; both go in this CiTO nanopub. The Bombus extension is what makes the Outcome composable with the constellation Synthesis (step 08).
- **`replicates` is NOT in the Science Live CiTO dropdown** per the form's note (despite existing in upstream CiTO). For our case `extends` covers the intent without needing `replicates`.
- **Honest framing — rare-species caveat citations** are framed as `citesAsAuthority` to make explicit that the Outcome's `hasLimitationsDescription` paragraph on rare-species ranking is invoking established literature (Lobo 2007, Hurlbert & Jetz 2007), not asserting a novel finding of this work.
