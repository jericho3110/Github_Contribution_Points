#!/usr/bin/env python3
import argparse
import datetime
import json
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta, timezone

DATA_PATH = "data.json"


def parse_date(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Date must be ISO format like 2025-05-17 or 2025-05-17T14:42:34+00:00"
        ) from exc


def build_random_date() -> datetime:
    now = datetime.now(timezone.utc)
    base = now - timedelta(days=1461) + timedelta(days=1)
    weeks = random.randint(0, 208)
    days = random.randint(0, 6)
    return base + timedelta(weeks=weeks, days=days)


def write_data(path: str, date_string: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"date": date_string}, handle, indent=2)
        handle.write("\n")


def git_commit(path: str, date_string: str, message: str) -> None:
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_string
    env["GIT_COMMITTER_DATE"] = date_string
    subprocess.run(["git", "add", path], check=True, env=env)
    subprocess.run(["git", "commit", "-m", message], check=True, env=env)


def git_push() -> None:
    subprocess.run(["git", "push"], check=True)


def commit_date(date_value: datetime, path: str, dry_run: bool) -> str:
    date_string = date_value.astimezone(timezone.utc).isoformat()
    write_data(path, date_string)
    if dry_run:
        return date_string
    git_commit(path, date_string, message=date_string)
    return date_string


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create backdated Git commits so GitHub contribution dates are in the past."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1000,
        help="Number of random backdated commits to create across the past year.",
    )
    parser.add_argument(
        "--date",
        type=parse_date,
        help="Create a single commit for this ISO date, e.g. 2025-05-17 or 2025-05-17T14:42:34+00:00.",
    )
    parser.add_argument(
        "--path",
        default=DATA_PATH,
        help="Path to the JSON file that will be updated before each commit.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the dates that would be used without making commits.",
    )
    args = parser.parse_args()

    if args.date and args.count != 100:
        parser.error("Use either --date for a single commit or --count for random commits, not both with a changed count.")

    if args.date:
        date_string = commit_date(args.date, args.path, args.dry_run)
        print(f"Prepared commit for {date_string}")
        return 0

    if args.count < 0:
        parser.error("--count must be zero or positive")

    if args.count == 0:
        if args.dry_run:
            print("No commits created because --count is 0.")
            return 0
        print("No commits to create; pushing current branch instead.")
        git_push()
        return 0

    for index in range(1, args.count + 1):
        commit_date(build_random_date(), args.path, args.dry_run)
        print(f"Created {index}/{args.count} backdated commit")

    if not args.dry_run:
        print("Pushing commits to remote...")
        git_push()

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"Git command failed: {exc}", file=sys.stderr)
        raise
