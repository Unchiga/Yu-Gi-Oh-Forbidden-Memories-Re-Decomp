YFM Re-Decomp
=============

A native PC version of Yu-Gi-Oh! Forbidden Memories (PlayStation, USA),
rebuilt from the decompiled game. It is a work in progress.

No part of the game's disc comes with it. You need your own copy.


Getting started
---------------

1. Make a raw image of your Yu-Gi-Oh! Forbidden Memories disc (USA,
   SLUS-01411): the .bin file of a .bin/.cue pair.

2. Extract the whole release archive into a folder.

3. Start the game:
     Windows: memories-pc.exe
     Linux:   ./memories-pc   (see "Linux" below)

4. On the welcome screen, choose "Choose ROM..." and select your .bin.
   The game remembers its location; the ROM stays where you keep it.
   Next time, the game starts directly. Cancel or Quit closes normally.

If you move or remove your ROM, setup asks you to locate it again. Choosing
an unsupported or unreadable file shows an error and lets you try again.
You can also place a .bin in the "game" folder beside the program to have
it detected automatically. The supported format is raw MODE2/2352, USA
SLUS-01411; select the .bin, not the .cue. ISO/CHD and other regions are
not supported.


Controls
--------

Keyboard (change these, or set up a controller, in Game > Controls on the
menu bar):

  Arrow keys   D-pad            X   Cross        S   Circle
  Enter        Start            Z   Square       A   Triangle
  Right Shift  Select           Q/W L1/R1        E/R L2/R2
                                T/Y L3/R3

  Esc          close an open menu; with none open, quit
  F5 / F7      save / load a state      F1, F2, F4  choose the state slot

Controllers (Xbox, PlayStation and most others) work out of the box.


Your files
----------

Settings, controls, memory cards, save states and your own mods are kept
in your user folder, not next to the program:

  Windows: Documents\My Games\YFM Re-Decomp
  Linux:   ~/.local/share/YFM Re-Decomp

To update, extract the new release into a fresh folder and launch it.
Your ROM selection, settings and memory-card saves stay in your user folder.
Save states may depend on the build; use an in-game save before updating.


Mods
----

Game > Mods lists the mods the game found and lets you turn them on and
off. The release includes:

  3D Monsters  face-up monsters stand on their cards as 3D models
  Hand Camera  L1/R1 turn and L3/R3 zoom the duel camera while the
               hand is up
  AI Hard Mode optional opponent AI changes
  Yamyi Mods   optional gameplay adjustments

To install someone else's mod, put its folder in the "mods" folder of your
user folder. A mod that contains code runs as part of the game, so only
install mods from people you trust. Mod authors: see sdk/notes/modding.md,
sdk/examples/mods and sdk/tools (build_mod.py builds a code mod;
extract_images.py and upscale_pack.py make texture packs).


Linux
-----

This is a 32-bit program, like the game it comes from. It needs the 32-bit
graphics driver (and, for sound, the 32-bit PulseAudio or ALSA library).
If you have Steam installed, you already have them. If not:

  Debian/Ubuntu:  sudo dpkg --add-architecture i386 && sudo apt update
                  sudo apt install libgl1:i386 libgl1-mesa-dri:i386 libpulse0:i386
  Fedora:         sudo dnf install mesa-libGL.i686 mesa-dri-drivers.i686 pulseaudio-libs.i686
  Arch:           enable [multilib], then: sudo pacman -S lib32-mesa lib32-libpulse

The build targets Debian 11-era system libraries. A desktop file picker
requires an XDG desktop portal or Zenity (package "zenity"). If the picker
is unavailable, put your .bin in the "game" folder beside the executable.


Problems
--------

If the game crashes or stops responding, it writes a report to the
"reports" folder in your user folder (crash-*.txt, hang-*.txt, and on
Windows a .dmp file) and shows where. Please include them, and
last-session.log from the same folder, when you report a problem.
