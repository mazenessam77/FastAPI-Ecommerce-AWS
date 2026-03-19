"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ShoppingBag, Package } from "lucide-react";
import { useAuthStore } from "@/stores/auth-store";
import { api } from "@/lib/api";
import type { Order } from "@/lib/types";
import { formatPrice } from "@/lib/utils";

const STATUS_COLORS: Record<string, string> = {
  confirmed: "bg-blue-100 text-blue-700",
  pending: "bg-yellow-100 text-yellow-700",
  shipped: "bg-purple-100 text-purple-700",
  delivered: "bg-green-100 text-green-700",
  cancelled: "bg-red-100 text-red-700",
};

export default function OrdersPage() {
  const { token } = useAuthStore();
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      router.push("/login");
      return;
    }
    api
      .getOrders()
      .then((res) => setOrders(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token, router]);

  if (loading) {
    return (
      <main className="container mx-auto px-4 py-16 text-center">
        <p className="text-muted-foreground">Loading orders…</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="container mx-auto px-4 py-16 text-center">
        <p className="text-destructive">{error}</p>
      </main>
    );
  }

  return (
    <main className="container mx-auto px-4 py-10 max-w-3xl">
      <h1 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <Package className="h-6 w-6" />
        My Orders
      </h1>

      {orders.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <ShoppingBag className="h-16 w-16 text-muted-foreground/30 mb-4" />
          <p className="text-lg font-medium">No orders yet</p>
          <p className="text-sm text-muted-foreground mt-1">
            Add products to your cart and place an order.
          </p>
          <button
            className="mt-6 underline text-sm text-primary"
            onClick={() => router.push("/")}
          >
            Browse Products
          </button>
        </div>
      ) : (
        <ul className="space-y-4">
          {orders.map((order) => (
            <li key={order.id} className="border rounded-lg p-5 space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-semibold">Order #{order.id}</span>
                  <span className="ml-3 text-sm text-muted-foreground">
                    {new Date(order.created_at).toLocaleDateString()}
                  </span>
                </div>
                <span
                  className={`text-xs font-medium px-2 py-1 rounded-full capitalize ${STATUS_COLORS[order.status] ?? "bg-gray-100 text-gray-700"}`}
                >
                  {order.status}
                </span>
              </div>

              <ul className="divide-y text-sm">
                {order.order_items.map((item) => (
                  <li key={item.id} className="py-1.5 flex justify-between">
                    <span>
                      Product #{item.product_id} × {item.quantity}
                    </span>
                    <span className="font-medium">{formatPrice(item.subtotal)}</span>
                  </li>
                ))}
              </ul>

              <div className="flex justify-end font-semibold">
                Total: {formatPrice(order.total_amount)}
              </div>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
