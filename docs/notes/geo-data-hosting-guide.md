# Practically Displaying Geospatial Data Online (Zero to Low Cost)

This guide breaks down the complete spectrum of options for hosting large-scale geospatial data (like your 2.1-million-link Open Road Risk dataset) online, ranging from static prototypes to full-scale production web apps. 

## 1. The Static Prototype (Netlify / Vercel / GitHub Pages)
Best for: Sharing UI mockups, small filtered datasets, portfolio pieces.
* **How it works:** You host plain HTML, CSS, and JavaScript (or a compiled React app). All logic happens in the user's browser.
* **Pros:** 100% free forever, lightning-fast global CDN, deploys in seconds via drag-and-drop or GitHub integration.
* **Cons:** Cannot handle massive files. Browsers will crash if you try to load 2.1 million vector lines at once into memory via standard JSON/JS files.
* **Cost:** $0

## 2. The Traditional Full-Stack (Render / Railway)
Best for: Applications requiring live machine learning inference, real-time writes, or complex spatial joins on the fly.
* **How it works:** You rent a permanent server running a Python API (e.g., FastAPI) connected to a persistent spatial database (PostgreSQL + PostGIS). The frontend queries the backend via REST/WebSockets.
* **Pros:** Infinite flexibility. Can handle the full 2.1 million links using PostGIS spatial indexing (`GIST`) and dynamic vector tile generation (`ST_AsMVT`).
* **Cons:** Requires DevOps setup. Flat monthly fees on Render, or usage-based billing on Railway. Cold starts on free tiers.
* **Cost:** ~$5 to $15+ per month for a 24/7 web service and managed database.

## 3. The Pure Python Free-Tier (Streamlit Community Cloud + DuckDB)
Best for: Data scientists who want to build a dashboard entirely in Python without writing frontend code.
* **How it works:** You compress your data into a `.parquet` file. Your Python Streamlit app uses `duckdb` to query the Parquet file locally. Streamlit renders the UI automatically.
* **Pros:** 100% free hosting via Streamlit Community Cloud or Hugging Face Spaces. No database server required.
* **Cons:** You lose total control over the UI (cannot use your custom Carto dark-theme React app). The app goes to sleep after 12-48 hours of inactivity, causing a 20-second "waking up" screen for the next visitor.
* **Cost:** $0

## 4. The "Holy Grail" Serverless Browser DB (DuckDB-WASM + React)
Best for: High-performance, zero-cost production apps with custom UIs and massive read-only datasets.
* **How it works:** You export your data as a spatially-sorted `.parquet` file and host it on a free static bucket (AWS S3 Free Tier or GitHub Releases). You embed `duckdb-wasm` directly into your React app hosted on Netlify. 
* **The Magic:** As the user pans the map, DuckDB-WASM uses **HTTP Range Requests** to fetch *only the bytes* from the remote Parquet file corresponding to the visible bounding box. 
* **Pros:** 100% free, handles millions of rows effortlessly, keeps your custom React UI pixel-perfect, zero cold-start wake-up times.
* **Cons:** Requires prepping your Parquet file carefully (spatial sorting, chunking, geometry simplification) and writing some complex WebAssembly integration code.
* **Cost:** $0
