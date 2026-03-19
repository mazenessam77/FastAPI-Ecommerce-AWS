"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { ProductFilters } from "@/lib/types";

export function useProducts(filters?: ProductFilters) {
  return useQuery({
    queryKey: ["products", filters],
    queryFn: () => api.getProducts(filters),
    staleTime: 1000 * 60 * 2,
  });
}

export function useCategories() {
  return useQuery({
    queryKey: ["categories"],
    queryFn: () => api.getCategories(),
    staleTime: 1000 * 60 * 10,
  });
}
