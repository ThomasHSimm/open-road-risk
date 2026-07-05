# GB Reporting-Area Display Policy

The named reporting-area layer is a simplified display geography for the
Quarto key-figure maps. It is not a modelling unit, validation fold, formal
statistical geography, or administrative reporting boundary.

Primary public geography:

- 10 km grid cells generated from scored road-link representative points.
- Grid cells with fewer than 20 scored links are omitted from the key-figure
  map to avoid sparse-cell overinterpretation.

Named display geography:

- Built by `scripts/build_reporting_areas_gb.py`.
- Output GeoJSON: `quarto/outputs/reporting_areas_gb.geojson`.
- Output manifest: `quarto/outputs/reporting_areas_gb_manifest.json`.
- The policy dissolves compact urban and county-style local authorities where
  separate polygons would be hard to read at GB map scale.
- Areas not listed in the dissolve map remain as their source authority names.

Current dissolve intent:

- Metropolitan county-style groups: Greater London, Greater Manchester,
  Merseyside, West Midlands, West Yorkshire, South Yorkshire, Tyne and Wear.
- Compact combined-authority or travel-to-work style groups: Tees Valley,
  Bristol and West of England, Cambridgeshire and Peterborough, Cheshire and
  Warrington.
- County plus unitary-style groups: Bedfordshire, Lancashire and Blackpool,
  Derby and Derbyshire, Kent and Medway, Essex/Southend/Thurrock, Hampshire/
  Portsmouth/Southampton, Staffordshire/Stoke-on-Trent.
- Scottish city-region and council-cluster groups where individual councils
  are too compact at national scale: Glasgow City Region, Edinburgh and
  Lothians, Tayside, Forth Valley, Ayrshire, Aberdeen and Aberdeenshire.

Presentation rule:

- Public-facing maps and tables should prefer `risk_percentile`, deciles, or
  rank bands.
- Do not present raw `predicted_xgb` values as expected collision counts until
  a calibration diagnostic supports that interpretation for the current run.
