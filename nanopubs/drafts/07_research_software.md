# 07 — Research Software (optional)

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Scope check:** Research Software nanopubs are normatively for reusable software artefacts — tools people would `pip install` or `git clone` to use in their own work, NOT one-off demo / reproduction repos (`CLAUDE.md` § Layered architecture). This is a reproduction repo. Publishing a Research Software nanopub for it is nonetheless consistent with the Bombus sister-chain precedent (`weatherxbiodiversity-projection` published `RAKH9X…` for its codebase; `…-nside128` and `…-substrate-sensitivity` each published their own). The published artefact here describes the Lacertidae replication codebase as a citable, version-pinned snapshot — what someone would cite if they were re-running OUR Outcome at a future DestinE archive expansion or under different lizard-biology priors.

**Form heading:** *"Research Software — Describe research software with metadata including repository, supporting publications, and related resources."*

## Field-by-field draft

### URI of published software (text input, required)

Zenodo concept DOI URL when available, or a GitHub URL. Full URL form.

> Pending Phase 4 Zenodo mint. Until then, use the GitHub URL as a placeholder; replace with the Zenodo concept DOI URL (`https://doi.org/10.5281/zenodo.XXXXXXXX`) BEFORE publishing this nanopub.

```
TODO_ZENODO_DOI_URL — Phase 4 release will mint this. Until minted, paste the GitHub URL: https://github.com/annefou/weatherxbiodiversity-lizards
```

### Software Title (text input, required)

The full name or title of the software.

```
weatherxbiodiversity-lizards — Iberian Lacertidae h_r mechanism replication under Destination Earth Climate DT
```

### Repository URL (text input, required)

```
https://github.com/annefou/weatherxbiodiversity-lizards
```

### Research Project (text input, optional)

URI of the FORRT Claim or PCC question this software is associated with — pull from `nanopubs/PUBLISHED.md`. This is the back-link to the FORRT chain.

```
TODO_PASTE_STEP_03_CLAIM_URI
```

### License (text input, optional)

```
https://spdx.org/licenses/MIT.html
```

### Related Datasets (repeatable group, optional)

Input data DOIs (Zenodo data records, dataset DOIs, ESA product DOIs).

- _Dataset URL 1:_ `https://doi.org/10.15468/dl.rh4rfn` (GBIF Lacertidae × Iberia occurrence download, 136,210 records, CC-BY-NC-4.0 per individual GBIF datasets)
- _Dataset URL 2:_ `https://doi.org/10.6084/m9.figshare.9956471` (Soroye 2020 Figshare deposit — CRU TS 3.24.01 historical Tmax / Tmin, reused as the diurnal-cycle baseline)
- _Dataset URL 3:_ DestinE Climate Digital Twin SSP3-7.0 IFS-NEMO t2m, accessed via Polytope from `https://polytope.lumi.apps.dte.destination-earth.eu` (no public dataset DOI; access governed by DestinE Data Lake terms)

### Related Publications (repeatable group, optional)

One-way back-links to the FORRT Outcome URI(s) the software implements, plus any cited methods papers.

- _Publication URL 1 (FORRT Outcome from step 05):_ `TODO_PASTE_STEP_05_OUTCOME_URI`
- _Publication URL 2 (source paper):_ `https://doi.org/10.1126/science.1184695` (Sinervo et al. 2010 — the paper whose h_r mechanism this software operationalises)
- _Publication URL 3 (Bombus sister-chain Research Software nanopub):_ `https://w3id.org/sciencelive/np/RAKH9XeZn3CUr9WaFKMC3O2pT_HJJ96c3jTa6v6dWEE3c` (the canonical `weatherxbiodiversity-projection` Research Software nanopub — this lizards software is its cross-taxon analogue and explicitly shares its env / pinning / HEALPix-nside=128-NESTED / Snakefile-DAG conventions)

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 07.

## Drafting notes (not part of the nanopub)

- **Phase 4 gating** — this nanopub cannot be published as final until the Zenodo concept DOI is minted (Phase 4 GitHub release triggers Zenodo). The `TODO_ZENODO_DOI_URL` placeholder is the only field that needs a Phase-4 swap; everything else (title, repo URL, license, datasets, related pubs) is publish-ready now.
- **Layered-architecture compliance** (`CLAUDE.md`) — the Related Publications back-link to the FORRT Outcome URI is a one-way reference: Research Software cites the FORRT chain, NOT the other way around. The FORRT chain's nanopubs (Claim, Study, Outcome, CiTO) MUST NOT reference this Research Software URI in their citations.
- **Bombus precedent** — publishing this nanopub even though the repo is "demo-only" by the strict scope check follows the Bombus chain pattern (`weatherxbiodiversity-projection` published its Research Software nanopub `RAKH9X…`). The constellation-level consistency is the operational reason; the FAIR4RS rationale is that each citable software release should have a citable nanopub describing it.
- **Honest framing** — the software title explicitly says "replication", not "novel framework". The software's contribution is the operationalisation of an existing mechanism, not the mechanism itself.
