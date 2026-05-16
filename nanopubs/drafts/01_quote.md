# 01 — Quote-with-comment (paper-rooted chains)

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> If this is a question-rooted chain, use `01_pico.md` or `01_pcc.md` instead — see `docs/chain-decision-tree.md`.
>
> **After choosing the chain shape, delete the two step-1 alternates you aren't using.** Once you've decided this chain is paper-rooted and keep `01_quote.md`, run:
> ```bash
> rm nanopubs/drafts/01_pico.md nanopubs/drafts/01_pcc.md
> ```

**Form heading:** *"Annotate a paper quotation — Annotating a paper quotation with personal interpretation"*

## Field-by-field draft

### Cited DOI (text input)

Format: starts with `10.` — bare DOI, **NOT** `https://doi.org/...` form.

```
10.1126/science.1184695
```

### Quote mode (radio button)

- [x] **Quote whole text (less than 500 characters)**
- [ ] Quote start/end *(use this if the quote exceeds 500 chars)*

### Quoted Text (textarea, required)

Verbatim from the paper PDF in `paper/`. Character-for-character. ≤ 500 chars in whole-text mode.

> Verified verbatim from `paper/Sinervo-ErosionLizardDiversity-2010.pdf` page 894, column 3, second paragraph of the main text (the paragraph that introduces the *hours of restriction* mechanism). The paper sets the subscript "r" of *h<sub>r</sub>* in italics in the original typesetting; we render it as `h_r` in plain text. All other characters — punctuation, commas, parentheses, the en-dash-free phrasing — are preserved exactly.

```
However, hours of restriction (h_r) in thermal refuges limit foraging, constraining costly metabolic functions like growth, maintenance, and reproduction, thereby undermining population growth rates and raising extinction risk.
```

Character count: 227 / 500.

### Comment (textarea, required)

Subtitle: *"Our interpretation or explanation of why this quotation is relevant."*

Why this quote matters and what the replication tests. Connect the paper's claim to the work this repo does. Don't repeat the quote.

```
This replication transfers Sinervo et al.'s activity-restriction mechanism from Mexican Sceloporus and the global 34-family projection to the Iberian Lacertidae, using Destination Earth Climate Digital Twin (~5 km, daily) as the climate forcing instead of WorldClim 1.4 and limiting horizons to the 2020s and 2030s — the only windows DestinE currently exposes. The thermal-niche-exceedance mechanism itself is not new: the same physiological logic was applied to bumblebees by Soroye, Newbold, and Kerr (2020, Science), so the novelty of this work lies in the cross-taxon transfer, the application of a kilometre-scale climate digital twin, and the FAIR-by-design publication of every step as a signed FORRT nanopublication chain — not in the mechanism itself. The Outcome will therefore frame the relationship to the original paper as CiTO `extends` rather than `confirms` or `disputes`: we cannot test the famous 2080 species-extinction numbers (DestinE does not reach 2080), so the comparison will be on local-extinction rates over the near-term DestinE horizons, parameterised with Iberian-specific Tb priors.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 01.
