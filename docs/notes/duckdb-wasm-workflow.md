# Suggested Workflow: Open Road Risk Deployment (DuckDB-WASM Route)

This workflow outlines the exact steps and prompts needed to pivot your current React prototype and Python pipeline into a zero-cost, high-performance web app capable of rendering your 2.1-million-link dataset.

---

## Phase 1: Prepare the Data (Python Backend)
Before building the web app, your Python pipeline must output a web-optimized, spatially sorted Parquet file.

**Prompt to give to your AI Coding Assistant (Gemini/Claude/ChatGPT):**
> "I have a Python data science pipeline using GeoPandas that outputs a 2.1-million-row scored road network. I need to prepare the final output `risk_scores.parquet` so it can be queried efficiently over the web using DuckDB-WASM and HTTP Range Requests. 
> 
> Please write a Python snippet I can append to my pipeline that does the following to my final GeoDataFrame:
> 1. Simplifies the LineString geometry (e.g., Douglas-Peucker tolerance 0.0005) to reduce file size.
> 2. Extracts centroid X and Y coordinates.
> 3. Sorts the DataFrame spatially using the centroids (so nearby roads are grouped together in the file).
> 4. Converts the geometry column to Well-Known Text (WKT).
> 5. Drops the heavy shapely geometry and centroid columns.
> 6. Exports to a Parquet file named `open_road_risk_final.parquet` using `pyarrow`, Snappy compression, and a `row_group_size` of 100,000."

---

## Phase 2: Finalize the Visual Design (Claude Design)
Since Claude Design excels at frontend aesthetics but cannot build WASM data pipelines, use it to finalize your UI elements *before* we wire up the real data.

**Prompt to give to Claude Design:**
> "Attached is my React prototype for 'Open Road Risk' (`app.jsx`, `panels.jsx`, `map.jsx`, `styles.css`). It currently uses synthetic data generated in `data.js`. 
> 
> I am going to wire this up to a real database later, but first, I need you to finalize the UI. Please add the following UI elements to the left panel in `panels.jsx` and update `styles.css` accordingly:
> 1. A 'Risk Tolerance' slider (0 to 100) that looks clean and matches the dark analyst theme.
> 2. A toggle switch for 'Show Time-of-Day Profile'.
> 3. Ensure these new controls update the React state in `app.jsx`.
> Do not change any map logic or data structures. Just give me the updated frontend code."

---

## Phase 3: Human Setup (Hosting the Data & App)
Now that you have the optimized Parquet file and the finalized UI, you as the human need to set up the free infrastructure.

1. **Host the Parquet File:**
   * *Option A (Easiest):* Create a GitHub repository for your project. Go to "Releases" -> "Draft a new release". Upload `open_road_risk_final.parquet` as an asset. Once published, right-click the asset download button and copy the raw download URL.
   * *Option B (More robust):* Create an AWS account. Go to S3, create a public bucket, and upload the file. Note the object URL.
2. **Host the React App:**
   * Create an account at [Netlify](https://www.netlify.com/).
   * Once your code is wired up (Phase 4), you will just drag and drop your project folder here for an instant live URL.

---

## Phase 4: Wire the Engine (AI Coding Assistant)
This is the final step where you connect your React UI to the remote Parquet file using DuckDB-WASM. 

**Prompt to give to your AI Coding Assistant (Gemini/ChatGPT):**
> "I am ready to convert my static React map prototype into a live app using DuckDB-WASM. 
> 
> My React app currently maps over an array of mocked links. I have hosted my spatially-sorted, web-optimized Parquet file at `[INSERT YOUR GITHUB/S3 URL HERE]`. 
> 
> Please provide the JavaScript/React code to:
> 1. Initialize `duckdb-wasm` when the app loads.
> 2. Create a function that takes the current map bounding box (North, South, East, West coordinates) from my Leaflet map (`map.jsx`).
> 3. Write a SQL query using DuckDB that queries the remote Parquet file via HTTP range requests to return ONLY the road geometries (from the WKT column) and risk scores that fall within that bounding box.
> 4. Parse the WKT back into Leaflet polylines.
> 
> Tell me exactly how to modify my `app.jsx` and `map.jsx` to achieve this."
