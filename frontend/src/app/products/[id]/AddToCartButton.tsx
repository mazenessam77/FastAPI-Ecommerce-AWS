"use client";

import { useState } from "react";
import { ShoppingCart, Minus, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProductVariants } from "@/components/product/ProductVariants";
import { useCartStore } from "@/stores/cart-store";
import type { Product } from "@/lib/types";

interface AddToCartButtonProps {
  product: Product;
}

export function AddToCartButton({ product }: AddToCartButtonProps) {
  const [quantity, setQuantity] = useState(1);
  const addItem = useCartStore((s) => s.addItem);

  return (
    <div className="space-y-6">
      <ProductVariants />

      {/* Quantity + Add to Cart */}
      <div className="flex items-center gap-4">
        <div className="flex items-center rounded-md border">
          <Button
            variant="ghost"
            size="icon"
            className="h-10 w-10 rounded-r-none"
            onClick={() => setQuantity(Math.max(1, quantity - 1))}
            aria-label="Decrease quantity"
          >
            <Minus className="h-4 w-4" />
          </Button>
          <span className="flex h-10 w-12 items-center justify-center text-sm font-medium">
            {quantity}
          </span>
          <Button
            variant="ghost"
            size="icon"
            className="h-10 w-10 rounded-l-none"
            onClick={() => setQuantity(quantity + 1)}
            aria-label="Increase quantity"
          >
            <Plus className="h-4 w-4" />
          </Button>
        </div>

        <Button
          size="lg"
          className="flex-1 gap-2"
          disabled={product.stock === 0}
          onClick={() => addItem(product, quantity)}
        >
          <ShoppingCart className="h-4 w-4" />
          Add to Cart
        </Button>
      </div>
    </div>
  );
}
