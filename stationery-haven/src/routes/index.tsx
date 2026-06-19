import { createFileRoute } from "@tanstack/react-router";
import heroImg from "@/assets/hero-stationery.jpg";
import storeImg from "@/assets/store-front.jpg";
import productNotebook from "@/assets/product-notebook.jpg";
import productPen from "@/assets/product-pen.jpg";
import productWatercolor from "@/assets/product-watercolor.jpg";
import productWashi from "@/assets/product-washi.jpg";

export const Route = createFileRoute("/")({
  component: Home,
});

const categories = [
  { name: "Školní potřeby", tint: "var(--cat-school)", icon: BackpackIcon },
  { name: "Papírnictví", tint: "var(--cat-paper)", icon: NotebookIcon },
  { name: "Kancelářské potřeby", tint: "var(--cat-office)", icon: ClipIcon },
  { name: "Výtvarné potřeby", tint: "var(--cat-art)", icon: BrushIcon },
  { name: "Dárkové balení", tint: "var(--cat-gift)", icon: GiftIcon },
  { name: "Sezónní zboží", tint: "var(--cat-season)", icon: LeafIcon },
  { name: "Hry a kreativita", tint: "var(--cat-play)", icon: PuzzleIcon },
];

const products = [
  {
    img: productNotebook,
    badge: "NOVINKA",
    badgeTone: "neutral" as const,
    brand: "Leuchtturm1917",
    name: "Zápisník Medium A5, tečkovaný",
    rating: 4.9,
    reviews: 12,
    price: "520 Kč",
  },
  {
    img: productPen,
    badge: "−15 %",
    badgeTone: "brand" as const,
    brand: "Kaweco",
    name: "Sport Mint Edition, kuličkové pero",
    rating: 5.0,
    reviews: 8,
    price: "589 Kč",
    oldPrice: "690 Kč",
  },
  {
    img: productWatercolor,
    brand: "Schmincke",
    name: "Akvarelové barvy Horadam, 12 ks",
    rating: 4.8,
    reviews: 24,
    price: "1 450 Kč",
  },
  {
    img: productWashi,
    badge: "BESTSELLER",
    badgeTone: "neutral" as const,
    brand: "MT",
    name: "Washi pásky – pastel set 4 ks",
    rating: 4.7,
    reviews: 42,
    price: "320 Kč",
  },
];

function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <UtilityBar />
      <Header />
      <main>
        <Hero />
        <Categories />
        <Benefits />
        <Products />
        <StoreSection />
      </main>
      <Footer />
    </div>
  );
}

/* ---------- Utility bar ---------- */
function UtilityBar() {
  return (
    <div className="bg-paper-tint border-b border-line/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-10 flex items-center justify-between gap-4">
        <div className="flex items-center gap-4 min-w-0">
          <span className="flex items-center gap-2 text-xs text-ink-muted">
            <span className="size-2 rounded-full bg-brand" aria-hidden />
            <span className="truncate">Oficiální výdejní místo Zásilkovny</span>
          </span>
          <span className="hidden md:inline text-xs text-ink-subtle">|</span>
          <span className="hidden md:inline text-xs text-ink-muted">
            Osobní odběr dnes do 18:00
          </span>
        </div>
        <div className="hidden sm:flex items-center gap-6 shrink-0">
          <a href="#" className="text-xs text-ink-muted hover:text-ink transition-colors">
            Sledovat zásilku
          </a>
          <a href="#" className="text-xs text-ink-muted hover:text-ink transition-colors">
            Doprava a platba
          </a>
        </div>
      </div>
    </div>
  );
}

