/**
 * Demo catalog for Vercel / local previews when Supabase is unset, errors, or empty.
 * Images in /public/demo-art are 440px JPEGs from Wikimedia Commons (public domain / CC).
 * Replace with real products in Supabase for production.
 */

export interface DemoCatalogProduct {
  id: string;
  title: string;
  description: string;
  price: number;
  image_url: string;
  tags: string[];
}

const DEMO_PREFIX = "demo-";

export const DEMO_PRODUCTS: readonly DemoCatalogProduct[] = [
  {
    id: `${DEMO_PREFIX}starry-night`,
    title: "The Starry Night (study print)",
    description:
      "Vincent van Gogh, 1889. Museum-quality reproduction for your demo storefront.",
    price: 189,
    image_url: "/demo-art/starry-night.jpg",
    tags: ["post-impressionism", "landscape", "demo"],
  },
  {
    id: `${DEMO_PREFIX}great-wave`,
    title: "The Great Wave off Kanagawa (study print)",
    description:
      "Katsushika Hokusai, c. 1830. Iconic Japanese woodblock — placeholder listing.",
    price: 145,
    image_url: "/demo-art/great-wave.jpg",
    tags: ["ukiyo-e", "seascape", "demo"],
  },
  {
    id: `${DEMO_PREFIX}girl-pearl-earring`,
    title: "Girl with a Pearl Earring (study print)",
    description:
      "Johannes Vermeer, c. 1665. Classic portrait — demo product only.",
    price: 165,
    image_url: "/demo-art/girl-pearl-earring.jpg",
    tags: ["baroque", "portrait", "demo"],
  },
  {
    id: `${DEMO_PREFIX}impression-sunrise`,
    title: "Impression, Sunrise (study print)",
    description:
      "Claude Monet, 1872. The painting that named Impressionism — demo placeholder.",
    price: 155,
    image_url: "/demo-art/impression-sunrise.jpg",
    tags: ["impressionism", "demo"],
  },
  {
    id: `${DEMO_PREFIX}sunflowers`,
    title: "Sunflowers (study print)",
    description:
      "Vincent van Gogh, 1888. Vibrant still life — sample listing for your store.",
    price: 175,
    image_url: "/demo-art/sunflowers.jpg",
    tags: ["post-impressionism", "still life", "demo"],
  },
  {
    id: `${DEMO_PREFIX}the-kiss`,
    title: "The Kiss (study print)",
    description:
      "Gustav Klimt, 1908. Art Nouveau masterpiece — demo artwork only.",
    price: 198,
    image_url: "/demo-art/the-kiss.jpg",
    tags: ["symbolism", "demo"],
  },
  {
    id: `${DEMO_PREFIX}mona-lisa`,
    title: "Mona Lisa (study print)",
    description:
      "Leonardo da Vinci, c. 1503–1519. World-famous portrait — placeholder product.",
    price: 210,
    image_url: "/demo-art/mona-lisa.jpg",
    tags: ["renaissance", "portrait", "demo"],
  },
  {
    id: `${DEMO_PREFIX}nighthawks`,
    title: "Nighthawks (study print)",
    description:
      "Edward Hopper, 1942. American realist diner scene — demo listing.",
    price: 168,
    image_url: "/demo-art/nighthawks.jpg",
    tags: ["american realism", "demo"],
  },
] as const;

export function isDemoProductId(id: string): boolean {
  return id.startsWith(DEMO_PREFIX);
}

export function getDemoProductById(id: string): DemoCatalogProduct | undefined {
  return DEMO_PRODUCTS.find((p) => p.id === id);
}

export function getDemoProductsForGrid(): DemoCatalogProduct[] {
  return [...DEMO_PRODUCTS];
}

/** Case-insensitive match on title, description, or tags */
export function filterDemoProducts(
  products: readonly DemoCatalogProduct[],
  search: string | undefined
): DemoCatalogProduct[] {
  const term = search?.trim().toLowerCase();
  if (!term) return [...products];
  return products.filter(
    (p) =>
      p.title.toLowerCase().includes(term) ||
      p.description.toLowerCase().includes(term) ||
      p.tags.some((t) => t.toLowerCase().includes(term))
  );
}
