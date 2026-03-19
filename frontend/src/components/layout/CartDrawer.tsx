"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { X, Minus, Plus, ShoppingBag, CheckCircle, ArrowLeft, Package } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { useCartStore } from "@/stores/cart-store";
import { useAuthStore } from "@/stores/auth-store";
import { formatPrice, getDiscountedPrice } from "@/lib/utils";
import { api } from "@/lib/api";

type Step = "cart" | "confirm" | "success";

function deliveryDate() {
  const d = new Date();
  d.setDate(d.getDate() + 2);
  return d.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
}

export function CartDrawer() {
  const { items, isOpen, closeCart, removeItem, updateQuantity, totalPrice, clearCart } =
    useCartStore();
  const { token } = useAuthStore();
  const router = useRouter();

  const [step, setStep] = useState<Step>("cart");
  const [isPlacing, setIsPlacing] = useState(false);
  const [orderId, setOrderId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  function handleClose() {
    closeCart();
    // reset to cart view after drawer closes (small delay so animation isn't jarring)
    setTimeout(() => { setStep("cart"); setError(null); setOrderId(null); }, 300);
  }

  async function placeOrder() {
    if (!token) {
      handleClose();
      router.push("/login");
      return;
    }
    setIsPlacing(true);
    setError(null);
    try {
      const res = await api.checkout(
        items.map((i) => ({ product_id: i.product.id, quantity: i.quantity }))
      );
      setOrderId(res.data.id);
      clearCart();
      setStep("success");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Checkout failed. Please try again.");
    } finally {
      setIsPlacing(false);
    }
  }

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm animate-fade-in"
        onClick={step === "success" ? undefined : handleClose}
        aria-hidden="true"
      />

      {/* Drawer */}
      <aside
        className="fixed right-0 top-0 z-50 flex h-full w-full max-w-md flex-col bg-background shadow-2xl animate-slide-in-right"
        role="dialog"
        aria-label="Shopping cart"
      >
        {/* ── STEP: SUCCESS ────────────────────────────────────────── */}
        {step === "success" && (
          <div className="flex flex-1 flex-col items-center justify-center px-8 text-center space-y-4">
            <CheckCircle className="h-20 w-20 text-green-500" />
            <h2 className="text-2xl font-bold">Order Confirmed!</h2>
            <p className="text-muted-foreground">
              Thank you for your purchase. Your order{" "}
              <span className="font-semibold text-foreground">#{orderId}</span> has been placed
              successfully.
            </p>
            <div className="w-full rounded-lg border bg-muted/40 px-5 py-4 text-sm space-y-1">
              <div className="flex items-center gap-2 justify-center font-medium">
                <Package className="h-4 w-4" />
                Estimated Delivery
              </div>
              <p className="text-base font-semibold text-foreground">{deliveryDate()}</p>
              <p className="text-muted-foreground text-xs">Delivery within 2 business days</p>
            </div>
            <Button
              className="w-full mt-2"
              onClick={() => { handleClose(); router.push("/orders"); }}
            >
              View My Orders
            </Button>
            <Button variant="outline" className="w-full" onClick={handleClose}>
              Continue Shopping
            </Button>
          </div>
        )}

        {/* ── STEP: CONFIRM ────────────────────────────────────────── */}
        {step === "confirm" && (
          <>
            <div className="flex items-center gap-2 border-b px-6 py-4">
              <Button variant="ghost" size="icon" onClick={() => { setStep("cart"); setError(null); }}>
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <h2 className="text-lg font-semibold">Confirm Order</h2>
            </div>

            <div className="flex-1 overflow-y-auto px-6 py-4 space-y-3 hide-scrollbar">
              <p className="text-sm text-muted-foreground">
                Please review your order before placing it.
              </p>
              <ul className="divide-y">
                {items.map((item) => {
                  const price = getDiscountedPrice(item.product.price, item.product.discount_percentage);
                  return (
                    <li key={item.product.id} className="py-3 flex items-center gap-3">
                      <div className="relative h-14 w-14 flex-shrink-0 overflow-hidden rounded-md bg-muted">
                        <Image
                          src={item.product.thumbnail || "/placeholder.svg"}
                          alt={item.product.title}
                          fill
                          className="object-cover"
                          sizes="56px"
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium line-clamp-1">{item.product.title}</p>
                        <p className="text-xs text-muted-foreground">Qty: {item.quantity}</p>
                      </div>
                      <span className="text-sm font-semibold shrink-0">
                        {formatPrice(price * item.quantity)}
                      </span>
                    </li>
                  );
                })}
              </ul>

              <Separator />
              <div className="flex justify-between font-semibold text-base">
                <span>Total</span>
                <span>{formatPrice(totalPrice())}</span>
              </div>

              <div className="rounded-lg border bg-muted/40 px-4 py-3 text-sm text-muted-foreground flex gap-2 items-center">
                <Package className="h-4 w-4 shrink-0" />
                <span>Estimated delivery by <strong className="text-foreground">{deliveryDate()}</strong></span>
              </div>
            </div>

            <div className="border-t px-6 py-4 space-y-3">
              {error && <p className="text-sm text-destructive">{error}</p>}
              <Button className="w-full" size="lg" onClick={placeOrder} disabled={isPlacing}>
                {isPlacing ? "Placing Order…" : "Place Order"}
              </Button>
              <Button variant="outline" className="w-full" onClick={() => { setStep("cart"); setError(null); }}>
                Back to Cart
              </Button>
            </div>
          </>
        )}

        {/* ── STEP: CART ───────────────────────────────────────────── */}
        {step === "cart" && (
          <>
            <div className="flex items-center justify-between border-b px-6 py-4">
              <div className="flex items-center space-x-2">
                <ShoppingBag className="h-5 w-5" />
                <h2 className="text-lg font-semibold">Cart ({items.length})</h2>
              </div>
              <Button variant="ghost" size="icon" onClick={handleClose} aria-label="Close cart">
                <X className="h-5 w-5" />
              </Button>
            </div>

            <div className="flex-1 overflow-y-auto px-6 py-4 hide-scrollbar">
              {items.length === 0 ? (
                <div className="flex h-full flex-col items-center justify-center text-center">
                  <ShoppingBag className="mb-4 h-16 w-16 text-muted-foreground/30" />
                  <p className="text-lg font-medium">Your cart is empty</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Add some products to get started
                  </p>
                  <Button className="mt-6" onClick={handleClose}>
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
                      <li key={item.product.id} className="flex gap-4 rounded-lg border p-3">
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
                            <h3 className="text-sm font-medium line-clamp-1">{item.product.title}</h3>
                            <p className="mt-0.5 text-sm font-semibold">{formatPrice(discountedPrice)}</p>
                          </div>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-1">
                              <Button
                                variant="outline" size="icon" className="h-7 w-7"
                                onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                                aria-label="Decrease quantity"
                              >
                                <Minus className="h-3 w-3" />
                              </Button>
                              <span className="w-8 text-center text-sm">{item.quantity}</span>
                              <Button
                                variant="outline" size="icon" className="h-7 w-7"
                                onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                                aria-label="Increase quantity"
                              >
                                <Plus className="h-3 w-3" />
                              </Button>
                            </div>
                            <Button
                              variant="ghost" size="icon"
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

            {items.length > 0 && (
              <div className="border-t px-6 py-4 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">Subtotal</span>
                  <span className="text-lg font-semibold">{formatPrice(totalPrice())}</span>
                </div>
                <Separator />
                <Button
                  className="w-full" size="lg"
                  onClick={() => {
                    if (!token) { handleClose(); router.push("/login"); return; }
                    setStep("confirm");
                  }}
                >
                  Checkout
                </Button>
                <Button variant="outline" className="w-full" size="sm" onClick={clearCart}>
                  Clear Cart
                </Button>
              </div>
            )}
          </>
        )}
      </aside>
    </>
  );
}
