import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Star, Truck, Shield, RotateCcw } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { ProductGallery } from "@/components/product/ProductGallery";
import { AddToCartButton } from "./AddToCartButton";
import { formatPrice, getDiscountedPrice } from "@/lib/utils";
import type { Product, ApiResponse } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface PageProps {
  params: Promise<{ id: string }>;
}

/**
 * SSR — Server-side rendered for SEO indexability.
 * Product data is fetched on every request (no cache).
 */
async function getProduct(id: string): Promise<Product | null> {
  try {
    const res = await fetch(`${API_URL}/products/${id}`, {
      cache: "no-store",
    });
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

  const discountedPrice = getDiscountedPrice(
    product.price,
    product.discount_percentage
  );

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="grid gap-10 lg:grid-cols-2">
        {/* Gallery */}
        <ProductGallery images={product.images} title={product.title} />

        {/* Details */}
        <div className="space-y-6">
          {/* Brand + Title */}
          <div>
            <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
              {product.brand}
            </p>
            <h1 className="mt-1 text-3xl font-bold tracking-tight">
              {product.title}
            </h1>
          </div>

          {/* Rating + Stock */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
              <span className="text-sm font-medium">
                {product.rating.toFixed(1)}
              </span>
            </div>
            <Separator orientation="vertical" className="h-4" />
            {product.stock > 0 ? (
              <Badge variant="secondary">In Stock ({product.stock})</Badge>
            ) : (
              <Badge variant="destructive">Out of Stock</Badge>
            )}
          </div>

          {/* Price */}
          <div className="flex items-baseline gap-3">
            <span className="text-3xl font-bold">
              {formatPrice(discountedPrice)}
            </span>
            {product.discount_percentage > 0 && (
              <>
                <span className="text-xl text-muted-foreground line-through">
                  {formatPrice(product.price)}
                </span>
                <Badge variant="destructive">
                  -{product.discount_percentage}%
                </Badge>
              </>
            )}
          </div>

          <Separator />

          {/* Description */}
          <div>
            <h2 className="text-sm font-semibold uppercase tracking-wider">
              Description
            </h2>
            <p className="mt-2 leading-relaxed text-muted-foreground">
              {product.description}
            </p>
          </div>

          <Separator />

          {/* Variants + Add to Cart (Client Component) */}
          <AddToCartButton product={product} />

          <Separator />

          {/* Trust badges */}
          <div className="grid grid-cols-3 gap-4">
            {[
              { icon: Truck, label: "Free Shipping", sub: "Orders $50+" },
              { icon: Shield, label: "Secure Payment", sub: "SSL encrypted" },
              { icon: RotateCcw, label: "Easy Returns", sub: "30-day policy" },
            ].map(({ icon: Icon, label, sub }) => (
              <div
                key={label}
                className="flex flex-col items-center rounded-lg border p-3 text-center"
              >
                <Icon className="h-5 w-5 text-muted-foreground" />
                <span className="mt-1.5 text-xs font-medium">{label}</span>
                <span className="text-[10px] text-muted-foreground">{sub}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
