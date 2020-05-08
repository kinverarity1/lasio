import argparse
import os
import sys

import lasio


def convert_version():
    args = get_convert_version_parser().parse_args(sys.argv[1:])

    assert os.path.isfile(args.input)

    las = lasio.read(args.input, ignore_header_errors=args.ignore_header_errors)

    if os.path.isfile(args.output) and not args.overwrite:
        raise OSError("Output file already exists")

    with open(args.output, "w") as f:
        las.write(f, version=float(args.to))


def get_convert_version_parser():
    parser = argparse.ArgumentParser(
        "Convert LAS file version",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-t", "--to", default=2, help="Version to convert to")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite output file if it already exists",
    )
    parser.add_argument(
        "-i",
        "--ignore-header-errors",
        action="store_true",
        help="Ignore header section errors.",
        default=False,
    )
    parser.add_argument("input")
    parser.add_argument("output")
    return parser
