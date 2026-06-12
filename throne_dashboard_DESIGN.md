---
version: "1.0"
name: Coco's Divine Astromantic Throne
description: "A dark occult-themed astrology dashboard. Deep purple-black canvas with gold accents and pink highlights. Mystical, luxurious, and precise."

colors:
  canvas: "#0d0015"
  canvas-soft: "#1a0a2e"
  canvas-panel: "#23103a"
  canvas-elevated: "#2d1a4a"
  primary: "#c9a84c"
  primary-dim: "#a08030"
  primary-glow: "#f4d03f"
  accent: "#e91e9e"
  accent-dim: "#a0156e"
  accent-glow: "#ff6bcd"
  ink: "#e8d8f8"
  ink-dim: "#9a8aaa"
  ink-muted: "#6a5a7a"
  ink-subtle: "#4a3a5a"
  hairline: "#3a1a6e"
  hairline-strong: "#5a2a8e"
  success: "#81c784"
  warning: "#f4d03f"
  danger: "#e57373"
  info: "#64b5f6"

typography:
  display-xl:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "3rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  display-lg:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "2rem"
    fontWeight: 600
    lineHeight: 1.2
  headline:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.3
  body-lg:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "1.1rem"
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 400
    lineHeight: 1.4
  label:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 500
    letterSpacing: "0.05em"
    textTransform: "uppercase"

rounded:
  sm: "4px"
  md: "8px"
  lg: "12px"
  xl: "16px"
  full: "9999px"

spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  xxl: "48px"

shadows:
  sm: "0 1px 2px rgba(0,0,0,0.3)"
  md: "0 4px 8px rgba(0,0,0,0.4)"
  lg: "0 8px 24px rgba(0,0,0,0.5)"
  glow-gold: "0 0 20px rgba(201,168,76,0.3)"
  glow-pink: "0 0 20px rgba(233,30,158,0.3)"

---

## Overview

Coco's Divine Astromantic Throne is a real-time astrological computation dashboard. The design language is **dark occult luxury** — deep purple-black surfaces, gold for primary actions and important data, pink/magenta for accents and highlights. The aesthetic is mystical yet precise, like a high-end astrological instrument.

## Design Principles

1. **Dark First**: The canvas is always deep purple-black (#0d0015). Light surfaces are used sparingly for cards and panels.
2. **Gold = Primary**: Gold (#c9a84c) is the primary accent — used for headings, active states, important values, and interactive elements.
3. **Pink = Accent**: Pink (#e91e9e) is the secondary accent — used for moon phase, feminine energy, and special highlights.
4. **Precision**: Astrological data must be displayed with exact degrees, minutes, and seconds. Typography should be clean and readable.
5. **Mystical Atmosphere**: Subtle gradients, glowing effects, and occult symbols (☽ ☉ ♃ ♄ ♅ ♆ ♇) create the atmosphere without sacrificing usability.

## Color Usage

- **Canvas (#0d0015)**: Main background
- **Surface (#1a0a2e)**: Card backgrounds, tab content areas
- **Surface 2 (#23103a)**: Nested panels, table headers, secondary surfaces
- **Gold (#c9a84c)**: Primary text, active tabs, planet glyphs, important values
- **Pink (#e91e9e)**: Moon-related elements, special highlights, retro badges
- **Ink (#e8d8f8)**: Body text on dark surfaces
- **Hairline (#3a1a6e)**: Borders, dividers, table rows

## Component Patterns

### Cards
- Background: var(--surface)
- Border: 1px solid var(--hairline)
- Border-radius: 8px
- Padding: 1.5rem
- Box-shadow: var(--shadow-md)

### Tables
- Header: var(--surface2) background, uppercase labels, 0.75rem font
- Rows: alternating var(--surface) / var(--surface2)
- Hover: var(--hairline-strong) border highlight
- Selected: var(--gold) left border accent

### Tabs
- Active: var(--gold) text, 2px bottom border
- Inactive: var(--text-dim) text
- Hover: var(--ink) text

### Buttons
- Primary: var(--gold) background, var(--canvas) text, 8px radius
- Secondary: transparent, var(--gold) border and text
- Hover: glow effect (box-shadow: var(--shadow-glow-gold))

### Stat Cards
- Label: var(--text-muted), uppercase, 0.75rem
- Value: var(--ink), 1.25rem, 600 weight
- Gold variant: var(--gold) value
- Pink variant: var(--accent) value

## Planet Glyphs

| Planet | Glyph | Color |
|--------|-------|-------|
| Sun | ☉ | #f4d03f |
| Moon | ☽ | #c0c0c0 |
| Mercury | ☿ | #b0a0d0 |
| Venus | ♀ | #f0a0c0 |
| Mars | ♂ | #e05050 |
| Jupiter | ♃ | #d4a017 |
| Saturn | ♄ | #c8a860 |
| Uranus | ♅ | #4dd0e1 |
| Neptune | ♆ | #1565c0 |
| Pluto | ♇ | #8d6e63 |

## Zodiac Glyphs

| Sign | Glyph |
|------|-------|
| Aries | ♈ |
| Taurus | ♉ |
| Gemini | ♊ |
| Cancer | ♋ |
| Leo | ♌ |
| Virgo | ♍ |
| Libra | ♎ |
| Scorpio | ♏ |
| Sagittarius | ♐ |
| Capricorn | ♑ |
| Aquarius | ♒ |
| Pisces | ♓ |
