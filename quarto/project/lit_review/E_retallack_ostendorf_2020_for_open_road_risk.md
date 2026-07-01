# Summary of Retallack & Ostendorf (2020) for Open Road Risk

## Paper

**Retallack, A. E., & Ostendorf, B. (2020). _Relationship Between Traffic Volume and Accident Frequency at Intersections_. International Journal of Environmental Research and Public Health, 17(4), 1393.**

## Bottom line

This is a useful **supporting methods paper**, not a direct template for Open Road Risk.

It matters because it shows three things clearly:

1. **Traffic exposure is not safely assumed to have a simple linear relationship with collisions.**
2. **Poisson is a reasonable starting point, but overdispersion checks matter and may justify negative binomial models.**
3. **High-temporal-resolution traffic data can reveal risk structure that annual averages can hide.**

For Open Road Risk, the paper is most useful as evidence for:
- testing **non-linear exposure effects**,
- checking whether exposure–collision relationships differ by **road context / family**,
- using **Poisson vs negative binomial diagnostics** carefully,
- and treating **time-of-day exposure profiles** as substantively important rather than cosmetic.

It is **not** direct validation of the current ORR link × year model, offset form, feature set, XGBoost stage, or network-wide ranking output.

## What the paper did

The study analysed **120 intersections in Adelaide, Australia**, using:
- **1629 motor-vehicle accidents** linked to traffic volume data,
- traffic volumes drawn from **more than 5 million hourly measurements**,
- a rainfall analysis,
- and a simple severity comparison.  

The core design was intersection-focused and event-timed:
- accidents were filtered to the study area and period,
- accident times were **rounded down to the previous hour** so the traffic measure would reflect conditions immediately before the crash rather than conditions affected by the crash,
- and traffic volumes were joined to nearby intersections using space and time matching.

Because intersections had different capacities and the authors lacked the detailed lane/signal data needed for standard volume/capacity ratios, they created a **relative congestion index** instead:
- hourly traffic volumes were binned **within each intersection** into **15 quantile-based congestion levels**,
- intersections were also grouped into **three size classes** based on median traffic volume,
- accident counts were then analysed across **3 intersection-size groups × 15 congestion levels**.

For modelling, they compared:
- **Poisson GLMs** first,
- checked for **overdispersion**,
- then used **negative binomial** where Poisson was not adequate,
- and compared **linear, quadratic, and spline** functional forms using **AICc**.

## Main findings

### 1. Collision frequency rose with traffic volume, but not in a purely linear way

The main result is that collision frequency was **approximately linear at lower traffic volumes**, but at the **highest congestion levels** the relationship bent upward and collision frequency increased **faster than linearly**. The authors describe this as a significant **quadratic** effect, with the linear-only model clearly worse than the non-linear alternatives in middle- and high-volume settings.

### 2. The sharpest increase in collisions happened in the most congested conditions

The practical interpretation is straightforward: if a site regularly reaches the highest congestion states, reducing those peak conditions may deliver more safety benefit than the same traffic reduction at lower volumes.

### 3. Rain increased collision risk more in low-congestion conditions than in high-congestion conditions

Rainfall still raised risk, but its **relative effect fell as congestion increased**. At the lowest congestion level, the relative risk in rain was around **five times** the dry risk; by the highest congestion level, the relative risk approached **one**, meaning rain added little extra relative risk once congestion was already very high.

The likely interpretation is not that rain stops mattering, but that in very congested settings the congestion itself dominates the risk picture.

### 4. They did not find a clear severity effect

The paper reports **no significant effect of congestion level on accident severity** in this dataset. But that result is weak for transfer purposes because the study had very few serious-injury crashes and no fatal crashes in scope, and it excluded pedestrians and cyclists.

## Why this is useful for Open Road Risk

## 1. It supports testing exposure shape rather than assuming it

This is the strongest transfer point.

ORR already estimates collisions relative to traffic exposure. This paper is a good reminder that the exposure term may not behave in a globally linear way, especially at the high-flow end. In your project, that does **not** mean dropping the log-exposure-offset approach. It means you should consider whether there is additional structure beyond the offset:
- non-linear exposure effects,
- road-family-specific exposure elasticity,
- or interactions between exposure and road context.

That fits your existing concern that motorways, trunk roads, and other families may behave differently.

## 2. It supports your Poisson / NB diagnostic discipline

The paper does not prove that negative binomial is always the right ORR model, but it does reinforce the workflow:
- start with a count model that matches the problem,
- inspect overdispersion,
- and allow escalation to NB where the variance structure demands it.

That lines up with your existing work around Poisson versus NB / quasi-Poisson reasoning. The transfer here is methodological discipline, not model copying.

## 3. It strengthens the case for temporal exposure detail

The Adelaide paper benefits from **hourly exposure alignment**. ORR is currently a **link × year** model, so you are not using event-time alignment in Stage 2. But the paper still matters because it shows that **temporal structure in traffic exposure can change what relationship you see**.

