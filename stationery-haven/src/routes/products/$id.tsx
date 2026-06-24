import { useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { getProduct, getRelatedProducts } from "@/data/products";
import { ProductCard } from "@/components/product-card";
import { SiteHeader, SiteFooter } from "@/components/site-chrome";
import {
  StarIcon,
  PlusIcon,
  MinusIcon,
  CheckIcon,
  ChevronRight,
  ArrowLeft,
  PinIcon,
  TruckIcon,
  ShopIcon,
} from "@/components/icons";

export const Route = createFileRoute("/products/$id")({
  head: ({ params }) => {
    const product = getProduct(params.id);
    if (!product) {
      return { meta: [{ title: "Produkt nenalezen — Papírnictví Zásilkovna" }] };
    }
    return {
      meta: [
        { title: `${product.name} — ${product.brand} | Papírnictví Zásilkovna` },
        { name: "description", content: product.tagline },
        { property: "og:title", content: `${product.brand} ${product.name}` },
        { property: "og:description", content: product.tagline },
        { property: "og:image", content: product.img },
        { name: "twitter:image", content: product.img },
      ],
    };
  },
  component: ProductDetail,
});

function ProductDetail() {
  const { id } = Route.useParams();
  const product = getProduct(id);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <SiteHeader />
      <main>{product ? <ProductView id={id} /> : <NotFound />}</main>
      <SiteFooter />
    </div>
  );
}

