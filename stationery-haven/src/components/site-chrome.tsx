import { Link } from "@tanstack/react-router";
import {
  SearchIcon,
  UserIcon,
  BagIcon,
} from "@/components/icons";

/* ---------- Utility bar ---------- */
export function UtilityBar() {
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
export function Header() {
  return (
    <header className="sticky top-0 z-50 bg-paper/85 backdrop-blur-md border-b border-line/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-20 grid grid-cols-[auto_1fr_auto] items-center gap-6 md:gap-10">
        <Link to="/" className="flex items-baseline gap-0.5 shrink-0">
          <span className="text-xl font-semibold tracking-tight text-ink">Papírnictví</span>
          <span className="text-brand text-xl font-semibold">.</span>
          <span className="text-xl font-semibold tracking-tight text-ink">Zásilkovna</span>
        </Link>

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

/** Utility bar + sticky header, used on every page. */
export function SiteHeader() {
  return (
    <>
      <UtilityBar />
      <Header />
    </>
  );
}

/* ---------- Footer ---------- */
export function SiteFooter() {
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
            <form onSubmit={(e) => e.preventDefault()} className="flex gap-2">
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
