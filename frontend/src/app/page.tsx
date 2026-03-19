import Link from "next/link";
import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProductGrid } from "@/components/product/ProductGrid";
import type { Product, Category, PaginatedResponse } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * SSG with ISR — revalidates every 60 seconds for fresh data
 * while serving cached pages for blazing-fast performance.
 */
async function getFeaturedProducts(): Promise<Product[]> {
  try {
    const res = await fetch(`${API_URL}/products/?limit=8`, {
      next: { revalidate: 60 },
    });
    if (!res.ok) return [];
    const json: PaginatedResponse<Product> = await res.json();
    return json.data ?? [];
  } catch {
    return [];
  }
}

async function getCategories(): Promise<Category[]> {
  try {
    const res = await fetch(`${API_URL}/categories/`, {
      next: { revalidate: 300 },
    });
    if (!res.ok) return [];
    const json: PaginatedResponse<Category> = await res.json();
    return json.data ?? [];
  } catch {
    return [];
  }
}

export default async function HomePage() {
  const [products, categories] = await Promise.all([
    getFeaturedProducts(),
    getCategories(),
  ]);

  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-muted/50 to-muted">
        <div className="mx-auto flex max-w-7xl flex-col items-center px-4 py-24 text-center sm:px-6 sm:py-32 lg:px-8">
          <h1 className="max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Discover Products <br />
            <span className="text-muted-foreground">That Define You</span>
          </h1>
          <p className="mt-6 max-w-xl text-lg text-muted-foreground">
            Curated collections of premium products at prices that make sense.
            Quality meets affordability.
          </p>
          <div className="mt-10 flex gap-4">
            <Link href="/products">
              <Button size="lg" className="gap-2">
                Shop Now <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href="/products">
              <Button size="lg" variant="outline">
                Browse Categories
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Categories */}
      {categories.length > 0 && (
        <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold tracking-tight">
              Shop by Category
            </h2>
            <Link
              href="/products"
              className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              View all
            </Link>
          </div>
          <div className="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
            {categories.slice(0, 8).map((category) => (
              <Link
                key={category.id}
                href={`/products?category=${category.id}`}
                className="group flex flex-col items-center rounded-xl border bg-card p-6 text-center transition-all hover:shadow-md hover:-translate-y-0.5"
              >
                <div className="flex h-14 w-14 items-center justify-center rounded-full bg-muted transition-colors group-hover:bg-primary/10">
                  <span className="text-xl font-bold text-muted-foreground group-hover:text-primary">
                    {category.name.charAt(0)}
                  </span>
                </div>
                <h3 className="mt-3 text-sm font-medium">{category.name}</h3>
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Featured Products */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold tracking-tight">
            Featured Products
          </h2>
          <Link
            href="/products"
            className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            View all
          </Link>
        </div>
        <div className="mt-8">
          {products.length > 0 ? (
            <ProductGrid products={products} />
          ) : (
            <div className="rounded-xl border border-dashed p-12 text-center">
              <p className="text-muted-foreground">
                No products available yet. Connect your API to see products here.
              </p>
            </div>
          )}
        </div>
      </section>

      {/* CTA Banner */}
      <section className="bg-primary text-primary-foreground">
        <div className="mx-auto flex max-w-7xl flex-col items-center px-4 py-16 text-center sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold">Ready to start shopping?</h2>
          <p className="mt-3 max-w-md text-primary-foreground/80">
            Join thousands of happy customers and find exactly what you need.
          </p>
          <Link href="/products" className="mt-8">
            <Button
              size="lg"
              variant="secondary"
              className="gap-2"
            >
              Explore Products <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </section>
    </>
  );
}
