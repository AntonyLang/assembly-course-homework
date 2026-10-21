"""Explicit opt-in download and setup of official portable tools (Windows x64)."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    records = json.loads((ROOT / "docs" / "toolchain.json").read_text(encoding="utf-8"))
    downloads = ROOT / "tools" / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    for package in records:
        archive = downloads / package["name"]
        print(f"Downloading {package['name']} from its official project...", flush=True)
        request = urllib.request.Request(package["url"], headers={"User-Agent": "assembly-course"})
        with urllib.request.urlopen(request, timeout=60) as response:
            archive.write_bytes(response.read())
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        assert digest == package["sha256"], f"SHA-256 mismatch: {archive.name}"
        with zipfile.ZipFile(archive) as zipped:
            zipped.extractall(ROOT / "tools" / package["directory"])
    source_parent = ROOT / "tools" / "jwasm-source"
    source = next(path for path in source_parent.iterdir() if path.is_dir())
    output = ROOT / "tools" / "jwasm" / "JWasm64.exe"
    output.parent.mkdir(parents=True, exist_ok=True)
    compiler = shutil.which("gcc")
    print("Building native x64 JWasm from official v2.20 source with existing GCC...", flush=True)
    command = [compiler, "-std=gnu89", "-O2", "-D__NT__", "-DNDEBUG", "-Isrc/H"]
    command += [str(path.relative_to(source)) for path in sorted((source / "src").glob("*.c"))]
    command += ["-s", "-o", str(output)]
    result = subprocess.run(command, cwd=source, capture_output=True)
    (ROOT / "tools" / "jwasm-build.log").write_bytes(result.stdout + result.stderr)
    result.check_returncode()
    print("Ready. Next: python scripts/build_all.py")


if __name__ == "__main__":
    main()
