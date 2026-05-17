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
This sentence names the causal chain — refuge time during the reproductive period as the proximate cause of climate-driven local extinction in heliothermic lizards — that the replication tests on Iberian Lacertidae. The mechanism class is not novel: Soroye et al. (2020) applied the same thermal-niche-exceedance logic to bumblebees. The novelty of this work is the cross-taxon transfer and the FAIR-by-design publication of every replication step as a signed FORRT nanopub.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 01.