/* ---------- Header ---------- */
function Header() {
  return (
    <header className="sticky top-0 z-50 bg-paper/85 backdrop-blur-md border-b border-line/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-20 grid grid-cols-[auto_1fr_auto] items-center gap-6 md:gap-10">
        <a href="/" className="flex items-baseline gap-0.5 shrink-0">
          <span className="text-xl font-semibold tracking-tight text-ink">Papírnictví</span>
          <span className="text-brand text-xl font-semibold">.</span>
          <span className="text-xl font-semibold tracking-tight text-ink">Zásilkovna</span>
        </a>

        <div className="min-w-0 max-w-2xl w-full justify-self-center">
          <div className="relative">
            <input
              type="search"
              placeholder="Hledat sešity, pera nebo barvy…"
              className="w-full h-10 pl-4 pr-10 bg-paper-tint rounded-lg text-sm border border-transparent ring-1 ring-black/5 focus:border-brand/40 focus:ring-brand/20 outline-none transition"
            />
            <SearchIcon className="absolute right-3 top-1/2 -translate-y-1/2 size-4 text-ink-subtle" />
          </div>
        </div>

        <div className="flex items-center gap-5 sm:gap-7 shrink-0">
          <IconButton label="Účet">
            <UserIcon className="size-5" />
          </IconButton>
          <IconButton label="Košík" badge="0">
            <BagIcon className="size-5" />
          </IconButton>
        </div>
      </div>
    </header>
  );
}

function IconButton({
  children,
  label,
  badge,
}: {
  children: React.ReactNode;
  label: string;
  badge?: string;
}) {
  return (
    <button className="relative flex flex-col items-center gap-0.5 group">
      <span className="text-ink-muted group-hover:text-ink transition-colors">{children}</span>
      <span className="text-[10px] font-medium text-ink-subtle uppercase tracking-tight">
        {label}
      </span>
      {badge !== undefined && (
        <span className="absolute -top-1 -right-1.5 size-4 bg-brand text-[9px] font-bold text-brand-foreground rounded-full flex items-center justify-center">
          {badge}
        </span>
      )}
    </button>
  );
}

