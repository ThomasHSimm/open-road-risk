"""PROJ/pyproj environment diagnostic for the Stage 1a EPSG:27700 issue.

Run inside the affected environment:  python scripts/diag_proj.py
Paste the full output back. Every section is wrapped so one failure
doesn't stop the rest.
"""

import glob
import os
import sqlite3
import sys
import traceback


def section(title):
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


def safe(fn):
    try:
        fn()
    except Exception:
        traceback.print_exc()


def s1_python():
    print("Python     :", sys.version)
    print("Executable :", sys.executable)
    print("Prefix     :", sys.prefix)


def s2_env_vars():
    for var in [
        "PROJ_LIB",
        "PROJ_DATA",
        "PROJ_NETWORK",
        "GDAL_DATA",
        "GDAL_DRIVER_PATH",
        "CONDA_PREFIX",
        "CONDA_DEFAULT_ENV",
    ]:
        print(f"{var:18s} = {os.environ.get(var, '<unset>')}")


def s3_pyproj():
    import pyproj

    print("pyproj version :", pyproj.__version__)
    print("pyproj file    :", pyproj.__file__)
    print("PROJ version   :", pyproj.proj_version_str)
    print("data dir       :", pyproj.datadir.get_data_dir())
    try:
        print("user data dir  :", pyproj.datadir.get_user_data_dir())
    except Exception as e:
        print("user data dir  : <error>", e)


def s4_proj_dbs():
    # Find every proj.db visible from this environment and report its
    # schema version. A runtime/database layout mismatch is the prime suspect.
    roots = set()
    for v in ["PROJ_LIB", "PROJ_DATA", "CONDA_PREFIX"]:
        if os.environ.get(v):
            roots.add(os.environ[v])
    roots.add(sys.prefix)
    try:
        import pyproj

        roots.add(pyproj.datadir.get_data_dir())
    except Exception:
        pass

    seen = set()
    for root in roots:
        for db in glob.glob(os.path.join(root, "**", "proj.db"), recursive=True):
            real = os.path.realpath(db)
            if real in seen:
                continue
            seen.add(real)
            try:
                conn = sqlite3.connect(f"file:{real}?mode=ro", uri=True)
                rows = dict(
                    conn.execute(
                        "SELECT key, value FROM metadata WHERE key IN "
                        "('DATABASE.LAYOUT.VERSION.MAJOR','DATABASE.LAYOUT.VERSION.MINOR',"
                        "'PROJ.VERSION','EPSG.VERSION')"
                    ).fetchall()
                )
                conn.close()
                print(f"{real}\n    {rows}")
            except Exception as e:
                print(f"{real}\n    <unreadable: {e}>")
    if not seen:
        print("No proj.db found under any candidate root.")


def s5_transform():
    import numpy as np
    import pyproj

    print("CRS EPSG:27700 resolves:", pyproj.CRS("EPSG:27700").name)
    t = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
    x, y = t.transform(-2.1, 51.8)
    print(f"transform(-2.1, 51.8) -> ({x}, {y})")
    print("Expected (Helmert/no grid): (~393201, ~211266)")
    finite = np.isfinite(x) and np.isfinite(y)
    print("FINITE:", finite)
    if finite:
        err = ((x - 393200.94) ** 2 + (y - 211266.38) ** 2) ** 0.5
        print(f"Offset from control value: {err:.1f} m")


def s6_operations():
    from pyproj.transformer import TransformerGroup

    tg = TransformerGroup("EPSG:4326", "EPSG:27700", always_xy=True)
    print(f"Available operations  : {len(tg.transformers)}")
    for tr in tg.transformers[:5]:
        print(f"    accuracy={tr.accuracy}m  {tr.description[:80]}")
    print(f"Unavailable operations: {len(tg.unavailable_operations)}")
    for op in tg.unavailable_operations[:5]:
        print(f"    {op.name[:80]}")


def s7_packages():
    try:
        from importlib import metadata
    except ImportError:
        import importlib_metadata as metadata
    names = [
        "pyproj",
        "geopandas",
        "shapely",
        "fiona",
        "rasterio",
        "gdal",
        "pandas",
        "numpy",
        "scipy",
    ]
    for dist in metadata.distributions():
        n = (dist.metadata["Name"] or "").lower()
        if n in names:
            print(f"{n:12s} {dist.version:12s} {dist.locate_file('')}")


if __name__ == "__main__":
    section("1. Python")
    safe(s1_python)
    section("2. Environment variables")
    safe(s2_env_vars)
    section("3. pyproj / PROJ")
    safe(s3_pyproj)
    section("4. All proj.db files visible (schema versions)")
    safe(s4_proj_dbs)
    section("5. The failing transform")
    safe(s5_transform)
    section("6. Coordinate operations PROJ can see")
    safe(s6_operations)
    section("7. Geospatial package inventory (pip/conda mix check)")
    safe(s7_packages)
