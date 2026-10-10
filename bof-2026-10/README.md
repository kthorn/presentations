# Agentic Engineering BoF — 3 slides

1. `slide1` — Projects for an audience of one (mixology.tools, Infinite Armory, Sauron's Mace cosplay)
2. `slide2` — Ariadne: chemists design strategies, agents explore the molecules
3. `slide3` — What makes a domain agent-ready? (data vs. language + checker)

## Build

```bash
npm ci
python3 slide1.py                     # slide1.svg is generated (cocktail map drawn from assets/mixology-em.json)
node render.mjs slide1 slide2 slide3  # SVG -> 3200x1800 PNG via headless Chromium
```

`slide2.svg` and `slide3.svg` are hand-edited. Montserrat is bundled in `fonts/`.
`render.mjs` uses the Playwright Chromium at `~/.cache/ms-playwright/chromium-1234`; override with `CHROME=/path/to/chrome`.

Plan and rationale: `../docs/2026-10-05-bof-talk-design.md`.
