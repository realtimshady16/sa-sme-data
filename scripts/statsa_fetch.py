#!/usr/bin/env python3
"""Fetch Stats SA unit-record and time-series files, with a manifest.

    python3 scripts/statsa_fetch.py FILE_WITH_URLS [--out DIR]

One request at a time, 2 s apart, one retry, research user agent. Writes
`manifest.tsv` (url, status, bytes, sha256, path) beside the downloads, so a
re-download can be checked against what any analysis was computed from.

Note: on isibaloweb.statssa.gov.za the HTML *pages* sit behind Incapsula (a
~1.1 KB challenge shell to a plain client) but the files under /data/ and
/metadata/ download directly. Enumeration therefore happens in a browser; this
script only fetches the file list it is given.
"""
import hashlib
import os
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (research; SME data inventory)"
DELAY = 2.0


def fetch(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
                status = r.status
            with open(path, "wb") as f:
                f.write(data)
            return status, len(data), hashlib.sha256(data).hexdigest()
        except urllib.error.HTTPError as e:
            if attempt == 2:
                return e.code, 0, ""
            time.sleep(DELAY * 2)
        except Exception as e:
            if attempt == 2:
                return f"ERR {type(e).__name__}", 0, ""
            time.sleep(DELAY * 2)
    return "unreachable", 0, ""


def main():
    args = sys.argv[1:]
    out = str(DATA / "statsa" / "work")
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        del args[i:i + 2]
    urls = [l.strip() for l in open(args[0]) if l.strip() and not l.startswith("#")]
    os.makedirs(out, exist_ok=True)

    rows, seen = [], set()
    for url in urls:
        name = url.rstrip("/").rsplit("/", 1)[-1]
        sub = ""
        for part in ("/data/", "/metadata/"):
            if part in url:
                sub = "metadata" if part == "/metadata/" else "data"
        dest = os.path.join(out, sub, name) if sub else os.path.join(out, name)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if dest in seen:
            continue
        seen.add(dest)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            h = hashlib.sha256(open(dest, "rb").read()).hexdigest()
            rows.append((url, "cached", os.path.getsize(dest), h, dest))
            print(f"cached  {name}", file=sys.stderr)
            continue
        status, size, digest = fetch(url, dest)
        rows.append((url, status, size, digest, dest))
        print(f"{status}  {size:>10,}  {name}", file=sys.stderr)
        time.sleep(DELAY)

    # merge with any existing manifest: two runs writing the same path would
    # otherwise truncate each other (they did, on 2026-11-23)
    mpath = os.path.join(out, "manifest.tsv")
    merged = {}
    if os.path.exists(mpath):
        for line in open(mpath).read().splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) == 5:
                merged[parts[4]] = tuple(parts)
    for r in rows:
        merged[r[4]] = tuple(str(x) for x in r)
    with open(mpath, "w") as f:
        f.write("url\tstatus\tbytes\tsha256\tpath\n")
        for k in sorted(merged):
            f.write("\t".join(merged[k]) + "\n")
    rows = list(merged.values())
    total = sum(r[2] for r in rows if isinstance(r[2], int))
    print(f"\n{len(rows)} files, {total/1e6:,.1f} MB -> {out}/manifest.tsv", file=sys.stderr)


if __name__ == "__main__":
    main()
