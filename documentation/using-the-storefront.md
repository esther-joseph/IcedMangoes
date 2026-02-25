# Using the Storefront

[← Back to Wiki](README.md)

This guide covers the **Django backend** storefront (http://localhost:8000). For the Next.js frontend, see [Frontend: Vercel + Supabase](frontend-vercel-supabase.md).

---

## Browsing Artworks

The main page shows a Pinterest-style masonry grid of available artworks. Each card displays:

- Image
- Title
- Artist name
- Description
- Tags (if set)
- Price (“From $X”)

**Click any artwork card** to open the detail modal with image carousel, product options, and add-to-cart.

---

## Artwork Detail Modal

When you click an artwork card:

- **Image carousel** — Swipe or use arrows to view multiple images (artwork + product-type images)
- **Product form dropdown** — Select an option (e.g. Print 8x10, Canvas) with its price
- **Add to cart** — Enabled after selecting a product option; adds the chosen variant
- **Close** — Click X, Escape, or click outside the modal to close

---

## Changing Theme

Click the **Theme** button in the header to open the theme selector. Choose from:

- Cute Beige (default)
- Lavender
- Baby Blue
- Peach Pink
- Slate Gray
- Mint Green
- Coral Red

Your choice is stored in the browser and persists across visits.

---

## Adding an Artwork

1. Click the **+** (plus) button in the header.
2. The Add Artwork modal opens with a 3-step flow.
3. **Close button** or **click outside** the modal discards all entered data (no save).

### Step 1: Upload Images

- Click or drag and drop images (minimum 1 required).
- **Requirements**: PNG, JPG, GIF; max 5 MB each; recommended 1200×1200 px.
- Add multiple images; each shows a preview with a remove (×) button.

### Step 2: Details

- **Artist name** (required)
- **Title** (required)
- **Description** (required)
- **Tags** (optional, comma-separated)
- **Price** (required, $)
- **Product form options** (optional) — One per line: `Name, Price` (e.g. `Print 8x10, 25.00`)

### Step 3: Review & Post

- Review the summary including product options.
- Click **Post** to add the artwork to the gallery.

## Modal Navigation

- **Back** / **Next** move between steps.
- Breadcrumb dots let you jump to completed steps.
- **X** or **Escape** or **click outside** closes the modal (data is not saved).
