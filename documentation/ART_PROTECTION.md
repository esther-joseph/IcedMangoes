# Protect Your Art (Glaze / WebGlaze / Nightshade)

[← Back to Wiki](README.md)

This guide explains how to use University of Chicago SAND Lab tools to help protect your artwork from AI style mimicry and unauthorized training. **IcedMangoes does not run these tools.** You process images on your own device before uploading to your store.

---

## A) What These Tools Are

- **Glaze** — A desktop application that adds subtle alterations to images to make it harder for AI models to mimic your artistic style. Images remain viewable but become less useful for style extraction.
  - [Official Glaze (desktop)](https://glaze.cs.uchicago.edu/)
  - [WebGlaze (browser-based)](https://glaze.cs.uchicago.edu/webglaze.html)

- **WebGlaze** — Browser-based version of Glaze. No installation required; may require invite or account.
  - [WebGlaze](https://glaze.cs.uchicago.edu/webglaze.html)

- **Nightshade** — A desktop application that creates “poisoned” images intended to discourage training on scraped images. Aimed at affecting models that train on web-scraped data.
  - [Official Nightshade](https://nightshade.cs.uchicago.edu/)

**These are third-party tools.** Review the official documentation and terms before use. Effectiveness and compatibility can change.

---

## B) When to Use Which

| Tool | Use when |
|------|----------|
| **Glaze / WebGlaze** | You are posting public portfolio images and want to reduce the risk of style mimicry. |
| **Nightshade** | You are sharing images publicly and want to discourage unauthorized training. Nightshade targets training-time misuse, not normal viewing. |

### Tradeoffs

- **Processing time** — Both tools can take minutes per image depending on resolution and strength.
- **Visual artifacts** — There may be minor visible changes; test on copies before batch processing.
- **Keep originals** — Always retain unmodified high-resolution originals for printing and archives.

---

## C) Recommended Workflow for IcedMangoes

1. **Keep a master/original folder** — Store high-resolution originals. Do not upload these to the web.
2. **Create a “Web” export folder** — Downsize images (e.g., 1600–2400px longest edge). Add watermarks if desired.
3. **Apply Glaze or WebGlaze** — Process your web exports. Choose a strength that balances protection and visual quality.
4. **Optionally apply Nightshade** — If desired, process the same web exports with Nightshade.
5. **Upload protected web exports** — Use the processed images in IcedMangoes. Never replace your originals.
6. **Keep masters private/offline** — Use originals only for printing, high-res sales, or archives.

---

## D) Best Practices for an Artist Storefront

- **Web-friendly size** — Use 1600–2400px longest edge for display images. Reduces bandwidth and limits hi-res scraping value.
- **Format** — Use WebP or AVIF if your workflow supports it (optional).
- **Watermarks** — Consider subtle visible watermarks on marketplace previews (optional).
- **High-res behind paywall** — If you sell digital files, keep full-resolution downloads behind authentication.

---

## E) How-To (High Level)

### Glaze (Desktop)

1. Download from the [official Glaze page](https://glaze.cs.uchicago.edu/).
2. Install and run the application.
3. Select your web export images.
4. Choose strength (start with default; adjust if needed).
5. Export processed images to a new folder.
6. Upload the exported images to your store.

### WebGlaze

1. Go to [WebGlaze](https://glaze.cs.uchicago.edu/webglaze.html).
2. Request access if required.
3. Upload images, set strength, and download glazed outputs.
4. Upload the downloaded images to your store.

### Nightshade

1. Download from the [official Nightshade page](https://nightshade.cs.uchicago.edu/).
2. Install and run.
3. Select images, choose strength, and export.
4. Keep originals separate. Use Nightshade outputs only for web display.
5. Upload processed images to your store.

**Do not use unofficial download sources.** Use only the official UChicago links above.

---

## F) FAQ / Troubleshooting

**Do I upload the protected image or the original?**  
Upload the **protected** image for public display. Keep the original for printing and private archives.

**Will this affect print quality?**  
Use **originals** for print masters. Protected versions are for web display. Do not use Glaze/Nightshade outputs for professional prints.

**Do I need both Glaze and Nightshade?**  
Optional. Depends on your risk tolerance and workflow. Glaze focuses on style mimicry; Nightshade focuses on training-time misuse. You can use one, both, or neither.

---

## G) Disclaimers

- **Third-party tools** — Glaze, WebGlaze, and Nightshade are developed by University of Chicago SAND Lab. IcedMangoes is not affiliated with them. Effectiveness, compatibility, and availability may change. Always review the official docs and terms.
- **Your responsibility** — Artists are responsible for compliance with platform terms, applicable laws, and their own policies.
- **No guarantee** — This template does not guarantee protection from scraping, training, or misuse. These tools are one option among many practices (watermarking, lower resolution, terms of use, etc.).
