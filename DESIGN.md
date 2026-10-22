---
name: Deep Learning UIDE · Semana 1 — Sala de señales
description: Classic one-idea slides and teacher maps where the ideas run live; light only where a neuron is active.
colors:
  night: "oklch(0.17 0.03 258)"
  night-raised: "oklch(0.215 0.035 258)"
  night-line: "oklch(0.34 0.035 258)"
  grid: "oklch(0.25 0.03 258)"
  ink-light: "oklch(0.97 0.008 250)"
  ink-soft: "oklch(0.82 0.03 250)"
  signal-amber: "oklch(0.83 0.155 72)"
  signal-azure: "oklch(0.75 0.13 235)"
  learned-mint: "oklch(0.85 0.14 165)"
  error-coral: "oklch(0.72 0.17 28)"
  trend-lilac: "oklch(0.78 0.11 300)"
  paper: "oklch(0.99 0.003 250)"
  ink-dark: "oklch(0.22 0.03 258)"
typography:
  display:
    fontFamily: "Unbounded, Lexend, system-ui, sans-serif"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Lexend, system-ui, sans-serif"
    fontSize: "2.5em"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Lexend, system-ui, sans-serif"
    fontSize: "1.25em"
    fontWeight: 400
    lineHeight: 1.4
  label:
    fontFamily: "Lexend, system-ui, sans-serif"
    fontSize: "0.85em"
    fontWeight: 600
    letterSpacing: "0.02em"
  math:
    fontFamily: "KaTeX (embedded), only inside formulas"
    fontSize: "1em"
  code:
    fontFamily: "JetBrains Mono, ui-monospace, monospace"
    fontSize: "1em"
    fontWeight: 500
rounded:
  code: "0.35em"
  panel: "0.85em"
  plate: "1em"
  chip: "999px"
spacing:
  gutter: "5em"
  block: "1.5em"
  tight: "0.5em"
components:
  button-primary:
    backgroundColor: "{colors.signal-amber}"
    textColor: "{colors.night}"
    rounded: "{rounded.chip}"
    padding: "0.45em 1.1em"
  button-ghost:
    backgroundColor: "{colors.night-raised}"
    textColor: "{colors.ink-light}"
    rounded: "{rounded.chip}"
    padding: "0.45em 1.1em"
  panel:
    backgroundColor: "{colors.night-raised}"
    rounded: "{rounded.panel}"
    padding: "1.2em 1.4em"
  chip-key-idea:
    backgroundColor: "{colors.signal-amber}"
    textColor: "{colors.night}"
    rounded: "{rounded.chip}"
    padding: "0.2em 0.8em"
---

# Design System: Deep Learning UIDE · Semana 1

## Overview

**Creative North Star: "Sala de señales"**

A classic keynote (one idea per slide, huge clear type, title then proof) set in a night control room where the ideas run live. Signals travel along edges, a neuron lights up as strongly as it fires, a decision line turns when a weight changes, and the loss ball rolls downhill. The look is futuristic because the content moves like an instrument, not because of decoration.

Density is low on purpose: the slides are screen-shared in Microsoft Teams, so everything that carries meaning is large, thick and high contrast. The teacher drives every step; nothing important happens on a timer.

**Key Characteristics:**
- Deep blue-graphite night ground, never pure black; white Lexend type.
- Two diverging signal hues with fixed meaning: amber = sí / positive / class 1, azure = no / negative / class 0.
- Live figures on a faint coordinate grid; demos are the hero of most slides.
- Unbounded only for covers, section openers and big numbers.

## Colors

A night ground with five signal roles; color always means something.

### Primary
- **Signal Amber** (oklch(0.83 0.155 72)): positive weights, class 1 ("paga", "sí"), the active signal, primary buttons, key-idea badges.
- **Signal Azure** (oklch(0.75 0.13 235)): negative weights, class 0 ("no paga", "no"), the opposite side of a decision line.

