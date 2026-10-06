"""CLI entry point.

Deliberately thin: parse arguments, load inputs, invoke the pipeline, write
output. Any logic worth testing belongs in a module, not here, because this
file is the part that cannot be exercised without spawning a process.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from infravce import __version__
from infravce.normalise.versions import detect_ecosystem, normalise_many


def _cmd_version(_: argparse.Namespace) -> int:
    print(f"infravce {__version__}")
    return 0


def _cmd_normalise(args: argparse.Namespace) -> int:
    versions: list[str] = list(args.version)
    if args.file:
        versions.extend(
            line.strip() for line in Path(args.file).read_text().splitlines() if line.strip()
        )

    pairs = [(args.product, v) for v in versions]
    records = [v.model_dump(mode="json") for v in normalise_many(pairs)]

    payload = json.dumps(records, indent=2)
    if args.out:
        Path(args.out).write_text(payload + "\n")
        print(f"wrote {len(records)} record(s) to {args.out}", file=sys.stderr)
    else:
        print(payload)
    return 0


def _cmd_detect(args: argparse.Namespace) -> int:
    print(detect_ecosystem(args.product, args.version).value)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="infravce", description="Infrastructure CVE checker.")
    p.add_argument("--version", action="version", version=f"infravce {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="print version").set_defaults(func=_cmd_version)

    n = sub.add_parser("normalise", help="decompose version strings")
    n.add_argument("version", nargs="*", help="version strings to normalise")
    n.add_argument("--file", help="read version strings from a file, one per line")
    n.add_argument("--product", default="", help="product name, used for ecosystem detection")
    n.add_argument("--out", help="write JSON here instead of stdout")
    n.set_defaults(func=_cmd_normalise)

    d = sub.add_parser("detect", help="detect the ecosystem of a product/version pair")
    d.add_argument("product")
    d.add_argument("version")
    d.set_defaults(func=_cmd_detect)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
