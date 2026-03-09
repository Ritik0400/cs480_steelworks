"""Fail pre-commit if GPL-family licenses are present in dependencies."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
import tomllib
from typing import Any


def main() -> int:
    try:
        result = subprocess.run(
            ["pip-licenses", "--format=json"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("pip-licenses is not installed in this environment.")
        return 1
    except subprocess.CalledProcessError as exc:
        print(exc.stdout)
        print(exc.stderr)
        return 1

    dependencies: list[dict[str, Any]] = json.loads(result.stdout)
    copyleft_pattern = re.compile(r"^(?:AGPL|GPL|LGPL)", re.IGNORECASE)
    project_lock = Path("poetry.lock")
    locked_packages: set[str] = set()
    if project_lock.exists():
        with project_lock.open("rb") as handle:
            lock_data = tomllib.load(handle)
        for package in lock_data.get("package", []):
            package_name = str(package.get("name", "")).strip().lower()
            if package_name:
                locked_packages.add(package_name)

    blocked: list[tuple[str, str]] = []

    for dependency in dependencies:
        package_name = str(dependency.get("Name", "<unknown>"))
        if locked_packages and package_name.lower() not in locked_packages:
            continue
        license_name = str(dependency.get("License", ""))
        if copyleft_pattern.search(license_name.strip()):
            blocked.append((package_name, license_name))

    if blocked:
        print("Detected disallowed GPL-family licenses:")
        for package_name, license_name in blocked:
            print(f"- {package_name}: {license_name}")
        print("Replace these dependencies before merging.")
        return 1

    print("No GPL/AGPL/LGPL licenses detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
