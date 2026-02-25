# Next.js Component Structure

Production-ready React components following atomic design and Next.js App Router conventions.

## File Structure

```
src/components/
├── atoms/              # Smallest building blocks
│   ├── Badge.tsx       # Server - cart count badge
│   ├── Button.tsx      # Server - reusable button variants
│   ├── Input.tsx       # Server - form input with label/error
│   └── ProductImage.tsx# Server - next/image wrapper for product images
├── molecules/          # Combinations of atoms
│   ├── AddToCartButton.tsx  # Client - cart context + button
│   ├── CartItem.tsx         # Client - cart line item
│   ├── CartLink.tsx         # Client - nav cart link + badge
│   ├── CheckoutButton.tsx   # Client - Stripe checkout
│   ├── EmptyState.tsx       # Server - empty state message
│   ├── Hero.tsx             # Server - hero section
│   ├── Pagination.tsx       # Server - Link-based pagination
│   └── ShopSearch.tsx       # Client - search form
├── organisms/          # Complex sections
│   ├── Navbar.tsx      # Server - site navigation
│   ├── ProductCard.tsx # Server - product link card
│   └── ProductGrid.tsx # Server - grid of ProductCards
└── templates/          # Page layouts
    └── PageLayout.tsx  # Server - max-width container
```

## Server vs Client Components

| Component | Type | Reason |
|-----------|------|--------|
| Badge, Button, Input, ProductImage | Server | No interactivity |
| Hero, EmptyState, Pagination | Server | Static content, Link only |
| Navbar, ProductCard, ProductGrid | Server | Composition, no state |
| PageLayout | Server | Layout wrapper |
| AddToCartButton, CartItem, CartLink | Client | useCart context |
| CheckoutButton | Client | useState, fetch |
| ShopSearch | Client | useRouter, useTransition |

## Conventions

- **next/link** for internal navigation (no `<a>` for same-site links)
- **next/image** for product images (`ProductImage` uses `unoptimized` for external URLs)
- **Tailwind CSS** - all classes preserved from original HTML
- **TypeScript** - typed props for all components
- **Accessibility** - aria-label, aria-describedby, semantic HTML
