# PC release packaging

The release is an unpack-and-run folder. Windows uses a GUI executable
(no console window); Linux uses the SDL executable, built against the
existing Debian 11 i386 sysroot. Both remain 32-bit builds.

```text
yfm-redecomp-<version>/
  memories-pc.exe + SDL3.dll    # Windows ZIP
  memories-pc                  # Linux tar.gz, executable permission retained
  README.txt
  LICENSE
  buildid
  commit
  game/README.txt              # optional auto-detected ROM location
  mods/                       # bundled mods, from tracked project files
  sdk/                        # headers, tools, examples, modding notes
  symbols/                    # this build's crash/save-state symbol tables
```

GitHub shows each release asset's SHA-256 itself, so there are no
`.sha256` files beside the archives. No ROM, extracted game data, user
settings, saves, reports or personal HD packs belong in the archive. Release
builds omit the optional executable icon extracted from a local disc.

## Launch experience

If a remembered or auto-detected disc is available, launch goes straight
into the game. Otherwise a normal information dialog welcomes the player,
explains the USA SLUS-01411 raw `.bin` requirement, and offers **Choose ROM...**
and **Quit**. Choose ROM opens the system file picker. Cancel exits with
status zero. Invalid/unreadable selections show an error and allow another
attempt. Failure to save the location is also reported.

Only the path is saved, as UTF-8 in `disc-path.txt` in the existing user
folder. The ROM is never copied or modified. A moved/missing selection brings
setup back on the next launch. The existing `game/` discovery and explicit
`MEMORIES_DISC` override still work. Headless launches and a broken explicit
override fail without opening a picker. The developer X11 backend retains
folder/environment-based discovery; shipped builds explicitly use SDL.

SDL's asynchronous picker is awaited while pumping events, with the crash
monitor paused for user interaction. Linux uses the desktop portal or Zenity;
a failed picker explains the `game/` folder fallback. See the
[SDL dialog contract](https://wiki.libsdl.org/SDL3/SDL_ShowOpenFileDialog).

## GitHub build flow

`.github/workflows/pc-release.yml` builds on pull requests, pushes to `master`,
`v*` tags and manual dispatch. Native Ubuntu and Windows runners use the
existing dependency/toolchain fetchers and cache only dependencies. Linux
selects GCC 14 because the game source build uses C `-fpermissive`.

Every build uploads a Windows ZIP or Linux tar.gz as an Actions
artifact, retained for 14 days. On a version tag, both jobs must succeed before
the final job creates a **draft** GitHub release and attaches both packages.
Reruns can update a draft but refuse to replace an already published release.

Two kinds of tag:

- `v0.2.0-preview.1` (any hyphen, also `-rc.1`, `-beta.2`): a **preview**.
  The draft is marked as a pre-release, so GitHub labels it and "Latest
  release" keeps pointing at the last real one.
- `v0.2.0`: a **release**, a normal draft.

To make one: `git tag v0.2.0-preview.1 origin/master && git push origin
v0.2.0-preview.1`, wait for the workflow, test the attached archives, then
edit the draft on the Releases page and press Publish. Nothing is public
until then. A bad draft can be deleted along with its tag
(`gh release delete v0.2.0-preview.1 --cleanup-tag`).
The normal PC foundation workflow continues running the full adapter tests
on both platforms; it also includes the new ROM setup tests.

Public runners do not receive a disc or need a ROM secret. They compile the
full game and check archive structure; they skip ROM-dependent gameplay smoke
tests explicitly. Run those locally before publishing a draft. Workflow events
follow [GitHub's trigger documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## Local commands

```sh
# Build the CTests used by the Linux smoke runner first:
cmake -S . -B tmp/pc/cmake-test -DCMAKE_BUILD_TYPE=Release
cmake --build tmp/pc/cmake-test --parallel

# Build, smoke-test with your own disc, then package both platforms:
python tools/pc/package.py --version v0.1.0

# Compile/package without a disc (the CI path):
python tools/pc/package.py linux --skip-smoke --version dev-preview
python tools/pc/package.py windows --skip-smoke --version dev-preview

# Inspect the artifacts without a disc:
python tools/pc/test_package.py --archives dist
```

`--no-build` packages existing outputs; use it only after explicitly building
with `--release`, since it cannot change a previously built executable.
Windows builds use `tmp/pc/win32` during packaging on both host platforms.

Before publishing: play-test the packaged builds on Linux and real Windows,
including first-run selection, invalid selection, cancellation, moving the
ROM, restart with the remembered path, sound, controller input, and an in-game
save/load. Wine checks help but do not replace native Windows validation.
Upgrade by extracting into a fresh folder. User settings and memory-card
saves persist; cross-build save-state compatibility is not guaranteed.
