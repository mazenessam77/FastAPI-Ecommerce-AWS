"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { ShoppingCart, Star, Check } from "lucide-react";
import { useCartStore } from "@/stores/cart-store";
import { formatPrice, getDiscountedPrice } from "@/lib/utils";
import type { Product } from "@/lib/types";

interface ProductCardProps {
  product: Product;
}

export function ProductCard({ product }: ProductCardProps) {
  const addItem = useCartStore((s) => s.addItem);
  const [added, setAdded] = useState(false);

  const discountedPrice = getDiscountedPrice(product.price, product.discount_percentage);
  const hasDiscount = product.discount_percentage > 0;
  const isLowStock = product.stock > 0 && product.stock <= 5;

  function handleQuickAdd(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    addItem(product);
    setAdded(true);
    setTimeout(() => setAdded(false), 1600);
  }

  const ratingStars = Math.round(product.rating);

  return (
    <article className="group relative flex flex-col overflow-hidden rounded-2xl bg-white border border-border/60 shadow-card hover:shadow-card-hover hover:-translate-y-1 transition-all duration-300 ease-out">

      {/* ── Image ── */}
      <Link
        href={`/products/${product.id}`}
        className="relative block overflow-hidden bg-muted"
        style={{ aspectRatio: "4 / 5" }}
      >
        <Image
          src={product.thumbnail || "/placeholder.svg"}
          alt={product.title}
          fill
          className="object-cover transition-transform duration-500 ease-out group-hover:scale-[1.04]"
          sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
        />

        {/* Discount badge */}
        {hasDiscount && (
          <span className="absolute left-3 top-3 rounded-full bg-red-500 px-2.5 py-0.5 text-[11px] font-bold text-white shadow">
            -{product.discount_percentage}%
          </span>
        )}

        {/* Low stock badge */}
        {isLowStock && (
          <span className="absolute right-3 top-3 rounded-full bg-amber-500 px-2.5 py-0.5 text-[11px] font-bold text-white shadow">
            Only {product.stock} left
          </span>
        )}

        {/* Quick-add overlay — slides up on hover */}
        <div className="absolute inset-x-0 bottom-0 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-[cubic-bezier(0.32,0.72,0,1)] px-3 pb-3 pt-8 bg-gradient-to-t from-black/60 to-transparent">
          <button
            onClick={handleQuickAdd}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-white py-2.5 text-sm font-semibold text-foreground shadow-lg hover:bg-primary hover:text-primary-foreground transition-colors duration-150"
            aria-label={`Add ${product.title} to cart`}
          >
            {added
              ? <><Check className="h-4 w-4 text-green-500" /> Added to cart</>
              : <><ShoppingCart className="h-4 w-4" /> Quick Add</>
            }
          </button>
        </div>
      </Link>

      {/* ── Details ── */}
      <div className="flex flex-1 flex-col gap-1.5 p-4">
        {/* Brand */}
        <p className="text-[10px] font-semibold uppercase tracking-widest text-muted-foreground/80">
          {product.brand}
        </p>

        {/* Title */}
        <Link href={`/products/${product.id}`}>
          <h3 className="text-sm font-semibold leading-snug line-clamp-2 text-foreground hover:text-primary/70 transition-colors">
            {product.title}
          </h3>
        </Link>

        {/* Stars */}
        <div className="flex items-center gap-1.5">
          <div className="flex">
            {[1, 2, 3, 4, 5].map((i) => (
              <Star
                key={i}
                className={`h-3 w-3 ${i <= ratingStars ? "fill-amber-400 text-amber-400" : "fill-muted text-muted"}`}
              />
            ))}
          </div>
          <span className="text-[11px] text-muted-foreground">{product.rating.toFixed(1)}</span>
        </div>

        {/* Price */}
        <div className="mt-auto flex items-baseline gap-2 pt-2">
          <span className="text-base font-bold tracking-tight">{formatPrice(discountedPrice)}</span>
          {hasDiscount && (
            <span className="text-xs text-muted-foreground line-through">{formatPrice(product.price)}</span>
          )}
        </div>
      </div>
    </article>
  );
}
