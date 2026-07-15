"""Command-line entry point for the Phase 1 pipeline.

    python -m project_pilot.cli index --artist top
    python -m project_pilot.cli generate --artist top --theme identity --mood anxious \\
        --structure verse,chorus,verse,chorus,bridge,chorus
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def cmd_index(args: argparse.Namespace) -> None:
    from .retrieval import build_index_for_artist

    try:
        index = build_index_for_artist(DATA_DIR, args.artist)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    index_dir = DATA_DIR / "artists" / args.artist / "index"
    print(f"Indexed {len(index.songs)} song(s) for '{args.artist}' -> {index_dir}")


def cmd_generate(args: argparse.Namespace) -> None:
    from .generate import GenerationParseError, generate_lyrics
    from .storage import save_generation

    structure = [s.strip() for s in args.structure.split(",") if s.strip()]
    try:
        result = generate_lyrics(
            data_dir=DATA_DIR,
            artist_slug=args.artist,
            theme=args.theme,
            mood=args.mood,
            structure=structure,
            era=args.era,
            top_k=args.top_k,
            model=args.model or "claude-sonnet-5",
        )
    except (FileNotFoundError, GenerationParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    output = json.dumps(result, indent=2)
    if args.out:
        Path(args.out).write_text(output)
        print(f"Wrote {args.out}")
    else:
        print(output)

    if not args.no_archive:
        archive_path = save_generation(DATA_DIR, args.artist, result)
        print(f"Archived -> {archive_path}", file=sys.stderr)


def main() -> None:
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(prog="project_pilot", description="Project Pilot Phase 1 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="Build/refresh the retrieval index for an artist's corpus")
    p_index.add_argument("--artist", required=True, help="Artist slug (e.g. 'top')")
    p_index.set_defaults(func=cmd_index)

    p_generate = sub.add_parser("generate", help="Generate lyrics for an artist")
    p_generate.add_argument("--artist", required=True)
    p_generate.add_argument("--theme", required=True)
    p_generate.add_argument("--mood", required=True)
    p_generate.add_argument(
        "--structure",
        default="verse,chorus,verse,chorus,bridge,chorus",
        help="Comma-separated section labels",
    )
    p_generate.add_argument("--era", default=None)
    p_generate.add_argument("--top-k", type=int, default=5)
    p_generate.add_argument("--model", default=None)
    p_generate.add_argument("--out", default=None, help="Write JSON output to this file")
    p_generate.add_argument(
        "--no-archive",
        action="store_true",
        help="Don't archive this generation under data/artists/<artist>/generations/",
    )
    p_generate.set_defaults(func=cmd_generate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
