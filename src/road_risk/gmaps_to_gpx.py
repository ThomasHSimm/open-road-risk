"""
gmaps_to_gpx.py
---------------
Convert Google Maps shared route URLs to GPX files.

The short goo.gl/maps URLs redirect to a full URL containing waypoints
in the path as lat,lon pairs. We extract those waypoints and write a
GPX file with a single track.

Usage
-----
    # Single URL
    python gmaps_to_gpx.py "https://maps.app.goo.gl/UfA775sNWEs6P7ZW9" doncaster_route_1.gpx

    # Batch — text file with one URL per line, optional name after tab
    python gmaps_to_gpx.py --batch urls.txt --outdir data/raw/test_routes/

urls.txt format (tab separated, name optional):
    https://maps.app.goo.gl/XXX    doncaster_route_1
    https://maps.app.goo.gl/YYY    doncaster_route_2
    https://maps.app.goo.gl/ZZZ

Notes
-----
- Waypoints are route control points, not a dense track. The snap
  pipeline in ingest_test_routes.py handles this via link densification.
- Requires internet access to resolve the short URL redirect.
"""

import argparse
import re
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError


def resolve_redirect(url: str, timeout: int = 10) -> str:
    """Follow redirects on a URL and return the final destination URL."""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.url
    except URLError as e:
        raise ValueError(f"Could not resolve URL {url}: {e}")


def extract_waypoints(resolved_url: str) -> list[tuple[float, float]]:
    """
    Extract lat/lon waypoints from a Google Maps directions URL.

    Google Maps directions URLs have the form:
      /maps/dir/lat1,lon1/lat2,lon2/.../data=...

    Returns list of (lat, lon) tuples.
    """
    # Match coordinate pairs in the URL path
    coords = re.findall(r'(-?\d+\.\d+),(-?\d+\.\d+)', resolved_url)

    if not coords:
        raise ValueError(
            f"No coordinates found in URL: {resolved_url[:200]}"
        )

    waypoints = [(float(lat), float(lon)) for lat, lon in coords]

    # Basic sanity check — GB bounding box
    gb_lat = (49.5, 61.0)
    gb_lon = (-8.5, 2.0)
    valid = [
        (lat, lon) for lat, lon in waypoints
        if gb_lat[0] <= lat <= gb_lat[1] and gb_lon[0] <= lon <= gb_lon[1]
    ]

    if not valid:
        raise ValueError(
            f"No valid GB coordinates found. Raw coords: {waypoints[:5]}"
        )

    return valid


def waypoints_to_gpx(
    waypoints: list[tuple[float, float]],
    name: str = "route",
) -> str:
    """Generate GPX XML string from a list of (lat, lon) waypoints."""
    points_xml = "\n".join(
        f'        <trkpt lat="{lat}" lon="{lon}"></trkpt>'
        for lat, lon in waypoints
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="gmaps_to_gpx"
     xmlns="http://www.topografix.com/GPX/1/1">
  <trk>
    <name>{name}</name>
    <trkseg>
{points_xml}
    </trkseg>
  </trk>
</gpx>"""


def convert_url(url: str, output_path: Path, name: str = None) -> None:
    """Resolve a Google Maps URL, extract waypoints, write GPX."""
    print(f"  Resolving: {url[:60]}...")
    resolved = resolve_redirect(url)

    waypoints = extract_waypoints(resolved)
    print(f"  Found {len(waypoints)} waypoints")

    if name is None:
        name = output_path.stem

    gpx = waypoints_to_gpx(waypoints, name=name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(gpx, encoding="utf-8")
    print(f"  Saved → {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Google Maps shared route URLs to GPX files"
    )
    parser.add_argument(
        "url_or_batch",
        help="Single Google Maps URL, or path to batch file (with --batch)"
    )
    parser.add_argument(
        "output",
        nargs="?",
        help="Output GPX path (single URL mode only)"
    )
    parser.add_argument(
        "--batch", action="store_true",
        help="Treat first argument as a text file of URLs"
    )
    parser.add_argument(
        "--outdir", default="data/raw/test_routes",
        help="Output directory for batch mode (default: data/raw/test_routes)"
    )
    parser.add_argument(
        "--delay", type=float, default=1.0,
        help="Seconds between requests in batch mode (default: 1.0)"
    )
    args = parser.parse_args()

    if args.batch:
        batch_file = Path(args.url_or_batch)
        if not batch_file.exists():
            print(f"Batch file not found: {batch_file}")
            sys.exit(1)

        outdir = Path(args.outdir)
        lines = [l.strip() for l in batch_file.read_text().splitlines()
                 if l.strip() and not l.startswith("#")]

        ok, fail = 0, 0
        for i, line in enumerate(lines, 1):
            parts = line.split("\t")
            url  = parts[0].strip()
            name = parts[1].strip() if len(parts) > 1 else f"route_{i:03d}"
            out  = outdir / f"{name}.gpx"

            print(f"\n[{i}/{len(lines)}] {name}")
            try:
                convert_url(url, out, name=name)
                ok += 1
            except Exception as e:
                print(f"  ERROR: {e}")
                fail += 1

            if i < len(lines):
                time.sleep(args.delay)

        print(f"\nDone: {ok} converted, {fail} failed")

    else:
        # Single URL mode
        url = args.url_or_batch
        if args.output:
            out = Path(args.output)
        else:
            out = Path("data/raw/test_routes/route.gpx")

        try:
            convert_url(url, out)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()