### Secondary
- **Learned Mint** (oklch(0.85 0.14 165)): correct, converged, "ya lo aprendió"; inside a readable equation it marks what the network learns (weights and bias).
- **Error Coral** (oklch(0.72 0.17 28)): errors, blame traveling backward, traps.

### Tertiary
- **Trend Lilac** (oklch(0.78 0.11 300)): only for the thread that connects to the weekly trend readings.

### Neutral
- **Night** (oklch(0.17 0.03 258)): page ground.
- **Night Raised** (oklch(0.215 0.035 258)): panels and figure plates.
- **Night Line** (oklch(0.34 0.035 258)): hairlines, axes, inactive edges.
- **Grid** (oklch(0.25 0.03 258)): the coordinate grid; never carries meaning.
- **Ink Light** (oklch(0.97 0.008 250)) and **Ink Soft** (oklch(0.82 0.03 250)): primary and secondary text.
- **Paper** and **Ink Dark**: print and the light print version of the maps.

### Named Rules
**The Activation Rule.** Glow appears only on something that is active (a firing neuron, a traveling pulse) and its intensity encodes the value. No decorative halos.
**The Two-Hue Rule.** Amber and azure never swap meaning anywhere in the week.

## Typography

**Display Font:** Unbounded (fallback Lexend)
**Body Font:** Lexend (fallback system-ui)
**Code Font:** JetBrains Mono, only for code, numbers in demos and measurements.

**Character:** Unbounded gives the futuristic voice in a few large words; Lexend, designed for reading fluency, keeps every sentence effortless when compressed by Teams.

### Hierarchy
- **Display** (700, 4–7em, 1.02): cover titles, section openers, one big number.
- **Headline** (600, 2.5em, 1.1): slide titles, at most two lines.
- **Body** (400, 1.25em, 1.4): one or two sentences per slide.
- **Label** (600, 0.85em): chips, axis labels, demo readouts. Never below 20px at 1080p.

### Named Rules
**The One-Idea Rule.** One idea per slide: a title that states it, one proof (demo, example or number) and at most two short sentences.

## Layout

Fixed 16:9 stage (1920×1080 design canvas, 1em = 24px at full size), scaled to fit; 5em side gutters. Layouts: cover, section opener, statement, title + full figure, split (text 5 columns / demo 7 columns). Below 760px wide the deck switches to reading mode: slides stack vertically and grids collapse to one column.

## Elevation & Depth

Flat by default. Depth comes from tonal layering (night → night raised) and from light: active elements emit their own color. No drop shadows on panels.

## Shapes

Panels 0.85em radius; chips and buttons fully rounded; neurons are circles; edges are 3px or thicker when they carry meaning.

## Components

- **Live figure:** an SVG or canvas plate on Night Raised with the faint grid; readouts in JetBrains Mono.
- **Slider:** thick track in Night Line, amber thumb, value shown next to it.
- **Step reveal:** presenter-driven; new content arrives with a 500 ms exponential ease-out from slight blur.
- **Key-idea badge:** amber chip "Idea clave N" at the end of the title line (never above it) on the five slides measured by the quizzes.
- **Readable equation:** each term in its own cell with its meaning underneath (amber = the result, mint = what is learned, white = the data, dashed = η, the step you choose) and a «Léelo así» sentence in plain Spanish.
- **Dated note:** a rounded chip with the year and who had the idea (1847 · Cauchy…), so every concept carries its history.
- **Code walk-through:** Python with syntax colours; the presenter highlights one line per click and a Spanish explanation appears beside it. Code comments in English, short enough to never clip.
- **Presenter view:** separate window with notes, timer and next slide.

## Do's and Don'ts

- Do show the concept working before naming it.
- Do keep every meaningful line ≥3px and text ≥20px at 1080p.
- Don't use gradient text, glass panels or decorative glows.
- Don't put more than two sentences of body text on a slide; the rest goes to the speaker notes.
- Don't start loops the presenter cannot stop; respect prefers-reduced-motion.