function ProductView({ id }: { id: string }) {
  const product = getProduct(id)!;
  const related = getRelatedProducts(id, 4);
  const [qty, setQty] = useState(1);

  return (
    <>
      {/* Breadcrumb */}
      <div className="px-4 sm:px-6 pt-6">
        <div className="max-w-7xl mx-auto">
          <nav className="flex items-center gap-1.5 text-xs text-ink-muted flex-wrap">
            <Link to="/" className="hover:text-brand transition-colors">
              Domů
            </Link>
            <ChevronRight className="size-3 text-ink-subtle" />
            <span className="hover:text-brand transition-colors">{product.category}</span>
            <ChevronRight className="size-3 text-ink-subtle" />
            <span className="text-ink font-medium truncate max-w-[60vw]">{product.name}</span>
          </nav>
        </div>
      </div>

      {/* Product hero */}
      <section className="px-4 sm:px-6 py-8 md:py-12">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-14">
          {/* Image */}
          <div className="relative">
            <div className="w-full aspect-[4/5] max-w-lg lg:max-w-none rounded-2xl overflow-hidden bg-paper-tint ring-1 ring-black/5">
              <img
                src={product.img}
                alt={product.name}
                width={800}
                height={1000}
                className="w-full h-full object-cover"
              />
              {product.badge && (
                <span
                  className={
                    "absolute top-4 left-4 px-2.5 py-1 rounded text-[11px] font-bold ring-1 ring-black/5 " +
                    (product.badgeTone === "brand"
                      ? "bg-brand text-brand-foreground"
                      : "bg-paper/90 backdrop-blur-sm text-ink")
                  }
                >
                  {product.badge}
                </span>
              )}
            </div>
          </div>

          {/* Info */}
          <div className="flex flex-col">
            <p className="text-[11px] text-brand font-bold uppercase tracking-[0.2em] mb-3">
              {product.category}
            </p>
            <p className="text-[11px] text-ink-subtle font-semibold uppercase tracking-widest mb-2">
              {product.brand}
            </p>
            <h1 className="text-2xl md:text-3xl lg:text-4xl font-medium text-ink tracking-tight leading-tight mb-4">
              {product.name}
            </h1>

            <div className="flex items-center gap-2 mb-5">
              <div className="flex items-center gap-1.5">
                <StarIcon className="size-4 text-amber-400" />
                <span className="text-sm font-medium text-ink">{product.rating.toFixed(1)}</span>
              </div>
              <span className="text-sm text-ink-subtle">·</span>
              <span className="text-sm text-ink-muted">{product.reviews} recenzí</span>
            </div>

            <p className="text-ink-muted text-pretty max-w-[52ch] mb-6">{product.tagline}</p>

            <div className="flex items-baseline gap-3 mb-2">
              <span className="text-3xl font-semibold text-ink">{product.price}</span>
              {product.oldPrice && (
                <span className="text-lg text-ink-subtle line-through">{product.oldPrice}</span>
              )}
            </div>
            <p className="text-xs text-ink-subtle mb-6">Cena včetně DPH</p>

            {/* Stock */}
            <div className="mb-6">
              {product.inStock ? (
                <span className="inline-flex items-center gap-1.5 text-sm font-medium text-emerald-600">
                  <CheckIcon className="size-4" />
                  Skladem — odešleme ihned
                </span>
              ) : (
                <span className="inline-flex items-center gap-1.5 text-sm font-medium text-ink-muted">
                  <ClockDot />
                  Dočasně vyprodáno
                </span>
              )}
            </div>

            {/* Quantity + add to cart */}
            <div className="flex items-stretch gap-3 mb-8 max-w-md">
              <div className="flex items-center rounded-lg ring-1 ring-black/10 bg-paper">
                <button
                  type="button"
                  onClick={() => setQty((q) => Math.max(1, q - 1))}
                  className="size-11 grid place-items-center text-ink-muted hover:text-ink transition-colors disabled:opacity-40"
                  disabled={qty <= 1}
                  aria-label="Ubrat kus"
                >
                  <MinusIcon className="size-4" />
                </button>
                <span className="w-10 text-center text-sm font-medium text-ink tabular-nums">
                  {qty}
                </span>
                <button
                  type="button"
                  onClick={() => setQty((q) => Math.min(99, q + 1))}
                  className="size-11 grid place-items-center text-ink-muted hover:text-ink transition-colors"
                  aria-label="Přidat kus"
                >
                  <PlusIcon className="size-4" />
                </button>
              </div>
              <button
                className="flex-1 h-11 px-6 bg-ink text-paper text-sm font-medium rounded-lg hover:brightness-125 transition active:scale-[0.99] flex items-center justify-center gap-2 disabled:opacity-50 disabled:hover:brightness-100"
                disabled={!product.inStock}
              >
                <PlusIcon className="size-4" />
                {product.inStock ? "Přidat do košíku" : "Není skladem"}
              </button>
            </div>

            {/* Mini benefits */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 py-6 border-t border-line/60">
              <MiniBenefit icon={TruckIcon} title="Doprava od 79 Kč" desc="Zdarma nad 1 000 Kč" />
              <MiniBenefit icon={PinIcon} title="Výdejna Zásilkovny" desc="Vyzvednutí v prodejně" />
              <MiniBenefit icon={ShopIcon} title="Osobní odběr" desc="Dnes do 18:00 na Letné" />
            </div>
          </div>
        </div>
      </section>

      {/* Description + specs */}
      <section className="px-4 sm:px-6 pb-8">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-14">
          <div>
            <h2 className="text-lg font-semibold text-ink mb-4">Popis produktu</h2>
            <div className="space-y-4 text-sm text-ink-muted leading-relaxed max-w-[60ch]">
              {product.description.map((para, i) => (
                <p key={i}>{para}</p>
              ))}
            </div>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-ink mb-4">Parametry</h2>
            <dl className="rounded-2xl ring-1 ring-black/5 bg-paper overflow-hidden">
              {product.features.map((f, i) => (
                <div
                  key={i}
                  className={
                    "flex items-start gap-3 px-4 py-3 text-sm " +
                    (i % 2 === 1 ? "bg-paper-tint/50" : "")
                  }
                >
                  <CheckIcon className="size-4 text-brand mt-0.5 shrink-0" />
                  <span className="text-ink">{f}</span>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </section>

      {/* Related products */}
      {related.length > 0 && (
        <section className="px-4 sm:px-6 py-16 md:py-20">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-end justify-between mb-8 gap-4">
              <h2 className="text-2xl md:text-3xl font-medium text-ink tracking-tight">
                Mohlo by se vám líbit
              </h2>
              <Link
                to="/"
                className="text-sm font-medium text-ink-muted hover:text-brand flex items-center gap-1 transition-colors shrink-0"
              >
                <ArrowLeft className="size-3" />
                Zpět na úvod
              </Link>
            </div>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
              {related.map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          </div>
        </section>
      )}
    </>
  );
}

function MiniBenefit({
  icon: Icon,
  title,
  desc,
}: {
  icon: (p: { className?: string }) => React.ReactElement;
  title: string;
  desc: string;
}) {
  return (
    <div className="flex items-start gap-3">
      <div className="shrink-0 size-9 rounded-lg bg-paper-tint ring-1 ring-black/5 grid place-items-center text-ink/70">
        <Icon className="size-5" />
      </div>
      <div className="min-w-0">
        <p className="text-[13px] font-semibold text-ink leading-tight">{title}</p>
        <p className="text-xs text-ink-muted mt-0.5">{desc}</p>
      </div>
    </div>
  );
}

function ClockDot() {
  return <span className="size-2 rounded-full bg-ink-subtle" aria-hidden />;
}

function NotFound() {
  return (
    <section className="px-4 sm:px-6 py-24">
      <div className="max-w-md mx-auto text-center">
        <p className="text-[11px] font-bold text-brand uppercase tracking-[0.2em] mb-3">404</p>
        <h1 className="text-2xl font-medium text-ink tracking-tight mb-3">
          Produkt jsme nenašli
        </h1>
        <p className="text-sm text-ink-muted mb-8">
          Tento produkt už možná není v nabídce nebo odkaz není správný.
        </p>
        <Link
          to="/"
          className="inline-flex items-center justify-center gap-2 h-11 px-6 bg-ink text-paper text-sm font-medium rounded-lg hover:brightness-125 transition"
        >
          <ArrowLeft className="size-4" />
          Zpět do obchodu
        </Link>
      </div>
    </section>
  );
}
