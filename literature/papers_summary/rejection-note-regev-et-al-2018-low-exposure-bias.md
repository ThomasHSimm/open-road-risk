# Literature Rejection Note: Regev et al. (2018)

- **Citation:** Regev, S., Rolison, J. J., & Moutari, S. (2018). Crash risk by driver age, gender, and time of day using a new exposure methodology. *Journal of Safety Research*, 66, 131–140. https://doi.org/10.1016/j.jsr.2018.07.002
- **Rejection date:** 2026-05-11
- **Source PDF filename:** Crash_risk_by_driver_age__gender__and_time_of_day_using_a_new.pdf
- **Country / context:** Great Britain, STATS19 data 2002–2012, driver-population level analysis

**Reason for exclusion:**

The paper's core contribution — demonstrating that conventional crash rates overestimate risk for low-exposure driver groups (young, elderly, nighttime) due to the non-linear crash-exposure relationship — is theoretically relevant but not actionable for Open Road Risk. The adjusted exposure metric (Equations 2–4) is designed for driver-group comparisons using trip numbers and licensed driver counts, not for link-level SPF estimation. The underlying theoretical point (non-linear SPF means crash rates are biased at low exposure) is already covered more directly and in a more implementable form by Mensah & Hauer (1998), whose correction factor w applies to the SPF fitting problem that Open Road Risk actually faces. No repo actions arise from this paper that are not already captured by Mensah & Hauer or Qin et al. (2006).

**Tags:** low-mileage-bias, exposure-nonlinearity, driver-population-level, GB-STATS19, superseded-by-mensah-hauer-1998
