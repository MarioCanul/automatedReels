# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A batch generator for vertical (9:16, 1080×1920) social-media reels. It composes a background video, a music track, and overlaid text (with outline + shadow + optional logo) into one MP4 **per row** of a CSV. Built on MoviePy 2.2.1.

## Commands

Use the venv interpreter directly (there is no activation step in scripts):

```bash
# Install deps (Windows path shown; this is a Windows-first project)
./venv/Scripts/python.exe -m pip install -r requirements.txt

# Generate all reels (one per CSV row) using config.yaml
./venv/Scripts/python.exe generar.py

# Use an alternate config
./venv/Scripts/python.exe generar.py path/to/other-config.yaml
```

There is no test suite, linter, or build step. To smoke-test a single module without rendering, run it via `python -c`, e.g. quick TextClip check:
`./venv/Scripts/python.exe -c "from reels import text; ..."`.

## Architecture

`generar.py` is a thin orchestrator. The real work lives in the `reels/` package, one module per concern, each a pure function called by the orchestrator:

- **`config.py`** — `cargar_config()` loads `config.yaml`, deep-merges it over `DEFAULTS`, and validates that the fondos folder, CSV, and music file exist. A missing/partial YAML still works because every key has a default. **The full default schema lives in `DEFAULTS` here** — update it when adding config keys.
- **`csv_loader.py`** — `cargar_textos()` reads the `texto` column (other columns are preserved in `item["fila"]` for future per-row overrides like per-row music/background). Empty rows are skipped. Output filenames are derived as `{prefijo}_{NN:02d}.mp4` so runs never overwrite each other.
- **`background.py`** — picks the first `.mp4` in the fondos folder, scales by height then center-crops to the target size. Returns `(clip, duracion_real)`; duration is `min(duracion_max, video.duration)`.
- **`audio.py`** — trims music safely with `min(duracion, audio.duration)` so a track shorter than the video does not raise.
- **`text.py`** — builds the text layers: main `TextClip` with native stroke (`stroke_color`/`stroke_width`) plus an optional offset, semi-transparent shadow clip. Returns layers in composite order (shadow first, then text). Falls back to the default font if the configured `.ttf` is missing (prints a warning, does not fail).
- **`branding.py`** — optional logo/watermark `ImageClip`, scaled as a fraction of video width, positioned by corner name. Returns `None` when disabled or the logo file is missing.
- **`renderer.py`** — composes `[fondo, *capas_texto, logo?]` into a `CompositeVideoClip`, attaches audio, and writes the MP4.

### Data flow (per CSV row)

`config → csv_loader → [for each item] background + audio + text + branding → renderer → salida/reel_NN.mp4`

Each row reloads its own background/audio clips so clips are never reused across renders. A failure on one row is caught in `generar.py` and logged without aborting the batch.

## Key conventions

- **All tuning is data, not code.** Style, paths, render settings, and branding live in `config.yaml`. Adding a new knob means: add it to `DEFAULTS` in `config.py`, then read it in the relevant module — don't hard-code values in the modules.
- **Code and comments are in Spanish.** Match this (function names, docstrings, log messages).
- **MoviePy 2.x API** — methods are the `.with_*()` / `.resized()` / `.cropped()` / `.subclipped()` style (not the 1.x `.set_*()` names). Keep to this.
- Inputs: backgrounds in `fondos/` (`.mp4`), music at the path in `config.yaml`, fonts/logo in `assets/`. Outputs go to `salida/`. `venv/` is the committed environment.
