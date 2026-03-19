"use client";

import { Button } from "@/components/ui/button";
import type { Category, ProductFilters as FiltersType } from "@/lib/types";
import { cn } from "@/lib/utils";

interface ProductFiltersProps {
  categories: Category[];
  filters: FiltersType;
  onFilterChange: (filters: FiltersType) => void;
}

export function ProductFilters({ categories, filters, onFilterChange }: ProductFiltersProps) {
  const hasActiveFilters = !!filters.category_id || !!filters.min_price || !!filters.max_price;

  return (
    <aside className="w-full space-y-7 lg:w-56 lg:flex-shrink-0">

      {/* ── Categories ── */}
      <div>
        <p className="mb-3 text-[10px] font-semibold uppercase tracking-widest text-muted-foreground">
          Category
        </p>
        <div className="flex flex-col gap-0.5">
          <button
            onClick={() => onFilterChange({ ...filters, category_id: undefined })}
            className={cn(
              "flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors text-left",
              !filters.category_id
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:bg-muted hover:text-foreground"
            )}
          >
            All
            {!filters.category_id && (
              <span className="h-1.5 w-1.5 rounded-full bg-primary-foreground/60" />
            )}
          </button>

          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => onFilterChange({ ...filters, category_id: cat.id })}
              className={cn(
                "flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors text-left",
                filters.category_id === cat.id
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              {cat.name}
              {filters.category_id === cat.id && (
                <span className="h-1.5 w-1.5 rounded-full bg-primary-foreground/60" />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* ── Price Range ── */}
      <div>
        <p className="mb-3 text-[10px] font-semibold uppercase tracking-widest text-muted-foreground">
          Price Range
        </p>
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">$</span>
            <input
              type="number"
              placeholder="Min"
              value={filters.min_price ?? ""}
              onChange={(e) =>
                onFilterChange({
                  ...filters,
                  min_price: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              className="h-9 w-full rounded-lg border bg-background pl-5 pr-2 text-sm outline-none focus:ring-2 focus:ring-ring transition"
            />
          </div>
          <span className="text-xs text-muted-foreground">–</span>
          <div className="relative flex-1">
            <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-xs text-muted-foreground">$</span>
            <input
              type="number"
              placeholder="Max"
              value={filters.max_price ?? ""}
              onChange={(e) =>
                onFilterChange({
                  ...filters,
                  max_price: e.target.value ? Number(e.target.value) : undefined,
                })
              }
              className="h-9 w-full rounded-lg border bg-background pl-5 pr-2 text-sm outline-none focus:ring-2 focus:ring-ring transition"
            />
          </div>
        </div>
      </div>

      {/* ── Reset ── */}
      {hasActiveFilters && (
        <Button
          variant="ghost"
          size="sm"
          className="w-full rounded-full text-muted-foreground hover:text-foreground"
          onClick={() => onFilterChange({})}
        >
          Clear all filters
        </Button>
      )}
    </aside>
  );
}
