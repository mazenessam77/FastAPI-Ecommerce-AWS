"use client";

import { useState } from "react";
import { SlidersHorizontal, Search, X, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProductGrid } from "@/components/product/ProductGrid";
import { ProductFilters } from "@/components/product/ProductFilters";
import { ProductGridSkeleton } from "@/components/skeletons/ProductCardSkeleton";
import { useProducts, useCategories } from "@/hooks/useProducts";
import type { ProductFilters as FiltersType } from "@/lib/types";

const SORT_OPTIONS = [
  { label: "Newest", value: "newest" },
  { label: "Price: Low to High", value: "price_asc" },
  { label: "Price: High to Low", value: "price_desc" },
  { label: "Best Rating", value: "rating" },
] as const;

export default function ProductsPage() {
  const [filters, setFilters] = useState<FiltersType>({ page: 1, limit: 12 });
  const [showFilters, setShowFilters] = useState(false);
  const [searchInput, setSearchInput] = useState("");

  const { data: productsData, isLoading } = useProducts(filters);
  const { data: categoriesData } = useCategories();

  const products = productsData?.data ?? [];
  const categories = categoriesData?.data ?? [];

  const activeSort = SORT_OPTIONS.find((o) => o.value === (filters.sort_by ?? "newest"));
  const activeFiltersCount =
    (filters.category_id ? 1 : 0) +
    (filters.min_price ? 1 : 0) +
    (filters.max_price ? 1 : 0);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    setFilters((f) => ({ ...f, search: searchInput || undefined, page: 1 }));
  }

  function clearSearch() {
    setSearchInput("");
    setFilters((f) => ({ ...f, search: undefined, page: 1 }));
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">

      {/* ── Page Header ── */}
      <div className="mb-8">
        <p className="mb-1 text-xs font-semibold uppercase tracking-widest text-muted-foreground">
          Catalogue
        </p>
        <h1 className="text-3xl font-extrabold tracking-tight">All Products</h1>
      </div>

      {/* ── Toolbar ── */}
      <div className="mb-6 flex flex-wrap items-center gap-3">
        {/* Search */}
        <form onSubmit={handleSearch} className="relative flex-1 min-w-[200px] max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search products…"
            className="h-9 w-full rounded-full border bg-background pl-9 pr-8 text-sm outline-none focus:ring-2 focus:ring-ring transition"
          />
          {searchInput && (
            <button type="button" onClick={clearSearch} className="absolute right-3 top-1/2 -translate-y-1/2">
              <X className="h-3.5 w-3.5 text-muted-foreground" />
            </button>
          )}
        </form>

        {/* Filter toggle — mobile */}
        <Button
          variant="outline"
          size="sm"
          className="gap-2 rounded-full lg:hidden"
          onClick={() => setShowFilters(!showFilters)}
        >
          <SlidersHorizontal className="h-3.5 w-3.5" />
          Filters
          {activeFiltersCount > 0 && (
            <span className="flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[10px] font-bold text-primary-foreground">
              {activeFiltersCount}
            </span>
          )}
        </Button>

        {/* Sort dropdown */}
        <div className="relative ml-auto">
          <select
            className="h-9 appearance-none rounded-full border bg-background pl-4 pr-9 text-sm font-medium outline-none focus:ring-2 focus:ring-ring cursor-pointer transition"
            value={filters.sort_by ?? "newest"}
            onChange={(e) =>
              setFilters({ ...filters, sort_by: e.target.value as FiltersType["sort_by"] })
            }
          >
            {SORT_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
          <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        </div>

        {/* Result count */}
        {!isLoading && (
          <p className="text-sm text-muted-foreground whitespace-nowrap">
            {products.length} {products.length === 1 ? "product" : "products"}
            {activeSort && activeSort.value !== "newest" && (
              <span className="ml-1 text-foreground font-medium">· {activeSort.label}</span>
            )}
          </p>
        )}
      </div>

      {/* ── Content ── */}
      <div className="flex gap-8">
        {/* Sidebar */}
        <div className={`${showFilters ? "block" : "hidden"} w-full lg:block lg:w-auto shrink-0`}>
          <ProductFilters
            categories={categories}
            filters={filters}
            onFilterChange={setFilters}
          />
        </div>

        {/* Grid */}
        <div className="flex-1 min-w-0">
          {isLoading ? (
            <ProductGridSkeleton count={12} />
          ) : (
            <ProductGrid products={products} />
          )}
        </div>
      </div>
    </div>
  );
}
