# Hepatic Morphometry in Healthy South Asian Adults

Python re-analysis and extension of a cross-sectional sonographic study of 113
healthy adults aged 18–35, originally analysed in SPSS.

**Umair Ilyas** — B.S. Radiography and Imaging Technology, Green International
University, Lahore ·
[ORCID 0009-0008-2173-6945](https://orcid.org/0009-0008-2173-6945)

---

## Background

Reference standards for hepatic dimensions on routine ultrasound are largely
derived from Western populations. Because organ size scales with body habitus,
applying those standards unmodified to South Asian patients risks systematic
misclassification. This repository re-analyses a cohort scanned at Ali Fatima
Hospital, Lahore, using a 2–5 MHz curvilinear transducer under a standardised
measurement protocol.

## What this repository adds

The published analysis reported descriptive statistics and a sex comparison.
This re-analysis reproduces those results from the raw data and extends them in
four directions:

1. **Verification** — every published statistic is recomputed from source and
   checked automatically against the reported value.
2. **Measurement-quality audit** — each variable is profiled by distinct-value
   count and decimal precision, which distinguishes instrument-recorded
   measurements from estimated ones.
3. **Anthropometric association** — correlations with age, height, weight, BMI
   and body surface area, an analysis the published discussion identifies as
   absent from its own tables.
4. **Predictive modelling** — a regression model with a held-out test set and
   5-fold cross-validation, reported honestly including its poor performance.

## Key results

| Parameter | Recomputed | Published | Match |
|---|---|---|---|
| Right lobe, mean ± SD | 141.28 ± 11.80 mm | 141.28 ± 11.79 mm | ✔ |
| Left lobe, mean ± SD | 51.52 ± 5.00 mm | 51.52 ± 4.99 mm | ✔ |
| Right lobe, F vs M | p = 0.0070 | p = 0.007 | ✔ |
| Left lobe, F vs M | p = 0.0014 | p = 0.001 | ✔ |

All published statistics reproduce from the raw data.

**Anthropometric association (not in the published tables).** Right lobe length
correlates with weight (r = 0.44, p < 0.001), body surface area (r = 0.41),
BMI (r = 0.36) and age (r = 0.29). Left lobe correlates most strongly with
weight (r = 0.51).

**Comparison with Western reference values.** Against Riestra-Candelaria et al.
(2018), this cohort's right lobe is significantly *larger* in both sexes
(female +8.5 mm, p < 0.001; male +3.4 mm, p = 0.033) — evidence that Western
normative ranges do not transfer unchanged to this population.

**Predictive model.** Cross-validated R² ≈ 0.09. Anthropometric variables alone
explain roughly a fifth of the variance in hepatic dimensions, and height and
weight are collinear (r = 0.73), destabilising the coefficients. This is a
negative result and is reported as such: it is direct quantitative support for
moving from 2-D linear measurement to 3-D volumetric estimation.

## Data-quality finding

The audit step distinguishes properly instrument-recorded variables from ones
that are not. Right lobe length has 63 distinct values across 113 participants
with sub-millimetre precision; renal measurements are comparable. Splenic
measurements from the same cohort had only 6 distinct values with no decimal
precision, and were therefore excluded from this analysis rather than reported
as normative data.

## Repository structure

```
.
├── prepare_data.py            # raw spreadsheet -> clean CSV
├── 01_liver_analysis.ipynb    # main analysis
├── data/
│   └── README.md              # data availability statement
├── figures/                   # generated plots and reference-range table
└── requirements.txt
```

## Running the analysis

**Google Colab** — upload the notebook and run the cells top to bottom.

**Locally:**

```bash
pip install -r requirements.txt
python prepare_data.py DATA_SHEET_THESIS.xlsx
jupyter notebook 01_liver_analysis.ipynb
```

## A note on the height column

The raw spreadsheet stores height in feet-inches notation as a decimal: `5.6`
means 5 feet 6 inches, not 5.6 feet. Read naively, heights are wrong by up to
9 cm and BMI by up to 7 units. `prepare_data.py` decodes this and validates the
result against the BMI column computed by hand in the original sheet (maximum
drift 0.10 units).

## Data availability

Raw participant records are not committed to this repository. The dataset carries
no names or medical record numbers, but publication of individual-level records
is subject to the original institutional approval. Aggregate results and derived
reference ranges are reported in full; de-identified data is available on request.

## Related publications

- Batool L, Uzair M, **Ilyas U**, Murtaza G, Khalid A. Frequency of Rotator Cuff
  Abnormalities on Shoulder MRI in Symptomatic Patients of Different Age Groups.
  *Review Journal of Neurological and Medical Sciences.* 2025;3(4):298–309.
  [doi:10.5281/zenodo.16872469](https://doi.org/10.5281/zenodo.16872469)
- **Ilyas U**, Batool L. High-Resolution Sonographic Morphometry of the Adult
  Liver: Establishing Precise Normative Dimensions in Healthy Individuals Aged
  18–35. *Under review.*

## Next steps

- Extend the analysis to the renal measurements in the same cohort
- Compare linear regression against ensemble methods
- Move from 2-D linear measurement toward 3-D volumetric estimation

## Contact

umairilyas780@gmail.com ·
[LinkedIn](https://www.linkedin.com/in/umair-ilyas-53a364244)
