"use client";

import Image from "next/image";
import Link from "next/link";
import { ShoppingCart, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useCartStore } from "@/stores/cart-store";
import { formatPrice, getDiscountedPrice } from "@/lib/utils";
import type { Product } from "@/lib/types";

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  const addItem = useCartStore((s) => s.addItem);
  const discountedPrice = getDiscountedPrice(
    product.price,
    product.discount_percentage
  );

  return (
    <article className="group relative flex flex-col overflow-hidden rounded-xl border bg-card transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5">
      {/* Image */}
      <Link
        href={`/products/${product.id}`}
        className="relative aspect-square overflow-hidden bg-muted"
      >
        <Image
          src={product.thumbnail || "/placeholder.svg"}
          alt={product.title}
          fill
          className="object-cover transition-transform duration-500 group-hover:scale-105"
          sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
        />
        {product.discount_percentage > 0 && (
          <Badge className="absolute left-3 top-3" variant="destructive">
            -{product.discount_percentage}%
          </Badge>
        )}
      </Link>

      {/* Details */}
      <div className="flex flex-1 flex-col p-4">
        <p className="text-xs text-muted-foreground uppercase tracking-wider">
          {product.brand}
        </p>
        <Link href={`/products/${product.id}`}>
          <h3 className="mt-1 text-sm font-medium line-clamp-2 transition-colors hover:text-primary/80">
            {product.title}
          </h3>
        </Link>

        {/* Rating */}
        <div className="mt-2 flex items-center space-x-1">
          <Star className="h-3.5 w-3.5 fill-yellow-400 text-yellow-400" />
          <span className="text-xs text-muted-foreground">
            {product.rating.toFixed(1)}
          </span>
        </div>

        {/* Price */}
        <div className="mt-auto flex items-center justify-between pt-3">
          <div className="flex items-baseline space-x-2">
            <span className="text-lg font-bold">
              {formatPrice(discountedPrice)}
            </span>
            {product.discount_percentage > 0 && (
              <span className="text-sm text-muted-foreground line-through">
                {formatPrice(product.price)}
              </span>
            )}
          </div>
          <Button
            size="icon"
            variant="secondary"
            className="h-9 w-9 rounded-full"
            onClick={(e) => {
              e.preventDefault();
              addItem(product);
            }}
            aria-label={`Add ${product.title} to cart`}
          >
            <ShoppingCart className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </article>
  );
}
