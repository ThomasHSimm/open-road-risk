### ONS Rural-Urban LSOA classification

- [x] ONS Rural-Urban Classification (2021) added to `network_features.parquet`
  (23 April 2026) — 84.51% link coverage, 6-class 2021 scheme (`UN1`, `UF1`,
  `RSN1`, `RSF1`, `RLN1`, `RLF1`) preserved from source; derived binary
  `ruc_urban_rural` shows 74% urban / 26% rural across non-null links,
  consistent with the study area. `pop_density_per_km2` unchanged.
  Nearest-centroid limitation documented in methodology page. See
  `data/features/ruc_provenance.json`.

---
