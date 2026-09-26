#!/usr/bin/env python3
"""Check release archives without a ROM: layout, modes, no user data."""
import argparse
from pathlib import Path, PurePosixPath
import tarfile
import zipfile


def check(path):
    windows = path.suffix == ".zip"
    if windows:
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
            names = archive.namelist()
    else:
        with tarfile.open(path) as archive:
            members = archive.getmembers()
            names = [item.name for item in members if item.isfile()]
            assert all(item.isfile() or item.isdir() for item in members), "unexpected links or special files"
            executable = [item for item in members if item.name.endswith("/memories-pc")]
            assert len(executable) == 1 and executable[0].mode & 0o111, "Linux executable must be executable"
    roots = {PurePosixPath(name).parts[0] for name in names}
    assert len(roots) == 1, "archive needs one top-level folder"
    assert all(not PurePosixPath(name).is_absolute() and ".." not in PurePosixPath(name).parts for name in names)
    contents = {str(PurePosixPath(name).relative_to(next(iter(roots)))) for name in names}
    required = {"README.txt", "LICENSE", "buildid", "commit", "game/README.txt",
                "memories-pc.exe" if windows else "memories-pc"}
    if windows:
        required |= {"SDL3.dll", "memories-pc.pdb"}
    assert required <= contents, f"missing files: {required - contents}"
    for directory in ("mods/", "sdk/", "symbols/"):
        assert any(name.startswith(directory) for name in contents), f"missing {directory}"
    assert {name for name in contents if name.startswith("game/")} == {"game/README.txt"}
    assert not any(name.startswith(("saves/", "reports/", "tmp/", "mods/assets-hd/")) or
                   name in {"disc-path.txt", "settings.ini", "controls.ini"} or
                   PurePosixPath(name).suffix.lower() in {".bin", ".cue", ".iso", ".chd", ".mcr"}
                   for name in contents), "archive contains personal or disc data"
    print(f"{path.name}: layout passed ({len(contents)} files)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archives", type=Path, required=True)
    args = parser.parse_args()
    archives = sorted(args.archives.glob("*.zip")) + sorted(args.archives.glob("*.tar.gz"))
    assert archives, "no release archives found"
    for path in archives:
        check(path)


if __name__ == "__main__":
    main()
