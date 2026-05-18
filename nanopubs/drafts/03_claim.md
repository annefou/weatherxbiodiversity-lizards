# 03 — FORRT Claim

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"FORRT Claim — Declare an original claim according to FORRT, linking it to an AIDA sentence with a specific FORRT type."*

## Field-by-field draft

### Short URI suffix as claim ID (text input, required)

Slug becomes part of the nanopub URI. Use kebab-case.

```
lacertidae-h-r-extinction-mechanism
```

### Label of the claim (text input, required)

A descriptive title (not a sentence). Used for searches/discovery.

```
Sinervo 2010 h_r mechanism for heliothermic lizard local extinction
```

### Search for an AIDA sentence (search/select, required)

URI of the AIDA published in step 02. Pull from `nanopubs/PUBLISHED.md`.

> _If the AIDA was published via Nanodash (`w3id.org/np/...` namespace), the platform's search may not find it — paste the URI manually._

```
https://w3id.org/sciencelive/np/RA7jFaB3akXJH9XhcYkIKL-6svSehDYO-s0VhiNkeFKXQ
```

### Type of FORRT claim (dropdown, required)

Pick one. See `docs/claim-type-vocabulary.md` for the seven options and how to choose.

- [ ] computational performance
- [ ] scalability
- [ ] data quality
- [ ] data governance
- [x] **descriptive pattern**
- [ ] model performance
- [ ] statistical significance

**Rationale:** the claim asserts an empirical relationship between two variables (h_r and local-extinction outcome). Statistical significance was the *evidence* in the original paper (chi-square goodness-of-fit, logistic regression p-values), but the claim itself is about the underlying pattern. Same genre as the Soroye 2020 Bombus analogue in `docs/claim-type-vocabulary.md` (table row 1: "thermal exposure correlates with bumble bee extirpation" → `descriptive pattern`).

### Source URI (text input, optional)

Full URL form: `https://doi.org/...` (NOT bare DOI).

```
https://doi.org/10.1126/science.1184695
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 03.

## Drafting notes (not part of the nanopub)

- **Claim-type confusion to avoid** — *not* `statistical significance` even though Sinervo's calibration used iterative chi-square fitting to derive the family-specific threshold h_r. The claim is the *underlying empirical pattern*; significance was its evidence.
- **Claim-type confusion to avoid** — *not* `model performance` even though the h_r model produces extinction predictions. The model is the *instrument* by which the pattern is observed (per `docs/claim-type-vocabulary.md`: "Empirical relationships discovered by fitting a model are `descriptive pattern` (the model is the instrument; the pattern is the claim)").
- **Honest framing preserved** — the label says "Sinervo 2010 h_r mechanism", explicitly attributing the mechanism to the source paper. The replication does not claim the mechanism as its own contribution.
