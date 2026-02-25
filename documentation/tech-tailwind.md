# Tailwind CSS

[← Back to Wiki](README.md)

## Overview

The frontend uses Tailwind CSS via PostCSS (no Tailwind CLI) for reliability.

## Build Commands

```bash
npm run build:css        # One-time build
npm run build:css:watch  # Watch mode for development
```

Output: `store/static/store/css/output.css`

## Configuration

- **Config**: `tailwind.config.js`
- **Content**: `./store/templates/**/*.html`, `./config/templates/**/*.html`
- **Input**: `store/static/store/css/input.css`

## Theme System

Theme colors are defined in `store/static/store/css/themes.css` with CSS custom properties:

| Variable | Purpose |
|----------|---------|
| `--theme-bg` | Page background |
| `--theme-bg-card` | Card background |
| `--theme-bg-header` | Header background |
| `--theme-text` | Primary text |
| `--theme-text-muted` | Secondary text |
| `--theme-accent` | Accent / buttons |
| `--theme-border` | Borders |
| `--theme-shadow` | Shadows |

Themes are applied via `data-theme` on `<html>` (e.g. `data-theme="lavender"`).
