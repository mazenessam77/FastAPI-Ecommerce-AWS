import { Skeleton } from "@/components/ui/skeleton";

export default function HomeLoading() {
  return (
    <div className="space-y-16">
      {/* Hero skeleton */}
      <div className="bg-muted/50 py-24 text-center">
        <div className="mx-auto max-w-2xl space-y-4 px-4">
          <Skeleton className="mx-auto h-12 w-3/4" />
          <Skeleton className="mx-auto h-6 w-1/2" />
          <div className="flex justify-center gap-4 pt-6">
            <Skeleton className="h-11 w-32" />
            <Skeleton className="h-11 w-40" />
          </div>
        </div>
      </div>
      {/* Grid skeleton */}
      <div className="mx-auto max-w-7xl px-4">
        <Skeleton className="h-8 w-48 mb-8" />
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="space-y-3">
              <Skeleton className="aspect-square w-full rounded-xl" />
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-6 w-1/3" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