That supports your use of **WebTRIS-style time-of-day profiles** and suggests there is real value in future ORR work that moves beyond annual exposure only, for example:
- severity-aware temporal modelling,
- time-slice exposure surfaces,
- or event-time analyses for substudies.

## 4. It supports context-specific scaling rather than naive pooling

Their congestion index is crude compared with a full network model, but the idea is good: **the same raw traffic count means different things in different road contexts**.

That is highly relevant to ORR. At network scale, raw AADT does not have the same implication on:
- a motorway,
- an urban A road,
- or a rural minor link.

Your family split is already the more defensible version of this idea. The paper is useful as conceptual backing for that direction.

## 5. It shows the value of parsimonious models when detailed geometry/capacity data are missing

The paper explicitly argues that broad-scale safety modelling often has to work with incomplete design and signal data. That is relevant to ORR because open-data national models always face partial observability. The paper gives some support for using a parsimonious structure where richer variables are unavailable, while also acknowledging the cost: omitted heterogeneity.

That is a good fit with your “open-data, full-network, transparent prototype” positioning.

## What does **not** transfer cleanly to ORR

This is the part worth being strict about.

### 1. Intersection study ≠ link-level validation

The paper is about **intersections**, not general road links. ORR is a **road-link × year** model across a much larger and more heterogeneous geography. So you should not cite this as direct empirical support for your link-level risk scores.

### 2. Hourly event-matched exposure ≠ annual offset exposure

Their exposure logic is about **traffic at the hour of the crash**. ORR currently uses annualised exposure. Those are related, but they are not the same estimand.

### 3. Relative congestion bins are not a substitute for your actual exposure model

Their congestion index is a workaround for missing capacity / directional-flow detail. It is clever, but it is not something ORR should import wholesale. Your network-wide AADT estimation plus road-family stratification is the stronger framework for your use case.

### 4. The severity result is too weak to drive ORR decisions

Because serious injury and fatal counts were thin, and vulnerable road users were excluded, I would not use this paper to justify any strong claim that congestion is or is not related to severity in your project.

## What you should do in Open Road Risk because of this paper

## Priority actions

### 1. Test whether exposure effects vary by road family
Do this if not already explicit in the Stage 2 diagnostics.

The paper’s main lesson is that exposure–collision shape may differ by context. In ORR terms, that means:
- test family-specific AADT elasticity,
- compare residual behaviour by family,
- and inspect whether high-flow roads show systematic under- or over-prediction.

This is one of the cleanest actionable transfers.

### 2. Keep Poisson as the baseline, but make NB comparison explicit
If your current reporting does not already make this very visible, tighten it.

Use the paper as support for:
- Poisson baseline,
- overdispersion checks,
- NB comparison where dispersion suggests it,
- and family-specific dispersion assessment where appropriate.

Do not switch models just because this paper used NB in some strata. Use it as support for the **diagnostic workflow**.

### 3. Treat temporal exposure as a genuine next-step research path
You do not need to rebuild ORR around hourly data now. But this paper strengthens the case for a later branch that asks:
- do links with similar annual AADT but different within-day profiles have different observed collision behaviour?
- does temporal peaking matter for certain road families?
- can a time-sliced exposure proxy improve junction-heavy or urban contexts?

That is a serious extension, not a cosmetic add-on.

### 4. Be cautious about uniform exposure assumptions in high-flow settings
In model interpretation, avoid implying that one unit increase in exposure has the same collision meaning everywhere across the network.

Where possible:
- inspect calibration across AADT bands,
- inspect top-risk bands separately for high-flow roads,
- and consider whether the model needs a flexible exposure effect or interaction structure.

### 5. Use this paper in the literature review as “methodologically adjacent”, not “foundationally validating”
Best use in your literature record:
- relevant to **exposure shape**,
- relevant to **Poisson vs NB handling**,
- relevant to **temporal exposure detail**,
- but **not** direct validation of the ORR main unit of analysis.

That is the honest positioning.

## Suggested wording for your project notes

You could fairly say something like:

> Retallack and Ostendorf (2020) show that, in an intersection-based hourly traffic dataset, collision frequency is approximately linear at lower traffic volumes but rises faster at the highest congestion levels, with Poisson adequate in some strata and negative binomial preferred where overdispersion is present. For Open Road Risk, this supports testing non-linear and context-specific exposure effects and retaining explicit dispersion diagnostics, while not directly validating the project’s annual link-level exposure model.

## Final judgement

This paper is **useful but narrow** for ORR.

Its best value is not that it tells you the final model to use. It does not. Its value is that it gives a concrete empirical example showing:
- exposure–collision relationships can bend in the upper range,
- high-temporal-resolution exposure can reveal that,
- and Poisson-vs-NB choice should be evidence-led.

So the right reaction is not “this validates ORR”.
The right reaction is:

**use it to justify sharper tests inside ORR, especially around exposure shape, dispersion, road-family heterogeneity, and temporal exposure structure.**
