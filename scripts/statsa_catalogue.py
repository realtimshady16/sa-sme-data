#!/usr/bin/env python3
"""Catalogue Stats SA's iSiBaloweb unit-record archive.

    python3 scripts/statsa_catalogue.py > ../statsa-units/CATALOGUE.tsv

Walks the site's own navigation: hub pages -> surveys -> years -> resources.
Every dataset offered is a plain file under /data/PSS/... with no login, so this
produces the complete list of unit-record files with size and last-modified.

Polite by construction: one request at a time, 2 s apart, a research user agent,
one retry. Sizes come from a HEAD on each file, not a download.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urljoin

BASE = "https://isibaloweb.statssa.gov.za"
HUBS = ["/pages/labour.php", "/pages/social.php", "/pages/povertyinquality.php",
        "/pages/vital.php", "/pages/dataapps.php"]
UA = "Mozilla/5.0 (research; SME data inventory)"
DELAY = 2.0
_cache = {}


def get(url, head=False):
    if url in _cache:
        return _cache[url]
    req = urllib.request.Request(url, method="HEAD" if head else "GET",
                                 headers={"User-Agent": UA})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = b"" if head else r.read().decode("utf-8", "replace")
                out = (r.status, dict(r.headers), body)
                _cache[url] = out
                time.sleep(DELAY)
                return out
        except urllib.error.HTTPError as e:
            if attempt == 2:
                _cache[url] = (e.code, {}, "")
                time.sleep(DELAY)
                return _cache[url]
            time.sleep(DELAY * 2)
        except Exception:
            if attempt == 2:
                _cache[url] = (0, {}, "")
                time.sleep(DELAY)
                return _cache[url]
            time.sleep(DELAY * 2)
    return (0, {}, "")


def links(html, pattern=None):
    """URLs from href attributes and from <option value="..."> — the site's
    navigation is a <select>, so most of the tree is in option values."""
    out = set(re.findall(r'href=["\']([^"\']+)["\']', html))
    out |= set(re.findall(r'<option[^>]+value=["\']([^"\']+)["\']', html))
    return sorted(out)


def main():
    # 1. hub pages -> survey landing pages
    surveys = set()
    for hub in HUBS:
        status, _, body = get(BASE + hub)
        print(f"# hub {hub} -> {status}", file=sys.stderr)
        for h in links(body, None):
            if re.search(r"/pages/surveys/[a-z]+/[a-z]+/[a-z]+p\.php$", h):
                surveys.add(h)
    print(f"# {len(surveys)} survey landing pages", file=sys.stderr)

    rows = []
    # 2. survey page -> year pages
    for sp in sorted(surveys):
        status, _, body = get(BASE + sp)
        years = [h for h in links(body, None)
                 if re.search(r"/pages/surveys/[a-z]+/[a-z]+/\d{4}/", h)]
        slug = sp.rsplit("/", 1)[-1].replace("p.php", "")
        if not years:
            rows.append(dict(survey=slug, page=sp, year="", kind="landing",
                             url="", size="", modified="", status=status))
            continue
        for yp in sorted(set(years)):
            ystatus, _, ybody = get(BASE + yp)
            year = re.search(r"/(\d{4})/", yp)
            year = year.group(1) if year else ""
            files = [h for h in links(ybody, None) if h.startswith("/data/")
                     or "/metadata/" in h or "/data/" in h]
            if not files:
                rows.append(dict(survey=slug, page=yp, year=year, kind="yearpage",
                                 url="", size="", modified="", status=ystatus))
            for f in files:
                full = urljoin(BASE, f)
                hstatus, headers, _ = get(full, head=True)
                rows.append(dict(
                    survey=slug, page=yp, year=year,
                    kind="metadata" if "/metadata/" in f else "data",
                    url=full,
                    size=headers.get("Content-Length", ""),
                    modified=headers.get("Last-Modified", ""),
                    status=hstatus))
            print(f"# {slug} {year}: {len(files)} files (status {ystatus})", file=sys.stderr)

    cols = ["survey", "year", "kind", "url", "size", "modified", "status", "page"]
    print("\t".join(cols))
    for r in rows:
        print("\t".join(str(r.get(c, "")) for c in cols))


if __name__ == "__main__":
    main()
