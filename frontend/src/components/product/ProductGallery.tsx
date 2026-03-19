"use client";

import { useState } from "react";
import Image from "next/image";
import { cn } from "@/lib/utils";

interface ProductGalleryProps {
  images: string[];
  title: string;
}

export function ProductGallery({ images, title }: ProductGalleryProps) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const allImages = images.length > 0 ? images : ["/placeholder.svg"];

  return (
    <div className="space-y-4">
      {/* Main Image */}
      <div className="relative aspect-square overflow-hidden rounded-2xl bg-muted">
        <Image
          src={allImages[selectedIndex]}
          alt={`${title} — image ${selectedIndex + 1}`}
          fill
          priority
          className="object-cover"
          sizes="(max-width: 768px) 100vw, 50vw"
        />
      </div>

      {/* Thumbnails */}
      {allImages.length > 1 && (
        <div className="flex gap-3 overflow-x-auto pb-1 hide-scrollbar">
          {allImages.map((src, index) => (
            <button
              key={index}
              onClick={() => setSelectedIndex(index)}
              className={cn(
                "relative h-20 w-20 flex-shrink-0 overflow-hidden rounded-lg border-2 transition-all",
                selectedIndex === index
                  ? "border-primary ring-2 ring-primary/20"
                  : "border-transparent hover:border-muted-foreground/30"
              )}
              aria-label={`View image ${index + 1}`}
            >
              <Image
                src={src}
                alt={`${title} thumbnail ${index + 1}`}
                fill
                className="object-cover"
                sizes="80px"
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
