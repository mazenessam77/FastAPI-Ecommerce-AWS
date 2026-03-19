import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { Star, Truck, ShieldCheck, RotateCcw, ChevronRight } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { ProductGallery } from "@/components/product/ProductGallery";
import { AddToCartButton } from "./AddToCartButton";
import { formatPrice, getDiscountedPrice } from "@/lib/utils";
import type { Product, ApiResponse } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface PageProps {
  params: Promise<{ id: string }>;
}

async function getProduct(id: string): Promise<Product | null> {
  try {
    const res = await fetch(`${API_URL}/products/${id}`, { cache: "no-store" });
    if (!res.ok) return null;
    const json: ApiResponse<Product> = await res.json();
    return json.data ?? null;
  } catch {
    return null;
  }
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { id } = await params;
  const product = await getProduct(id);
  if (!product) return { title: "Product Not Found" };
  return {
    title: product.title,
    description: product.description,
    openGraph: {
      title: product.title,
      description: product.description,
      images: product.thumbnail ? [product.thumbnail] : [],
    },
  };
}

export default async function ProductDetailPage({ params }: PageProps) {
  const { id } = await params;
  const product = await getProduct(id);
  if (!product) notFound();

  const discountedPrice = getDiscountedPrice(product.price, product.discount_percentage);
  const hasDiscount = product.discount_percentage > 0;
  const savings = hasDiscount ? product.price - discountedPrice : 0;
  const ratingStars = Math.round(product.rating);
  const inStock = product.stock > 0;

  const TRUST = [
    { icon: Truck, label: "Free Shipping", sub: "Orders over $50" },
    { icon: ShieldCheck, label: "Secure Payment", sub: "SSL encrypted" },
    { icon: RotateCcw, label: "30-Day Returns", sub: "Hassle-free policy" },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">

      {/* Breadcrumb */}
      <nav className="mb-6 flex items-center gap-1.5 text-xs text-muted-foreground">
        <Link href="/" className="hover:text-foreground transition-colors">Home</Link>
        <ChevronRight className="h-3 w-3 shrink-0" />
        <Link href="/products" className="hover:text-foreground transition-colors">Products</Link>
        <ChevronRight className="h-3 w-3 shrink-0" />
        <span className="truncate max-w-[200px] text-foreground font-medium">{product.title}</span>
      </nav>

      <div className="grid gap-12 lg:grid-cols-2">

        {/* Gallery */}
        <ProductGallery images={product.images} title={product.title} />

        {/* Details */}
        <div className="space-y-6">

          {/* Brand + Title */}
          <div>
            <p className="mb-1 text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
              {product.brand}
            </p>
            <h1 className="text-3xl font-extrabold tracking-tight leading-tight">
              {product.title}
            </h1>
          </div>

          {/* Rating + Stock */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-1.5">
              <div className="flex">
                {[1, 2, 3, 4, 5].map((i) => (
                  <Star
                    key={i}
                    className={`h-4 w-4 ${i <= ratingStars ? "fill-amber-400 text-amber-400" : "fill-muted text-muted"}`}
                  />
                ))}
              </div>
              <span className="text-sm font-semibold">{product.rating.toFixed(1)}</span>
            </div>

            <Separator orientation="vertical" className="h-4" />

            <span
              className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                inStock
                  ? "bg-green-100 text-green-700"
                  : "bg-red-100 text-red-700"
              }`}
            >
              <span className={`h-1.5 w-1.5 rounded-full ${inStock ? "bg-green-500" : "bg-red-500"}`} />
              {inStock ? `In Stock · ${product.stock} available` : "Out of Stock"}
            </span>
          </div>

          {/* Price */}
          <div className="rounded-2xl border bg-muted/30 p-4">
            <div className="flex items-baseline gap-3">
              <span className="text-4xl font-extrabold tracking-tight">
                {formatPrice(discountedPrice)}
              </span>
              {hasDiscount && (
                <span className="text-lg text-muted-foreground line-through">
                  {formatPrice(product.price)}
                </span>
              )}
            </div>
            {hasDiscount && (
              <p className="mt-1 text-sm text-green-600 font-semibold">
                You save {formatPrice(savings)} ({product.discount_percentage}% off)
              </p>
            )}
          </div>

          {/* Description */}
          <div>
            <h2 className="mb-2 text-sm font-bold uppercase tracking-widest text-muted-foreground">
              About this product
            </h2>
            <p className="leading-relaxed text-muted-foreground text-sm">
              {product.description}
            </p>
          </div>

          <Separator />

          {/* Add to cart */}
          <AddToCartButton product={product} />

          <Separator />

          {/* Trust badges */}
          <div className="grid grid-cols-3 gap-3">
            {TRUST.map(({ icon: Icon, label, sub }) => (
              <div
                key={label}
                className="flex flex-col items-center gap-2 rounded-xl border bg-card p-3 text-center"
              >
                <Icon className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-[11px] font-semibold leading-tight">{label}</p>
                  <p className="text-[10px] text-muted-foreground">{sub}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
