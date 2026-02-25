# Atomic Design: Component Hierarchy

[← Back to Wiki](README.md)

This document describes the atomic design structure used for UI components in IcedMangoes. Components are organized into **atoms**, **molecules**, **organisms**, **templates**, and **pages**.

---

## Principles

- **Atoms**: Smallest, indivisible UI elements (buttons, inputs, icons, labels)
- **Molecules**: Combinations of atoms that form a functional unit (search bar = input + button)
- **Organisms**: Complex sections made of molecules and/or atoms (nav bar, product card, modals)
- **Templates**: Page-level layouts that place organisms
- **Pages**: Specific instances of templates with real content

Dependencies flow **downward only**: organisms use molecules and atoms; molecules use atoms; atoms use nothing UI-related.

---

## Django (store templates)

**Base path**: `store/templates/store/components/`

### Folder structure

```
components/
├── atoms/           # Smallest building blocks
│   └── button_add_artwork.html
├── molecules/       # Functional combinations
│   ├── cart_button.html
│   └── theme_switcher.html
└── organisms/       # Complex sections
    ├── nav_bar.html
    ├── artwork_card.html
    ├── pinterest_board.html
    ├── artwork_detail_modal.html
    ├── add_artwork_modal.html
    ├── admin/
    │   ├── admin_stripe_integration.html
    │   └── admin_artwork_list.html
    └── business/
        ├── integration_card.html
        ├── integration_none_manual.html
        └── integration_none_pod.html
```

### Classification

| Component | Level | Description |
|-----------|-------|-------------|
| `button_add_artwork` | Atom | Circular "+" button that opens add-artwork modal |
| `cart_button` | Molecule | Cart icon + badge + dropdown with cart items and checkout |
| `theme_switcher` | Molecule | Theme trigger button + dropdown with theme options |
| `nav_bar` | Organism | Sidebar navigation with links, cart, add-artwork button |
| `artwork_card` | Organism | Card with image, title, artist, description, price |
| `pinterest_board` | Organism | Masonry grid of artwork cards |
| `artwork_detail_modal` | Organism | Modal with carousel, product select, add-to-cart |
| `add_artwork_modal` | Organism | 3-step add-artwork flow (images, details, review) |
| `admin_stripe_integration` | Organism | Stripe keys form section |
| `admin_artwork_list` | Organism | List of artworks with update/delete |
| `integration_card` | Organism | Provider config card (API key, status, test) |

### Include examples

```django
{% include "store/components/atoms/button_add_artwork.html" %}
{% include "store/components/molecules/cart_button.html" %}
{% include "store/components/molecules/theme_switcher.html" %}
{% include "store/components/organisms/nav_bar.html" %}
{% include "store/components/organisms/pinterest_board.html" with artworks=artworks %}
{% include "store/components/organisms/admin/admin_stripe_integration.html" %}
```

---

## Next.js (frontend)

**Base path**: `frontend/src/components/`

### Folder structure

```
components/
├── atoms/           # Smallest building blocks (placeholder for future)
├── molecules/       # Functional combinations
│   ├── AddToCartButton.tsx
│   ├── CartLink.tsx
│   ├── CheckoutButton.tsx
│   └── ShopSearch.tsx
└── organisms/       # Complex sections
    ├── Navbar.tsx
    └── ProductCard.tsx
```

### Classification

| Component | Level | Description |
|-----------|-------|-------------|
| `AddToCartButton` | Molecule | Button + cart context logic |
| `CartLink` | Molecule | Link to cart + item count badge |
| `CheckoutButton` | Molecule | Checkout trigger + Stripe redirect logic |
| `ShopSearch` | Molecule | Search input + submit button |
| `Navbar` | Organism | Site nav with links and CartLink |
| `ProductCard` | Organism | Product image, title, description, price |

### Import examples

```tsx
import { Navbar } from "@/components/organisms/Navbar";
import { ProductCard } from "@/components/organisms/ProductCard";
import { AddToCartButton } from "@/components/molecules/AddToCartButton";
import { CartLink } from "@/components/molecules/CartLink";
import { CheckoutButton } from "@/components/molecules/CheckoutButton";
import { ShopSearch } from "@/components/molecules/ShopSearch";
```

---

## Adding new components

1. **Choose the right level**: Is it a single element (atom), a small combo (molecule), or a larger section (organism)?
2. **Place it** in the correct folder under `atoms/`, `molecules/`, or `organisms/`.
3. **Name it** descriptively: `button_primary`, `SearchForm`, `ProductGrid`, etc.
4. **Document** in this file when adding new patterns.

---

## References

- [Atomic Design by Brad Frost](https://atomicdesign.bradfrost.com/)
- [Architecture Overview](architecture.md)
