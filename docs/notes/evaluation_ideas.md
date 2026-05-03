# Open Road Risk: Evaluation Strategy & Competitive Landscape

While traditional road safety analysis relies on expensive manual surveys (e.g., EuroRAP) or highly localized historical crash mapping, **Open Road Risk** provides a programmatic, network-wide predictive model. 

To successfully position this open-source pipeline to transport authorities or academic peers, it is essential to establish robust internal evaluation metrics, source independent validation data, and understand how this tool compares to the wider commercial ecosystem.

---

## 1. Internal Evaluation & Validation Strategies

Because proprietary datasets like EuroRAP are locked behind commercial paywalls or NDAs, Open Road Risk utilizes internal mathematical validation to prove the efficacy of both its traffic interpolation (Stage 1a) and crash prediction (Stage 2) models.

### A. The Time-Series Holdout Validation (Predicting the Future)
The ultimate test of a predictive safety model is whether it accurately flags roads *before* crashes happen. This is the mathematically rigorous alternative to buying proprietary road-rating data.
* **Methodology:** Constrain the pipeline's training window to **2015–2021**. Generate XGBoost risk scores for the entire network based solely on this restricted timeline.
* **The Test:** Overlay the actual STATS19 collision points from the "future" years (**2022–2024**) onto the network. 
* **Success Metric:** Calculate the percentage of 2022-2024 crashes that occurred on road links residing in the top 10% (90th percentile) of the model's 2021 risk scores. A disproportionate concentration of future crashes on flagged roads proves high predictive validity.

### B. The "Naive" Baseline Test
To prove that the Stage 2 XGBoost model (current honest post-fix pseudo-R²
about 0.32, not the older leaky `~0.86` figure) is capturing complex
infrastructural signals rather than just acting as a routing algorithm, it
must beat a basic mathematical assumption.
* **The Baseline:** Calculate a naive risk score assuming crashes are strictly proportional to `AADT * link_length`. 
* **The Test:** Compare the out-of-sample predictive accuracy of the XGBoost model (which includes OSM features, network centrality, and curvature) against this naive baseline to isolate the exact value the machine learning adds.

### C. The "Battle of Interpolations" (Evaluating Stage 1a)
The pipeline intentionally drops DfT-interpolated traffic counts to train only on physically counted data. You can use this to prove your model is better at guessing traffic than the government.
* **The Setup:** Find a minor road point that was physically counted in 2019, flagged as an "Estimated" guess by the DfT in 2021/2022, and physically counted again in 2023.
* **The Test:** Pit the DfT's 2021 estimate against your Stage 1a model's 2021 prediction. 
* **The Verdict:** Use the 2023 physical ground-truth as the referee. If your model's curve (using OSM and network centrality) provides a smoother, more accurate bridge between the known count years than the DfT's baseline math, you have mathematically proven your traffic fill-in is superior.

---

## 2. Independent Ground-Truth Data Sources for AADT

Beyond comparing against the DfT, you can evaluate the Stage 1a traffic model against truly independent "new data"—data that exists entirely outside the national system.

