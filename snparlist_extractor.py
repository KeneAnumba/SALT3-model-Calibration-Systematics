#!/usr/bin/env python3
"""
snparlist_extractor.py

Builds the SALTShaker `snparlist` starter file (e.g. SN_params.list) from
one or more SNANA FITRES files (e.g. FIT_LSST.FITRES, FIT_Roman.FITRES),
combining every survey into a single file with unique SNIDs, as required by
the `snparlist` key in SALTShaker_main_file.config.

Output format (matches SN_params.list):

    #SNID zHEL x0 x1 x1ERR c cERR PKMJD PKMJDERR MWEBV FITPROB
    200003 1.27425 1.07201e-06 0.46904 0.42636 0.16790 0.10024 55564.3594 0.8730 6.36365e-03 0.89678
    ...

Usage
-----
    python snparlist_extractor.py \\
        --fitres FIT_LSST.FITRES FIT_Roman.FITRES \\
        --outfile SN_params.list

Quality cuts (converged fit, FITPROB, |x1|, |c|, x1ERR, PKMJDERR) are applied
before a SN's parameters are trusted as an initial guess; all thresholds are
tunable from the command line -- run with --help to see them, and adjust to
match whatever cuts your analysis actually uses.
"""

import argparse
import sys
from pathlib import Path

from fitres_utils import QualityCuts, cid_sort_key, collect_rows

# Order here fixes both the required FITRES columns and the output column order.
OUTPUT_COLUMNS = [
    "zHEL", "x0", "x1", "x1ERR", "c", "cERR",
    "PKMJD", "PKMJDERR", "MWEBV", "FITPROB",
]
REQUIRED_COLUMNS = ["CID"] + OUTPUT_COLUMNS


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Extract a combined SN_params.list (snparlist) "
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
        "--outfile", default="SN_params.list", metavar="FILE",
        help="Output snparlist path.",
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

    header = "#SNID " + " ".join(OUTPUT_COLUMNS)
    with open(args.outfile, "w") as f:
        f.write(header + "\n")
        for row in rows:
            values = " ".join(row[col] for col in OUTPUT_COLUMNS)
            f.write(f"{row['CID']} {values}\n")

    print(
        f"Wrote {len(rows)} SNe (from {len(args.fitres)} FITRES file(s)) "
        f"to {args.outfile}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
