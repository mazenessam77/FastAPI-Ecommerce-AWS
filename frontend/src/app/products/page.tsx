"use client";

import { useState } from "react";
import { SlidersHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProductGrid } from "@/components/product/ProductGrid";
import { ProductFilters } from "@/components/product/ProductFilters";
import { ProductGridSkeleton } from "@/components/skeletons/ProductCardSkeleton";
import { useProducts, useCategories } from "@/hooks/useProducts";
import type { ProductFilters as FiltersType } from "@/lib/types";

/**
 * Product Listing Page — Client-side fetching with TanStack Query
 * for instant filter/sort updates without full page reloads.
 */
export default function ProductsPage() {
  const [filters, setFilters] = useState<FiltersType>({ page: 1, limit: 12 });
  const [showFilters, setShowFilters] = useState(false);

  const { data: productsData, isLoading } = useProducts(filters);
  const { data: categoriesData } = useCategories();

  const products = productsData?.data ?? [];
  const categories = categoriesData?.data ?? [];

  const sortOptions = [
    { label: "Newest", value: "newest" },
    { label: "Price: Low to High", value: "price_asc" },
    { label: "Price: High to Low", value: "price_desc" },
    { label: "Best Rating", value: "rating" },
  ] as const;

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">All Products</h1>
        <p className="mt-2 text-muted-foreground">
          Browse our curated collection of premium products
        </p>
      </div>

      {/* Toolbar */}
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <Button
          variant="outline"
          size="sm"
          className="gap-2 lg:hidden"
          onClick={() => setShowFilters(!showFilters)}
        >
          <SlidersHorizontal className="h-4 w-4" />
          Filters
        </Button>

        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Sort by:</span>
          <select
            className="rounded-md border bg-background px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-ring"
            value={filters.sort_by ?? "newest"}
            onChange={(e) =>
              setFilters({
                ...filters,
                sort_by: e.target.value as FiltersType["sort_by"],
              })
            }
          >
            {sortOptions.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Content */}
      <div className="flex gap-8">
        {/* Sidebar — Desktop always visible, mobile toggleable */}
        <div
          className={`${
            showFilters ? "block" : "hidden"
          } w-full lg:block lg:w-auto`}
        >
          <ProductFilters
            categories={categories}
            filters={filters}
            onFilterChange={setFilters}
          />
        </div>

        {/* Grid */}
        <div className="flex-1">
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
