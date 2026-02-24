import Image from "next/image";

interface ProductImageProps {
  src: string | null;
  alt: string;
  className?: string;
  fill?: boolean;
  sizes?: string;
}

export function ProductImage({
  src,
  alt,
  className = "",
  fill = false,
  sizes = "(max-width: 768px) 100vw, 25vw",
}: ProductImageProps) {
  if (!src) {
    return (
      <div
        className={"flex items-center justify-center bg-[var(--border)] text-[var(--muted)] " + className}
        aria-hidden
      >
        No image
      </div>
    );
  }

  if (fill) {
    return (
      <Image
        src={src}
        alt={alt}
        fill
        sizes={sizes}
        className={"object-cover " + className}
        unoptimized
      />
    );
  }

  return (
    <Image
      src={src}
      alt={alt}
      width={400}
      height={400}
      className={"h-full w-full object-cover " + className}
      unoptimized
    />
  );
}
