import type { Metadata } from "next";
import { CartProvider } from "@/contexts/CartContext";
import { SidebarLayout } from "@/components/templates/SidebarLayout";
import "./globals.css";

export const metadata: Metadata = {
  title: "IcedMangoes | Artist Storefront",
  description: "Clean, simple artist storefront. Deploy to Vercel with Supabase.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">
        <CartProvider>
          <SidebarLayout>{children}</SidebarLayout>
        </CartProvider>
      </body>
    </html>
  );
}
