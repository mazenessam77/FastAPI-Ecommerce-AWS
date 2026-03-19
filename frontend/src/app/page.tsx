import Link from "next/link";
import { ArrowRight, Truck, ShieldCheck, RotateCcw, Headphones } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProductGrid } from "@/components/product/ProductGrid";
import type { Product, Category, PaginatedResponse } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getFeaturedProducts(): Promise<Product[]> {
  try {
    const res = await fetch(`${API_URL}/products/?limit=8`, { next: { revalidate: 60 } });
    if (!res.ok) return [];
    const json: PaginatedResponse<Product> = await res.json();
    return json.data ?? [];
  } catch {
    return [];
  }
}

async function getCategories(): Promise<Category[]> {
  try {
    const res = await fetch(`${API_URL}/categories/`, { next: { revalidate: 300 } });
    if (!res.ok) return [];
    const json: PaginatedResponse<Category> = await res.json();
    return json.data ?? [];
  } catch {
    return [];
  }
}

const CATEGORY_EMOJI: Record<string, string> = {
  "Electronics": "⚡",
  "Clothing": "👕",
  "Home & Garden": "🌿",
  "Sports & Outdoors": "🏃",
  "Books": "📖",
  "Beauty & Health": "✨",
  "Toys & Games": "🎮",
  "Automotive": "🚗",
};

const TRUST_ITEMS = [
  { icon: Truck, title: "Free Shipping", sub: "On orders over $50" },
  { icon: ShieldCheck, title: "Secure Checkout", sub: "SSL encrypted payments" },
  { icon: RotateCcw, title: "Easy Returns", sub: "30-day return policy" },
  { icon: Headphones, title: "24/7 Support", sub: "We're here to help" },
];

export default async function HomePage() {
  const [products, categories] = await Promise.all([
    getFeaturedProducts(),
    getCategories(),
  ]);

  return (
    <>
      {/* ── Hero ── */}
      <section className="relative overflow-hidden bg-[hsl(222,47%,7%)]">
        {/* Subtle grid pattern */}
        <div
          className="absolute inset-0 opacity-[0.04]"
          style={{
            backgroundImage:
              "linear-gradient(hsl(0,0%,100%) 1px, transparent 1px), linear-gradient(90deg, hsl(0,0%,100%) 1px, transparent 1px)",
            backgroundSize: "60px 60px",
          }}
        />

        <div className="relative mx-auto flex max-w-7xl flex-col items-center px-4 py-28 text-center sm:px-6 sm:py-36 lg:px-8">
          {/* Eyebrow */}
          <span className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-xs font-semibold uppercase tracking-widest text-white/60">
            ✦ Free shipping on orders $50+
          </span>

          {/* Heading */}
          <h1 className="max-w-4xl text-5xl font-extrabold leading-[1.08] tracking-tight text-white sm:text-6xl lg:text-7xl">
            Shop Smarter.{" "}
            <span className="bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
              Live Better.
            </span>
          </h1>

          <p className="mt-6 max-w-lg text-lg leading-relaxed text-white/50">
            Premium products across every category — curated for quality,
            priced for everyone.
          </p>

          {/* CTAs */}
          <div className="mt-10 flex flex-wrap justify-center gap-3">
            <Link href="/products">
              <Button
                size="lg"
                className="gap-2 rounded-full bg-white px-8 text-foreground hover:bg-white/90 shadow-lg shadow-black/20"
              >
                Shop Now <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/products">
              <Button
                size="lg"
                variant="ghost"
                className="gap-2 rounded-full border border-white/15 px-8 text-white hover:bg-white/10"
              >
                Browse Categories
              </Button>
            </Link>
          </div>

          {/* Stats */}
          <div className="mt-16 flex flex-wrap justify-center gap-10 border-t border-white/10 pt-10">
            {[
              { value: "14+", label: "Products" },
              { value: "8", label: "Categories" },
              { value: "100%", label: "Secure" },
              { value: "2-day", label: "Delivery" },
            ].map(({ value, label }) => (
              <div key={label} className="text-center">
                <div className="text-2xl font-bold text-white">{value}</div>
                <div className="mt-0.5 text-xs uppercase tracking-widest text-white/40">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Trust Bar ── */}
      <section className="border-b bg-muted/40">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 divide-x divide-border lg:grid-cols-4">
            {TRUST_ITEMS.map(({ icon: Icon, title, sub }) => (
              <div key={title} className="flex items-center gap-3 px-6 py-4">
                <Icon className="h-5 w-5 shrink-0 text-muted-foreground" />
                <div>
                  <p className="text-sm font-semibold">{title}</p>
                  <p className="text-xs text-muted-foreground">{sub}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Categories ── */}
      {categories.length > 0 && (
        <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="mb-8 flex items-end justify-between">
            <div>
              <p className="mb-1 text-xs font-semibold uppercase tracking-widest text-muted-foreground">
                Explore
              </p>
              <h2 className="text-2xl font-bold">Shop by Category</h2>
            </div>
            <Link
              href="/products"
              className="flex items-center gap-1 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
            >
              View all <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-8">
            {categories.slice(0, 8).map((category) => (
              <Link
                key={category.id}
                href={`/products?category=${category.id}`}
                className="group flex flex-col items-center gap-2 rounded-2xl border bg-card p-4 text-center transition-all duration-200 hover:border-primary/30 hover:bg-primary hover:shadow-md"
              >
                <span className="text-2xl transition-transform duration-200 group-hover:scale-110">
                  {CATEGORY_EMOJI[category.name] ?? "🛍️"}
                </span>
                <span className="text-xs font-semibold leading-tight text-foreground group-hover:text-primary-foreground transition-colors">
                  {category.name}
                </span>
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* ── Featured Products ── */}
      <section className="mx-auto max-w-7xl px-4 pb-20 sm:px-6 lg:px-8">
        <div className="mb-8 flex items-end justify-between">
          <div>
            <p className="mb-1 text-xs font-semibold uppercase tracking-widest text-muted-foreground">
              Handpicked
            </p>
            <h2 className="text-2xl font-bold">Featured Products</h2>
          </div>
          <Link
            href="/products"
            className="flex items-center gap-1 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
          >
            View all <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>

        {products.length > 0 ? (
          <ProductGrid products={products} />
        ) : (
          <div className="rounded-2xl border border-dashed py-16 text-center text-muted-foreground">
            Products will appear here once your API is connected.
          </div>
        )}
      </section>

      {/* ── CTA Banner ── */}
      <section className="mx-4 mb-16 overflow-hidden rounded-3xl bg-[hsl(222,47%,7%)] sm:mx-6 lg:mx-8">
        <div className="relative flex flex-col items-center px-6 py-16 text-center">
          <div
            className="absolute inset-0 opacity-[0.04]"
            style={{
              backgroundImage:
                "radial-gradient(circle at 50% 50%, hsl(0,0%,100%) 1px, transparent 1px)",
              backgroundSize: "28px 28px",
            }}
          />
          <h2 className="relative text-3xl font-extrabold text-white sm:text-4xl">
            Ready to find your next favourite thing?
          </h2>
          <p className="relative mt-3 max-w-md text-white/50">
            Thousands of products, competitive prices, and lightning-fast delivery.
          </p>
          <Link href="/products" className="relative mt-8">
            <Button
              size="lg"
              className="gap-2 rounded-full bg-white px-10 text-foreground hover:bg-white/90 shadow-lg"
            >
              Start Shopping <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>
    </>
  );
}
