# Zero-Calibration Diagnostic

**Method**: Posterior predictive zero check (Pew et al. 2020 / crash-frequency-models.qmd §8).

S = 1000 realisations drawn from the Poisson predictive distribution.
p = proportion of realisations with more zeros than observed (well-calibrated → p ≈ 0.50).

**Diagnostic sample**: 2,000,000 link-years (35,933 with ≥1 collision;
1,964,067 zeros — pure random draw preserving true zero rate from 21,675,570 total).

---

## Poisson GLM result

| Metric | Value |
|--------|-------|
| Observed zeros (Z_obs) | 1,964,067 |
| Simulated mean E[Z_sim] | 1,961,163 |
| Simulated SD[Z_sim] | 183 |
| p-value | 0.000 |
| Observed zero rate | 0.9820 |
| Simulated mean zero rate | 0.9806 |

**Interpretation**: severe misfit — Poisson substantially underestimates the zero count

### Negative Binomial check

| Metric | Value |
|--------|-------|
| MLE converged | YES |
| Warnflag | 0 (0 = clean) |
| Gradient norm at solution | 9.69e-06 |
| Overdispersion α | 2.0569 |
| α SE | 0.0485 |
| α 95% CI | [1.9619, 2.1520] |
| Z_obs | 1,964,067 |
| E[Z_sim] | 1,964,172 |
| p | 0.722 |

NB adequately reproduces the observed zero count (p ≈ 0.5).

---

## Notes

- The diagnostic sample preserves the true zero rate (~98.2%).
  The production Poisson GLM is trained on 1:10 downsampled zeros
  (biased intercept). This check uses an unbiased fit on the diagnostic sample.
- Full dataset: 21,675,570 link-years across 10 years
  (2015–2024).
- Supporting data: `reports/supporting/zero_calibration_z_distribution.csv`
- Summary JSON: `reports/supporting/zero_calibration_summary.json`
