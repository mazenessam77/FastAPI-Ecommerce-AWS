"use client";

import Image from "next/image";
import { X, Minus, Plus, ShoppingBag } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { useCartStore } from "@/stores/cart-store";
import { formatPrice, getDiscountedPrice } from "@/lib/utils";

export function CartDrawer() {
  const { items, isOpen, closeCart, removeItem, updateQuantity, totalPrice, clearCart } =
    useCartStore();

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm animate-fade-in"
        onClick={closeCart}
        aria-hidden="true"
      />

      {/* Drawer */}
      <aside
        className="fixed right-0 top-0 z-50 flex h-full w-full max-w-md flex-col bg-background shadow-2xl animate-slide-in-right"
        role="dialog"
        aria-label="Shopping cart"
      >
        {/* Header */}
        <div className="flex items-center justify-between border-b px-6 py-4">
          <div className="flex items-center space-x-2">
            <ShoppingBag className="h-5 w-5" />
            <h2 className="text-lg font-semibold">
              Cart ({items.length})
            </h2>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={closeCart}
            aria-label="Close cart"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Items */}
        <div className="flex-1 overflow-y-auto px-6 py-4 hide-scrollbar">
          {items.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center text-center">
              <ShoppingBag className="mb-4 h-16 w-16 text-muted-foreground/30" />
              <p className="text-lg font-medium">Your cart is empty</p>
              <p className="mt-1 text-sm text-muted-foreground">
                Add some products to get started
              </p>
              <Button className="mt-6" onClick={closeCart}>
                Continue Shopping
              </Button>
            </div>
          ) : (
            <ul className="space-y-4">
              {items.map((item) => {
                const discountedPrice = getDiscountedPrice(
                  item.product.price,
                  item.product.discount_percentage
                );
                return (
                  <li
                    key={item.product.id}
                    className="flex gap-4 rounded-lg border p-3"
                  >
                    <div className="relative h-20 w-20 flex-shrink-0 overflow-hidden rounded-md bg-muted">
                      <Image
                        src={item.product.thumbnail || "/placeholder.svg"}
                        alt={item.product.title}
                        fill
                        className="object-cover"
                        sizes="80px"
                      />
                    </div>
                    <div className="flex flex-1 flex-col justify-between">
                      <div>
                        <h3 className="text-sm font-medium line-clamp-1">
                          {item.product.title}
                        </h3>
                        <p className="mt-0.5 text-sm font-semibold">
                          {formatPrice(discountedPrice)}
                        </p>
                      </div>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-1">
                          <Button
                            variant="outline"
                            size="icon"
                            className="h-7 w-7"
                            onClick={() =>
                              updateQuantity(
                                item.product.id,
                                item.quantity - 1
                              )
                            }
                            aria-label="Decrease quantity"
                          >
                            <Minus className="h-3 w-3" />
                          </Button>
                          <span className="w-8 text-center text-sm">
                            {item.quantity}
                          </span>
                          <Button
                            variant="outline"
                            size="icon"
                            className="h-7 w-7"
                            onClick={() =>
                              updateQuantity(
                                item.product.id,
                                item.quantity + 1
                              )
                            }
                            aria-label="Increase quantity"
                          >
                            <Plus className="h-3 w-3" />
                          </Button>
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-7 w-7 text-muted-foreground hover:text-destructive"
                          onClick={() => removeItem(item.product.id)}
                          aria-label="Remove item"
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </div>

        {/* Footer */}
        {items.length > 0 && (
          <div className="border-t px-6 py-4 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Subtotal</span>
              <span className="text-lg font-semibold">
                {formatPrice(totalPrice())}
              </span>
            </div>
            <Separator />
            <Button className="w-full" size="lg">
              Checkout
            </Button>
            <Button
              variant="outline"
              className="w-full"
              size="sm"
              onClick={clearCart}
            >
              Clear Cart
            </Button>
          </div>
        )}
      </aside>
    </>
  );
}
