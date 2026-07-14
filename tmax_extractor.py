#!/usr/bin/env python3
"""
tmax_extractor.py

Builds the SALTShaker `tmaxlist` starter file (e.g. SN_peak_MJD.list) from
one or more SNANA FITRES files (e.g. FIT_LSST.FITRES, FIT_Roman.FITRES),
combining every survey into a single file with unique SNIDs, as required by
the `tmaxlist` key in SALTShaker_main_file.config.

Output format (matches SN_peak_MJD.list):

    #SNID PKMJD
    200003 55564.3594
    200005 55176.3359
    ...

Usage
-----
    python tmax_extractor.py \\
        --fitres FIT_LSST.FITRES FIT_Roman.FITRES \\
        --outfile SN_peak_MJD.list

Quality cuts (converged fit, FITPROB, |x1|, |c|, x1ERR, PKMJDERR) are applied
before a SN's PKMJD is trusted as an initial peak-MJD guess; all thresholds
are tunable from the command line -- run with --help to see them, and adjust
to match whatever cuts your analysis actually uses.
"""

import argparse
import sys
from pathlib import Path

from fitres_utils import QualityCuts, cid_sort_key, collect_rows

REQUIRED_COLUMNS = ["CID", "PKMJD"]


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Extract a combined SN_peak_MJD.list (tmaxlist) "
                     "from one or more SNANA FITRES files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--fitres", nargs="+", required=True, metavar="FILE",
        help="One or more FITRES files to combine, "
             "e.g. FIT_LSST.FITRES FIT_Roman.FITRES "
             "(.gz is also accepted).",
    )
    parser.add_argument(
        "--outfile", default="SN_peak_MJD.list", metavar="FILE",
        help="Output tmaxlist path.",
    )

    QualityCuts().add_cli_args(parser)

    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    cuts = QualityCuts.from_args(args)

    for path in args.fitres:
        if not Path(path).exists():
            print(f"ERROR: FITRES file not found: {path}", file=sys.stderr)
            return 1

    rows = collect_rows(args.fitres, cuts, REQUIRED_COLUMNS)
    rows.sort(key=cid_sort_key)

    with open(args.outfile, "w") as f:
        f.write("#SNID PKMJD\n")
        for row in rows:
            f.write(f"{row['CID']} {row['PKMJD']}\n")

    print(
        f"Wrote {len(rows)} SNe (from {len(args.fitres)} FITRES file(s)) "
        f"to {args.outfile}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
