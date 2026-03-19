import Link from "next/link";
import { Separator } from "@/components/ui/separator";

export function Footer() {
  return (
    <footer className="border-t bg-background">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
                <span className="text-sm font-bold text-primary-foreground">
                  E
                </span>
              </div>
              <span className="text-xl font-bold">EcomStore</span>
            </div>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Premium products at unbeatable prices. Quality you can trust,
              delivered to your door.
            </p>
          </div>

          {/* Shop */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold uppercase tracking-wider">
              Shop
            </h3>
            <ul className="space-y-2">
              {["All Products", "Categories", "New Arrivals", "Best Sellers"].map(
                (item) => (
                  <li key={item}>
                    <Link
                      href="/products"
                      className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                    >
                      {item}
                    </Link>
                  </li>
                )
              )}
            </ul>
          </div>

          {/* Support */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold uppercase tracking-wider">
              Support
            </h3>
            <ul className="space-y-2">
              {["Help Center", "Shipping Info", "Returns", "Contact Us"].map(
                (item) => (
                  <li key={item}>
                    <span className="text-sm text-muted-foreground cursor-default">
                      {item}
                    </span>
                  </li>
                )
              )}
            </ul>
          </div>

          {/* Legal */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold uppercase tracking-wider">
              Legal
            </h3>
            <ul className="space-y-2">
              {["Privacy Policy", "Terms of Service", "Cookie Policy"].map(
                (item) => (
                  <li key={item}>
                    <span className="text-sm text-muted-foreground cursor-default">
                      {item}
                    </span>
                  </li>
                )
              )}
            </ul>
          </div>
        </div>

        <Separator className="my-8" />

        <p className="text-center text-sm text-muted-foreground">
          &copy; {new Date().getFullYear()} EcomStore. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
