import { Link } from "@tanstack/react-router";
import type { Product } from "@/data/products";
import { StarIcon, PlusIcon } from "@/components/icons";

export function ProductCard({ product }: { product: Product }) {
  const { id, img, badge, badgeTone, brand, name, rating, reviews, price, oldPrice } = product;

  return (
    <article className="group bg-paper ring-1 ring-black/5 rounded-2xl p-3 flex flex-col hover:shadow-[var(--shadow-card-hover)] transition-shadow">
      <Link
        to="/products/$id"
        params={{ id }}
        className="relative aspect-[4/5] rounded-xl overflow-hidden mb-4 bg-paper-tint block"
      >
        <img
          src={img}
          alt={name}
          loading="lazy"
          width={600}
          height={750}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-[1.03]"
        />
        {badge && (
          <span
            className={
              "absolute top-3 left-3 px-2 py-1 rounded text-[10px] font-bold ring-1 ring-black/5 " +
              (badgeTone === "brand"
                ? "bg-brand text-brand-foreground"
                : "bg-paper/90 backdrop-blur-sm text-ink")
            }
          >
            {badge}
          </span>
        )}
      </Link>
      <div className="px-1 flex flex-col flex-1">
        <div className="flex items-center gap-1.5 mb-1.5">
          <StarIcon className="size-3 text-amber-400" />
          <span className="text-[11px] font-medium text-ink-muted">{rating.toFixed(1)}</span>
          <span className="text-[11px] text-ink-subtle">·</span>
          <span className="text-[11px] text-ink-subtle">{reviews} recenzí</span>
        </div>
        <p className="text-[10px] text-ink-subtle font-semibold uppercase tracking-widest mb-1">
          {brand}
        </p>
        <h3 className="text-sm font-medium text-ink mb-1 line-clamp-2">
          <Link to="/products/$id" params={{ id }} className="hover:text-brand transition-colors">
            {name}
          </Link>
        </h3>
        <div className="flex items-baseline gap-2 mt-auto pt-3">
          <p className="text-lg font-semibold text-ink">{price}</p>
          {oldPrice && <p className="text-sm text-ink-subtle line-through">{oldPrice}</p>}
        </div>
        <button className="mt-3 w-full h-9 bg-ink text-paper text-[13px] font-medium rounded-lg hover:brightness-125 transition flex items-center justify-center gap-2">
          <PlusIcon className="size-4" />
          Do košíku
        </button>
      </div>
    </article>
  );
}
