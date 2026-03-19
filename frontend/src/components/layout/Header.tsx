"use client";

import Link from "next/link";
import { useState } from "react";
import {
  ShoppingCart,
  Search,
  Menu,
  X,
  User,
  LogOut,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useCartStore } from "@/stores/cart-store";
import { useAuthStore } from "@/stores/auth-store";

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const totalItems = useCartStore((s) => s.totalItems());
  const openCart = useCartStore((s) => s.openCart);
  const { isAuthenticated, user, logout, _hasHydrated } = useAuthStore();

  // Don't render auth-sensitive UI until Zustand has read from localStorage.
  // Prevents the "flash of logged-out state" on page load / navigation.
  const authed = _hasHydrated && isAuthenticated;

  const navLinks = [
    { href: "/", label: "Home" },
    { href: "/products", label: "Shop" },
    ...(authed ? [{ href: "/orders", label: "Orders" }] : []),
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link href="/" className="flex items-center space-x-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <span className="text-sm font-bold text-primary-foreground">E</span>
          </div>
          <span className="hidden text-xl font-bold tracking-tight sm:block">
            EcomStore
          </span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden items-center space-x-8 md:flex">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Search + Actions */}
        <div className="flex items-center space-x-2">
          {/* Search Bar — Desktop */}
          <div className="hidden w-64 md:block">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search products..."
                className="pl-9 h-9"
              />
            </div>
          </div>

          {/* Search Toggle — Mobile */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setSearchOpen(!searchOpen)}
            aria-label="Toggle search"
          >
            <Search className="h-5 w-5" />
          </Button>

          {/* Auth — hidden until store has hydrated from localStorage */}
          {!_hasHydrated ? (
            <div className="hidden sm:block w-8 h-8" /> /* placeholder keeps layout stable */
          ) : authed ? (
            <div className="hidden items-center space-x-2 sm:flex">
              <span className="text-sm text-muted-foreground">
                {user?.full_name || user?.username}
              </span>
              <Button variant="ghost" size="icon" onClick={logout} aria-label="Logout">
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          ) : (
            <Link href="/login" className="hidden sm:block">
              <Button variant="ghost" size="icon" aria-label="Login">
                <User className="h-5 w-5" />
              </Button>
            </Link>
          )}

          {/* Cart */}
          <Button
            variant="ghost"
            size="icon"
            className="relative"
            onClick={openCart}
            aria-label="Open cart"
          >
            <ShoppingCart className="h-5 w-5" />
            {totalItems > 0 && (
              <Badge className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center p-0 text-[10px]">
                {totalItems}
              </Badge>
            )}
          </Button>

          {/* Mobile Menu Toggle */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
        </div>
      </div>

      {/* Mobile Search */}
      {searchOpen && (
        <div className="border-t px-4 py-3 md:hidden animate-fade-in">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input placeholder="Search products..." className="pl-9" autoFocus />
          </div>
        </div>
      )}

      {/* Mobile Nav */}
      {mobileMenuOpen && (
        <nav className="border-t px-4 py-4 md:hidden animate-fade-in">
          <div className="flex flex-col space-y-3">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                onClick={() => setMobileMenuOpen(false)}
              >
                {link.label}
              </Link>
            ))}
            {!authed && _hasHydrated && (
              <Link
                href="/login"
                className="text-sm font-medium text-muted-foreground"
                onClick={() => setMobileMenuOpen(false)}
              >
                Login
              </Link>
            )}
          </div>
        </nav>
      )}
    </header>
  );
}