### A. Local Authority Permanent Counters (Open Data)
Because local authorities manage the minor road network, they often place inductive loops on roads that the national DfT network ignores.
* **Data Mill North (Yorkshire Focus):** The primary open data portal for Leeds and the wider Yorkshire region. Contains historic and continuous local traffic counts.
  * [Data Mill North - Traffic & Transport](https://datamillnorth.org/dataset/?theme=Transport)
* **Transport for West Midlands (TfWM):** A highly active open data hub with local sensor data, useful for the Midlands portion of the study area.
  * [TfWM Open Data](https://www.tfwm.org.uk/who-we-are/data-and-insight/open-data/)

### B. Planning Application ATCs
When developers submit a Transport Assessment for a new development, they must commission private Automatic Traffic Counters (ATCs) using pneumatic tubes on surrounding minor roads. This provides hyper-local, physical count data.
* **Example - Leeds City Council Planning Portal:** [Leeds PublicAccess](https://publicaccess.leeds.gov.uk/online-applications/)
* **Example - Sheffield City Council Planning Portal:** [Sheffield Planning Applications](https://planningapps.sheffield.gov.uk/online-applications/)

> **FOI Pro-Tip:** Instead of manually scraping PDFs from planning portals, submit a Freedom of Information (FOI) request to a specific council's Highways department requesting: *"All raw ATC tube count data commissioned by the council or submitted via planning applications for minor roads between 2021–2023."*

### C. Telematics & Floating Car Data (Commercial)
Commercial GPS and mobile network providers track actual vehicle and device movements, offering network-wide ground truth without relying on physical roadside sensors.
* **O2 Motion:** Aggregated, anonymised mobility data based on billions of daily network events from Virgin Media O2 mobile users.
* **INRIX Volume Profiles:** Directional, time‑of‑day vehicle volumes in 15‑minute increments, specifically designed to replace manual counts.
* **TomTom O/D Traffic:** Granular traffic volume data based on their massive network of sat-navs and mobile apps.

---

## 3. The Commercial Ecosystem & Competitors

The predictive road safety market is highly active, primarily driven by the push for Autonomous Vehicles (AVs) and Smart Cities. Open Road Risk achieves similar network-wide screening using open data, offering a highly disruptive, free alternative to these capitalized startups.

### The Edge-Case & Graph AI Innovators
* **dRISK (dRisk.ai):** Founded by Chess Stetson (Caltech, Computational and Neural Systems), dRISK eschews traditional civil engineering models for **patented knowledge graphs**. They map massive arrays of physical hazards, traffic flows, and historical crashes to find edge-cases—focusing heavily on training driverless cars and assisting civil transit authorities.
* **Waycare (now Rekor Systems):** Famous for partnering with state DOTs. They ingest live connected-vehicle data, Waze reports, and weather APIs to predict crash hotspots up to two hours *before* they occur.

### The Connected Vehicle (Telematics) Giants
These companies monetize the raw data streaming off modern car computers (hard braking, steering jerks, wiper activation) and convert it into proxy safety data.
* **StreetLight Data & INRIX:** Both companies purchase massive amounts of mobile and sat-nav ping data to generate their own "Volume Profiles," selling AADT equivalents and risk metrics directly to transport planners.

### The Edge Vision Startups
* **Nexar & Derq:** Instead of relying purely on historical STATS19 data, these companies use AI computer vision—running either on consumer dashcams or edge-computers mounted in street cabinets—to actively map infrastructure degradation and near-misses in real-time.

---

## 4. Strategic Positioning vs. Industry Incumbents

When presenting Open Road Risk to GIS professionals and civil engineers, it is crucial to position the pipeline correctly against the tools they already use.

### Open Road Risk vs. ESRI (ArcGIS)
* **The Misconception:** ESRI is a direct competitor.
* **The Reality:** ESRI is a map canvas; Open Road Risk is the data factory. ESRI does not natively possess exposure-adjusted UK risk scores or machine-learning imputed traffic counts for minor roads out-of-the-box.
* **The "Bake-Off" Advantage:** While a GIS analyst *could* attempt to rebuild a Poisson GLM or Random Forest inside ArcGIS Pro using proprietary toolboxes, doing so is slow, requires £3,000+ commercial licenses, and produces binary project files that are notoriously difficult to version-control via Git. 
* **The Pitch:** Open Road Risk runs natively in Python (`scikit-learn`, `xgboost`), scales instantly, allows total control over hyperparameters, and outputs a standard **GeoPackage** that local councils can immediately drag-and-drop into their existing ESRI workflows.

### Open Road Risk vs. The Road Safety Foundation (EuroRAP)
* **The Incumbent:** The RSF is the UK franchise holder for EuroRAP. They utilize highly accurate but expensive camera-cars to manually log 50+ infrastructure hazards to generate 1-to-5 Star road ratings.
* **The Constraint:** Due to sheer cost, the RSF primarily surveys the Strategic Road Network and major 'A' roads, leaving the vast majority of local minor roads (roughly 85% of the physical network) completely unassessed.
* **The Pitch ("Complementary, not Competitive"):** Open Road Risk is not a replacement for an iRAP physical survey; it is an **algorithmic triage tool**. It uses free, open data to flag high-risk historical hotspots across the *entire* network—including those unclassified minor roads—allowing councils to strategically target exactly where they should commission their next physical RSF survey.
