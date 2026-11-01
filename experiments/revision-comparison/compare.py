"""Compare the actual historical v1 and v2 examples in the original Git checkout."""

from __future__ import annotations

import argparse
import subprocess

REVISIONS = {
    "v1": "a54e8d6326cd2c7c0ec3f2dd474b79e9e7da68f1",
    "v2": "f15b4847adee6c60992299e73eb8b446e7bb0587",
}
CASES = ({}, {"model": "demo"}, {"model": "demo", "version": "1"})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_repo", help="Path to a checkout of 5jyan/team-agent-knowledge")
    args = parser.parse_args()
    checkers = {}
    for label, sha in REVISIONS.items():
        source = subprocess.check_output(
            ["git", "-C", args.source_repo, "show", f"{sha}:examples/config-validation/config_checker.py"],
            text=True,
        )
        namespace = {}
        exec(compile(source, f"{label}:{sha}", "exec"), namespace)
        checkers[label] = namespace["validate_config"]
    for case in CASES:
        print(f"{case!r} | v1={checkers['v1'](case)} | v2={checkers['v2'](case)}")


if __name__ == "__main__":
    main()