/* ---------- Hero ---------- */
function Hero() {
  return (
    <section className="px-4 sm:px-6 py-10 md:py-14">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-12 gap-8 items-center">
          <div className="col-span-12 lg:col-span-5">
            <span className="inline-block text-[10px] font-bold text-brand uppercase tracking-[0.2em] mb-5">
              Lokální papírnictví od roku 2005
            </span>
            <h1 className="text-4xl lg:text-[3.25rem] font-medium text-ink leading-[1.1] tracking-tight text-balance mb-6">
              Vše pro školu, kancelář i kreativní tvorbu na jednom místě
            </h1>
            <p className="text-ink-muted mb-8 max-w-[48ch] text-pretty">
              Tradiční papírnictví s moderním duchem. Vaše sousedská prodejna —
              nyní i s kompletním sortimentem online a výdejnou Zásilkovny přímo
              v obchodě.
            </p>
            <div className="flex items-center gap-3">
              <button className="h-11 px-6 bg-ink text-paper text-sm font-medium rounded-lg hover:brightness-125 transition active:scale-[0.98]">
                Prozkoumat nabídku
              </button>
              <button className="h-11 px-6 bg-paper-tint text-ink text-sm font-medium rounded-lg hover:bg-line/70 transition ring-1 ring-black/5">
                Kde nás najdete
              </button>
            </div>
          </div>
          <div className="col-span-12 lg:col-span-7">
            <div className="w-full aspect-[16/10] rounded-2xl overflow-hidden ring-1 ring-black/5 bg-paper-tint">
              <img
                src={heroImg}
                alt="Pracovní stůl s papírnictvím — sešity, pera, washi pásky"
                width={1280}
                height={800}
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---------- Categories ---------- */
function Categories() {
  return (
    <section className="px-4 sm:px-6 py-14 md:py-20 bg-paper-tint/60 border-y border-line/60">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-end justify-between mb-10">
          <div>
            <h2 className="text-2xl md:text-3xl font-medium text-ink mb-2 tracking-tight">
              Oblíbené kategorie
            </h2>
            <p className="text-sm text-ink-muted">Vyberte si podle toho, co právě hledáte</p>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4">
          {categories.map((cat) => {
            const Icon = cat.icon;
            return (
              <a
                key={cat.name}
                href="#"
                className="group flex flex-col items-center gap-4"
              >
                <div
                  className="w-full aspect-square bg-paper ring-1 ring-black/5 rounded-2xl flex items-center justify-center p-6 group-hover:ring-brand/30 group-hover:-translate-y-0.5 transition-all"
                  style={{ backgroundColor: cat.tint }}
                >
                  <Icon className="size-10 text-ink/70" />
                </div>
                <span className="text-sm font-medium text-ink text-center leading-tight">
                  {cat.name}
                </span>
              </a>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ---------- Benefits ---------- */
function Benefits() {
  const items = [
    {
      icon: PinIcon,
      title: "Výdejní místo Zásilkovny",
      desc: "Vyzvedněte si u nás jakýkoliv balíček při cestě z nákupu.",
    },
    {
      icon: TruckIcon,
      title: "Doprava zdarma nad 1 000 Kč",
      desc: "Pro školy a firmy doprava vždy zdarma na faktury.",
    },
    {
      icon: ShopIcon,
      title: "Kamenná prodejna",
      desc: "Navštivte nás osobně, osahejte si papír a nechte se inspirovat.",
    },
  ];
  return (
    <section className="px-4 sm:px-6 py-10">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 py-6 border-b border-line/60">
          {items.map((it) => {
            const Icon = it.icon;
            return (
              <div key={it.title} className="flex items-start gap-4">
                <div className="shrink-0 size-10 rounded-lg bg-paper-tint ring-1 ring-black/5 grid place-items-center text-ink/70">
                  <Icon className="size-5" />
                </div>
                <div className="min-w-0">
                  <h3 className="text-sm font-semibold text-ink">{it.title}</h3>
                  <p className="text-xs text-ink-muted leading-relaxed mt-1">{it.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

/* ---------- Products ---------- */
function Products() {
  return (
    <section className="px-4 sm:px-6 py-16 md:py-20">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-end justify-between mb-8 gap-4">
          <div className="min-w-0">
            <span className="text-[10px] font-bold text-brand uppercase tracking-[0.2em]">
              Aktuální výběr
            </span>
            <h2 className="text-2xl md:text-3xl font-medium text-ink mt-1 tracking-tight">
              Bestsellery a novinky
            </h2>
          </div>
          <a
            href="#"
            className="text-sm font-medium text-ink-muted hover:text-brand flex items-center gap-1 transition-colors shrink-0"
          >
            Zobrazit vše
            <ArrowRight className="size-3" />
          </a>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
          {products.map((p) => (
            <ProductCard key={p.name} {...p} />
          ))}
        </div>
      </div>
    </section>
  );
}

function ProductCard({
  img,
  badge,
  badgeTone,
  brand,
  name,
  rating,
  reviews,
  price,
  oldPrice,
}: {
  img: string;
  badge?: string;
  badgeTone?: "brand" | "neutral";
  brand: string;
  name: string;
  rating: number;
  reviews: number;
  price: string;
  oldPrice?: string;
}) {
  return (
    <article className="group bg-paper ring-1 ring-black/5 rounded-2xl p-3 flex flex-col hover:shadow-[var(--shadow-card-hover)] transition-shadow">
      <div className="relative aspect-[4/5] rounded-xl overflow-hidden mb-4 bg-paper-tint">
        <img
          src={img}
          alt={name}
          loading="lazy"
          width={600}
          height={750}
          className="w-full h-full object-cover"
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
      </div>
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
        <h3 className="text-sm font-medium text-ink mb-1 group-hover:text-brand transition-colors line-clamp-2">
          {name}
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

/* ---------- Store Section ---------- */
function StoreSection() {
  return (
    <section className="px-4 sm:px-6 py-16 md:py-24">
      <div className="max-w-7xl mx-auto">
        <div className="bg-ink rounded-3xl overflow-hidden grid grid-cols-1 lg:grid-cols-2">
          <div className="p-10 lg:p-16 flex flex-col justify-center">
            <span className="text-brand font-semibold text-[10px] uppercase tracking-[0.25em] mb-4">
              Navštivte nás
            </span>
            <h2 className="text-3xl md:text-4xl font-medium text-paper mb-8 tracking-tight text-balance">
              Pojďte si vybrat osobně do naší prodejny
            </h2>

            <div className="space-y-6">
              <InfoRow icon={PinIcon} title="Milady Horákové 123/45">
                170 00 Praha 7 — Letná
              </InfoRow>
              <InfoRow icon={ClockIcon} title="Otevírací doba">
                <div className="grid grid-cols-2 gap-x-6 gap-y-0.5 mt-1 text-sm max-w-sm">
                  <span className="text-paper/60">Pondělí – Pátek</span>
                  <span className="text-paper/90 text-right tabular-nums">09:00 – 19:00</span>
                  <span className="text-paper/60">Sobota</span>
                  <span className="text-paper/90 text-right tabular-nums">10:00 – 16:00</span>
                  <span className="text-paper/60">Neděle</span>
                  <span className="text-paper/90 text-right tabular-nums">Zavřeno</span>
                </div>
              </InfoRow>
              <InfoRow icon={PhoneIcon} title="+420 123 456 789">
                info@papirnictvi-zasilkovna.cz
              </InfoRow>
            </div>
          </div>
          <div className="min-h-[320px] lg:min-h-full border-t lg:border-t-0 lg:border-l border-white/5">
            <img
              src={storeImg}
              alt="Kamenná prodejna na Letné"
              loading="lazy"
              width={1000}
              height={1000}
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </section>
  );
}

function InfoRow({
  icon: Icon,
  title,
  children,
}: {
  icon: (p: { className?: string }) => React.ReactElement;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex gap-4">
      <div className="shrink-0 size-10 rounded-full bg-white/5 grid place-items-center">
        <Icon className="size-5 text-paper/70" />
      </div>
      <div className="min-w-0">
        <p className="text-paper font-medium">{title}</p>
        <div className="text-paper/60 text-sm">{children}</div>
      </div>
    </div>
  );
}

/* ---------- Footer ---------- */
function Footer() {
  return (
    <footer className="bg-paper-tint/70 pt-16 pb-10 px-4 sm:px-6 border-t border-line/60">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
          <div className="col-span-2 md:col-span-1 space-y-4">
            <div className="flex items-baseline gap-0.5">
              <span className="text-lg font-semibold tracking-tight text-ink">Papírnictví</span>
              <span className="text-brand text-lg font-semibold">.</span>
              <span className="text-lg font-semibold tracking-tight text-ink">Zásilkovna</span>
            </div>
            <p className="text-sm text-ink-muted leading-relaxed max-w-xs">
              Váš lokální dodavatel papíru a radosti z tvoření již od roku 2005.
            </p>
          </div>
          <FooterCol
            title="Nákup"
            links={["Doprava a platba", "Reklamační řád", "Obchodní podmínky", "Časté dotazy"]}
          />
          <FooterCol
            title="O nás"
            links={["Náš příběh", "Kontakty", "Pro školy a firmy", "Blog"]}
          />
          <div className="space-y-4">
            <h5 className="text-xs font-semibold text-ink uppercase tracking-widest">
              Newsletter
            </h5>
            <p className="text-sm text-ink-muted">Tipy, akce a novinky jednou měsíčně.</p>
            <form
              onSubmit={(e) => e.preventDefault()}
              className="flex gap-2"
            >
              <input
                type="email"
                placeholder="vas@email.cz"
                className="flex-1 min-w-0 h-9 px-3 bg-paper border border-line rounded-md text-sm focus:outline-none focus:border-brand/50"
              />
              <button className="h-9 px-4 bg-ink text-paper text-sm font-medium rounded-md hover:brightness-125 transition">
                Odebírat
              </button>
            </form>
          </div>
        </div>

        <div className="pt-8 border-t border-line flex flex-col md:flex-row justify-between items-center gap-6">
          <p className="text-xs text-ink-subtle">
            © 2026 Papírnictví Zásilkovna. Všechna práva vyhrazena.
          </p>
          <div className="flex items-center gap-3">
            {["VISA", "MC", "GPAY", "APPLE", "ZÁSILKOVNA"].map((p) => (
              <span
                key={p}
                className="h-7 px-2.5 bg-paper border border-line rounded grid place-items-center text-[9px] font-bold text-ink-subtle tracking-wider"
              >
                {p}
              </span>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}

function FooterCol({ title, links }: { title: string; links: string[] }) {
  return (
    <div className="space-y-4">
      <h5 className="text-xs font-semibold text-ink uppercase tracking-widest">{title}</h5>
      <ul className="text-sm text-ink-muted space-y-2">
        {links.map((l) => (
          <li key={l}>
            <a href="#" className="hover:text-brand transition-colors">
              {l}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ---------- Icons (inline, stroke-based) ---------- */
type IconProps = { className?: string };
const stroke = {
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.5,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

function SearchIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <circle cx="11" cy="11" r="7" />
      <path d="m20 20-3.5-3.5" />
    </svg>
  );
}
function UserIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <circle cx="12" cy="8" r="4" />
      <path d="M4 21a8 8 0 0 1 16 0" />
    </svg>
  );
}
function BagIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M5 8h14l-1 12H6L5 8Z" />
      <path d="M9 8V6a3 3 0 0 1 6 0v2" />
    </svg>
  );
}
function StarIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path d="M10 1.5l2.6 5.27 5.82.85-4.21 4.1.99 5.79L10 14.77 4.8 17.5l.99-5.78L1.58 7.62l5.82-.85L10 1.5z" />
    </svg>
  );
}
function PlusIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M12 5v14M5 12h14" />
    </svg>
  );
}
function ArrowRight({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke} strokeWidth={2}>
      <path d="m9 5 7 7-7 7" />
    </svg>
  );
}
function PinIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M12 21s-7-6.5-7-12a7 7 0 1 1 14 0c0 5.5-7 12-7 12Z" />
      <circle cx="12" cy="9" r="2.5" />
    </svg>
  );
}
function TruckIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M3 7h11v9H3zM14 10h4l3 3v3h-7" />
      <circle cx="7" cy="18" r="1.8" />
      <circle cx="17" cy="18" r="1.8" />
    </svg>
  );
}
function ShopIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M4 9h16l-1 11H5L4 9Z" />
      <path d="M4 9l2-5h12l2 5" />
      <path d="M10 13h4v7h-4z" />
    </svg>
  );
}
function ClockIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3 2" />
    </svg>
  );
}
function PhoneIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2Z" />
    </svg>
  );
}
function BackpackIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M6 9a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v11H6V9Z" />
      <path d="M9 5V3.5A1.5 1.5 0 0 1 10.5 2h3A1.5 1.5 0 0 1 15 3.5V5" />
      <path d="M9 13h6" />
    </svg>
  );
}
function NotebookIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M6 3h11a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6V3Z" />
      <path d="M6 7H4M6 12H4M6 17H4" />
    </svg>
  );
}
function ClipIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
      <rect x="5" y="6" width="14" height="16" rx="2" />
      <path d="M9 12h6M9 16h4" />
    </svg>
  );
}
function BrushIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M14 4l6 6-8 8H6v-6l8-8Z" />
      <path d="M4 20s2-1 3-1 1 1 2 1" />
    </svg>
  );
}
function GiftIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <rect x="3" y="9" width="18" height="12" rx="1" />
      <path d="M3 13h18M12 9v12" />
      <path d="M12 9c-2 0-4-1-4-3s2-2 3-1 1 4 1 4Zm0 0c2 0 4-1 4-3s-2-2-3-1-1 4-1 4Z" />
    </svg>
  );
}
function LeafIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M20 4c0 8-6 14-14 14 0 0-2-8 4-14 4-4 10-4 10-4-1 1-1 4 0 4Z" />
      <path d="M4 20c4-4 8-6 12-8" />
    </svg>
  );
}
function PuzzleIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" {...stroke}>
      <path d="M10 3h4v3a2 2 0 1 0 4 0V3h3v4h-3a2 2 0 1 0 0 4h3v4h-4a2 2 0 1 1-4 0v4H6v-4a2 2 0 1 0-3 0H3v-4h3a2 2 0 1 0 0-4H3V3h3v3a2 2 0 1 0 4 0V3Z" />
    </svg>
  );
}
