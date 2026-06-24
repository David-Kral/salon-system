import { createFileRoute } from "@tanstack/react-router";
import heroImg from "@/assets/hero-stationery.jpg";
import storeImg from "@/assets/store-front.jpg";
import { products } from "@/data/products";
import { ProductCard } from "@/components/product-card";
import { SiteHeader, SiteFooter } from "@/components/site-chrome";
import {
  ArrowRight,
  PinIcon,
  TruckIcon,
  ShopIcon,
  ClockIcon,
  PhoneIcon,
  BackpackIcon,
  NotebookIcon,
  ClipIcon,
  BrushIcon,
  GiftIcon,
  LeafIcon,
  PuzzleIcon,
} from "@/components/icons";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Papírnictví Zásilkovna — Vše pro školu, kancelář i tvorbu" },
      {
        name: "description",
        content:
          "Lokální papírnictví s výdejním místem Zásilkovny. Školní, kancelářské a výtvarné potřeby, dárkové balení, hry a kreativita.",
      },
      { property: "og:title", content: "Papírnictví Zásilkovna" },
      {
        property: "og:description",
        content: "Vše pro školu, kancelář i kreativní tvorbu na jednom místě.",
      },
      { property: "og:image", content: heroImg },
      { name: "twitter:image", content: heroImg },
    ],
  }),
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

function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <SiteHeader />
      <main>
        <Hero />
        <Categories />
        <Benefits />
        <Products />
        <StoreSection />
      </main>
      <SiteFooter />
    </div>
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
              <a key={cat.name} href="#" className="group flex flex-col items-center gap-4">
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
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </div>
    </section>
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
