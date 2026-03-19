"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

const SIZES = ["XS", "S", "M", "L", "XL"];
const COLORS = [
  { name: "Black", value: "#000000" },
  { name: "White", value: "#FFFFFF" },
  { name: "Navy", value: "#1e3a5f" },
  { name: "Red", value: "#dc2626" },
];

interface ProductVariantsProps {
  onSizeChange?: (size: string) => void;
  onColorChange?: (color: string) => void;
}

export function ProductVariants({
  onSizeChange,
  onColorChange,
}: ProductVariantsProps) {
  const [selectedSize, setSelectedSize] = useState("M");
  const [selectedColor, setSelectedColor] = useState("Black");

  return (
    <div className="space-y-6">
      {/* Color */}
      <div>
        <h3 className="text-sm font-medium">
          Color: <span className="text-muted-foreground">{selectedColor}</span>
        </h3>
        <div className="mt-2 flex gap-2">
          {COLORS.map((color) => (
            <button
              key={color.name}
              onClick={() => {
                setSelectedColor(color.name);
                onColorChange?.(color.name);
              }}
              className={cn(
                "h-9 w-9 rounded-full border-2 transition-all",
                selectedColor === color.name
                  ? "border-primary ring-2 ring-primary/20"
                  : "border-muted hover:border-muted-foreground/50"
              )}
              style={{ backgroundColor: color.value }}
              aria-label={`Select ${color.name}`}
            />
          ))}
        </div>
      </div>

      {/* Size */}
      <div>
        <h3 className="text-sm font-medium">Size</h3>
        <div className="mt-2 flex flex-wrap gap-2">
          {SIZES.map((size) => (
            <button
              key={size}
              onClick={() => {
                setSelectedSize(size);
                onSizeChange?.(size);
              }}
              className={cn(
                "flex h-10 w-12 items-center justify-center rounded-md border text-sm font-medium transition-all",
                selectedSize === size
                  ? "border-primary bg-primary text-primary-foreground"
                  : "border-input bg-background hover:bg-accent"
              )}
            >
              {size}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
