"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import type { Category, ProductFilters as FiltersType } from "@/lib/types";
import { cn } from "@/lib/utils";

interface ProductFiltersProps {
  categories: Category[];
  filters: FiltersType;
  onFilterChange: (filters: FiltersType) => void;
}

export function ProductFilters({
  categories,
  filters,
  onFilterChange,
}: ProductFiltersProps) {
  return (
    <aside className="w-full space-y-6 lg:w-64 lg:flex-shrink-0">
      {/* Categories */}
      <div>
        <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider">
          Categories
        </h3>
        <div className="space-y-1">
          <button
            onClick={() => onFilterChange({ ...filters, category_id: undefined })}
            className={cn(
              "block w-full rounded-md px-3 py-2 text-left text-sm transition-colors",
              !filters.category_id
                ? "bg-primary text-primary-foreground"
                : "text-muted-foreground hover:bg-muted"
            )}
          >
            All Categories
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => onFilterChange({ ...filters, category_id: cat.id })}
              className={cn(
                "block w-full rounded-md px-3 py-2 text-left text-sm transition-colors",
                filters.category_id === cat.id
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted"
              )}
            >
              {cat.name}
            </button>
          ))}
        </div>
      </div>

      <Separator />

      {/* Price Range */}
      <div>
        <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider">
          Price Range
        </h3>
        <div className="flex items-center gap-2">
          <Input
            type="number"
            placeholder="Min"
            value={filters.min_price ?? ""}
            onChange={(e) =>
              onFilterChange({
                ...filters,
                min_price: e.target.value ? Number(e.target.value) : undefined,
              })
            }
            className="h-9"
          />
          <span className="text-muted-foreground">-</span>
          <Input
            type="number"
            placeholder="Max"
            value={filters.max_price ?? ""}
            onChange={(e) =>
              onFilterChange({
                ...filters,
                max_price: e.target.value ? Number(e.target.value) : undefined,
              })
            }
            className="h-9"
          />
        </div>
      </div>

      <Separator />

      {/* Reset */}
      <Button
        variant="outline"
        size="sm"
        className="w-full"
        onClick={() => onFilterChange({})}
      >
        Reset Filters
      </Button>
    </aside>
  );
}
