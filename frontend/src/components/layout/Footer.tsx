import Link from "next/link";

const LINKS = {
  Shop: [
    { label: "All Products", href: "/products" },
    { label: "New Arrivals", href: "/products?sort=newest" },
    { label: "Best Sellers", href: "/products?sort=rating" },
    { label: "Deals", href: "/products?sort=price_asc" },
  ],
  Support: [
    { label: "Help Center", href: "#" },
    { label: "Shipping Info", href: "#" },
    { label: "Returns", href: "#" },
    { label: "Contact Us", href: "#" },
  ],
  Legal: [
    { label: "Privacy Policy", href: "#" },
    { label: "Terms of Service", href: "#" },
    { label: "Cookie Policy", href: "#" },
  ],
};

export function Footer() {
  return (
    <footer className="border-t bg-[hsl(222,47%,5%)] text-white/70">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        {/* Main grid */}
        <div className="grid grid-cols-2 gap-8 py-14 sm:grid-cols-2 lg:grid-cols-4">

          {/* Brand */}
          <div className="col-span-2 lg:col-span-1 space-y-4">
            <Link href="/" className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/10">
                <span className="text-sm font-extrabold text-white">E</span>
              </div>
              <span className="text-lg font-extrabold text-white">EcomStore</span>
            </Link>
            <p className="text-sm leading-relaxed">
              Premium products at honest prices. Delivered fast, backed by great support.
            </p>
            <div className="flex gap-3 pt-1">
              {["Twitter", "Instagram", "Facebook"].map((s) => (
                <span
                  key={s}
                  className="flex h-8 w-8 cursor-default items-center justify-center rounded-full bg-white/5 text-[11px] font-bold text-white/40"
                >
                  {s[0]}
                </span>
              ))}
            </div>
          </div>

          {/* Links */}
          {Object.entries(LINKS).map(([section, items]) => (
            <div key={section} className="space-y-4">
              <h3 className="text-[10px] font-bold uppercase tracking-widest text-white/30">
                {section}
              </h3>
              <ul className="space-y-2.5">
                {items.map(({ label, href }) => (
                  <li key={label}>
                    <Link
                      href={href}
                      className="text-sm transition-colors hover:text-white"
                    >
                      {label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className="flex flex-col items-center justify-between gap-3 border-t border-white/10 py-6 sm:flex-row">
          <p className="text-xs text-white/30">
            &copy; {new Date().getFullYear()} EcomStore. All rights reserved.
          </p>
          <div className="flex items-center gap-1.5">
            {["Visa", "MC", "PayPal", "Apple Pay"].map((p) => (
              <span
                key={p}
                className="rounded-md bg-white/5 px-2 py-1 text-[10px] font-semibold text-white/40"
              >
                {p}
              </span>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
