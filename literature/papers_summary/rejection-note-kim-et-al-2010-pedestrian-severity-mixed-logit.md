# Literature Rejection Note: Kim et al. (2010)

- **Citation:** Kim, J.-K., Ulfarsson, G.F., Shankar, V.N., & Mannering, F.L. (2010). A note on modeling pedestrian-injury severity in motor-vehicle crashes with the mixed logit model. *Accident Analysis and Prevention*, 42, 1751–1758. https://doi.org/10.1016/j.aap.2010.04.016
- **Rejection date:** 2026-05-11
- **Source PDF filename:** Kim-Ulfarsson-Shankar-Mannering-AAP-2010.pdf
- **Country / context:** North Carolina, USA; police-reported pedestrian-vehicle crashes 1997–2000; 5,808 observations

**Reason for exclusion:**

This is a crash-injury severity application paper — it applies a mixed logit model to individual pedestrian-vehicle crashes to model the probability of fatal vs. incapacitating vs. non-incapacitating vs. no-injury outcomes. The methodological contribution (mixed logit with heterogeneous mean random parameters, capturing age and gender heterogeneity) is superseded as a reference by Savolainen et al. (2011), which reviews the full severity modelling landscape including mixed logit in a more comprehensive and directly citable form.

The specific empirical findings (darkness without streetlights +400% fatal probability, trucks +370%, freeway +330%, speeding +360%) are from a US state dataset with no direct UK transferability. The model operates at the individual crash level and requires per-crash covariates (pedestrian age, vehicle type, alcohol involvement, lighting condition) that are not available in Open Road Risk's link × year feature set.

No repo actions arise from this paper that are not already covered by Savolainen et al. (2011).

**Tags:** severity-modelling, mixed-logit, pedestrian-injury, random-parameters, unobserved-heterogeneity, US-only, crash-level-data, superseded-by-savolainen-2011
