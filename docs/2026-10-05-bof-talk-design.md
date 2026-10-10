# Agentic Engineering BoF — 3-slide talk

**Event:** A Birds of a Feather Session on Agentic Engineering (Jesse Vincent & Simon Willison, Prime Radiant), SF, Wed 2026-10-14.
**Format:** informal show-and-tell for practitioners; no pitches. Organizers ask for "what you're learning, and what you haven't figured out yet."
**Deliverable:** three 16:9 PNGs, authored as SVG and rendered by headless-browser screenshot.

## Thesis

Engineering got cheap, so things that were never worth building now are — from a canal router for one holiday to a 400k-line agent that runs a five-person biotech. The general pattern underneath: **the LLM supplies general intelligence; the domain has to supply a language to act in and a way to check the result.** The open question: when a domain has no such language, do you write one, or train a domain foundation model?

## Arc

| # | Slide | Job | Time |
|---|---|---|---|
| 1 | Software for an audience of one | Warm open; sets up "cheap engineering" | ~1 min |
| 2 | Ariadne | Same thing at company scale; the concrete result | ~2 min |
| 3 | General intelligence + domain language + domain checks | The pattern, ending on the open question | ~1–2 min, then discussion |

Stack / how I work: voiceover only, during slide 1.

## Slide 1 — "Projects for an audience of one"

Three tiles, each: live-site screenshot, project name, one-line origin, one "not throwaway" stat.

| Tile | Origin | Stat | Screenshot |
|---|---|---|---|
| Infinite Armory | My son wanted D&D weapons on a ski trip | Built in ~a week | Weapon gallery grid (infinitearmory on Fly) |
| mixology.tools | I wanted to do ML on cocktail recipes — no dataset existed, so I built one | 800+ commits / 18 months; picks our weekend drinks | EM "cocktail space" map (`/analytics.html#cocktail-space-em`) |
| Sauron's Mace cosplay | Claude designed the 3D-printed core that holds the blades, then measured the fit | 1 weekend · OpenSCAD · 3D printer | Film prop (Royal Armouries replica photo, core outlined) beside the OpenSCAD render |

Footer line: *Not throwaway — just never worth engineering before.*

## Slide 2 — Ariadne

- Header label: `ARREPATH / ARIADNE`
- Headline: **Chemists design strategies. Agents explore the molecules.**
- Context strip: **5 people · ~400k lines since January · used daily by CEO, CSO and me**
- Three metric tiles, side by side, explicitly *not* a funnel: **20** design strategies · **32,000+** structures scored · **34** sent for synthesis — *one scientist, two weeks*.
- Division-of-work strip: Scientist sets strategy → Ariadne agents enumerate, score, dock → Scientist reviews and advances.
- One-line analogy for non-chemists: *a strategy is the tech lead's plan; molecules are the implementations.*
- Footnote: computational scores; experimental validation pending; program anonymized.

Source: `arrepath/slides` → `decks/ai-pitch/case-study4-design-strategies` (numbers and caveats per its README).

## Slide 3 — "What makes a domain agent-ready?"

Subtitle: LLMs bring general intelligence; the domain brings data, or a language plus a checker. Code has both. No mace box (moved to slide 1). Towpath and feedback speed (seconds for code vs weeks of synthesis) are voiceover.

A 2×2 map. X axis: data (real or simulated). Y axis: language + checker.
- Top-right, both: **Code** (GitHub, compilers, tests) — "where this room lives"
- Top-left, general LLM + DSL: **Math** (Lean), **Physical objects** (OpenSCAD; mace holder thumbnail)
- Bottom-right, foundation models: **Proteins** (100M+ evolved sequences, AlphaFold), **Image generation** (billions of captioned images); **Law** near the boundary (lots of text, no checker). Robotics removed (sim-to-real gap; really data-starved) — voiceover only.
- Bottom-left, neither: **Small-molecule drugs** (scarce data, approximate checks, no language; we're writing one)

Right panel, "What I haven't figured out": When a domain has no language, write one for a general agent or train a foundation model? Bitter lesson says train; the data says not yet. What are the right primitives for medicinal chemistry? How do you audit what the agent claims it did?

Lab robotics friend: left out pending their OK.

## Visual system

- Arrepath look across all three: Montserrat; NAVY `#4D6182`, CORAL `#F74F58`, BLUE `#3A96DB`; light background; small uppercase header label.
- Slide 1 header `KURT THORN / AFTER HOURS`; slides 2–3 `ARREPATH / ARIADNE` (slide 3 could be unlabeled since it spans both).
- Large type: legible from the back of a room; at most ~40 words of body text per slide.

## Build pipeline

- Files in `~/presentations/bof-2026-10/`: `slide{1,2,3}.svg`, `assets/` (screenshots, renders), `fonts/` (Montserrat, downloaded locally), `render.mjs`.
- Render: Playwright (installed Chromium) loads each SVG at 1600×900, device scale 2 → 3200×1800 PNG.
- Site screenshots via the same Playwright script, captured once and saved to `assets/`.
- Verify by viewing each PNG.

## Open items

- Lab robotics friend: omitted until Kurt checks with them.
- Build: `bof-2026-10/` — slide1.py (generates slide1.svg from assets/mixology-em.json), slide2.svg, slide3.svg; `node render.mjs slide1 slide2 slide3`.
