import productNotebook from "@/assets/product-notebook.jpg";
import productPen from "@/assets/product-pen.jpg";
import productWatercolor from "@/assets/product-watercolor.jpg";
import productWashi from "@/assets/product-washi.jpg";

export type Product = {
  /** URL slug, used in /products/$id */
  id: string;
  img: string;
  badge?: string;
  badgeTone?: "brand" | "neutral";
  brand: string;
  name: string;
  rating: number;
  reviews: number;
  /** Display price, already formatted with currency */
  price: string;
  oldPrice?: string;
  category: string;
  /** Short marketing line shown on the detail page */
  tagline: string;
  /** Longer description paragraphs for the detail page */
  description: string[];
  /** Key specs / highlights */
  features: string[];
  inStock: boolean;
};

export const products: Product[] = [
  {
    id: "zapisnik-leuchtturm-medium-a5",
    img: productNotebook,
    badge: "NOVINKA",
    badgeTone: "neutral",
    brand: "Leuchtturm1917",
    name: "Zápisník Medium A5, tečkovaný",
    rating: 4.9,
    reviews: 12,
    price: "520 Kč",
    category: "Papírnictví",
    tagline: "Ikonický zápisník pro bullet journal i každodenní poznámky.",
    description: [
      "Zápisník Leuchtturm1917 Medium (A5) je oblíbenou volbou pro bullet journaling, plánování i běžné psaní. Tečkovaný rastr nechá vašim nápadům volnost a zároveň udrží řádky a náčrty v pořádku.",
      "Pevná vazba leží příjemně v ruce, kvalitní 80g/m² papír minimalizuje prosvítání a číslované stránky s předtištěným obsahem vám pomohou udržet přehled.",
    ],
    features: [
      "251 číslovaných stran, papír 80 g/m²",
      "Tečkovaný rastr 5 mm",
      "Dvě stužkové záložky a gumička",
      "Zadní kapsa na lístky a samolepky",
    ],
    inStock: true,
  },
  {
    id: "kaweco-sport-mint-kulickove",
    img: productPen,
    badge: "−15 %",
    badgeTone: "brand",
    brand: "Kaweco",
    name: "Sport Mint Edition, kuličkové pero",
    rating: 5.0,
    reviews: 8,
    price: "589 Kč",
    oldPrice: "690 Kč",
    category: "Papírnictví",
    tagline: "Kompaktní kapesní pero s nadčasovým designem.",
    description: [
      "Kaweco Sport v limitované mátové edici je malé, ale plnohodnotné pero, které se vejde do každé kapsy. Po nasazení víčka získá pohodlnou délku k psaní.",
      "Osmihranné tělo brání kutálení po stole a kovová kulička zajišťuje plynulou, sytou stopu na každém papíru.",
    ],
    features: [
      "Kompaktní kapesní formát",
      "Osmihranné tělo proti kutálení",
      "Mátová limitovaná edice",
      "Standardní náplň Kaweco",
    ],
    inStock: true,
  },
  {
    id: "schmincke-horadam-akvarel-12",
    img: productWatercolor,
    brand: "Schmincke",
    name: "Akvarelové barvy Horadam, 12 ks",
    rating: 4.8,
    reviews: 24,
    price: "1 450 Kč",
    category: "Výtvarné potřeby",
    tagline: "Profesionální akvarely s mimořádnou svítivostí.",
    description: [
      "Sada Schmincke Horadam obsahuje 12 jemně mletých akvarelových barev v kovové paletě. Vysoký podíl pigmentu zaručuje sytost a krásné rozpíjení.",
      "Barvy jsou vyráběny v Německu z kvalitních surovin a jsou ideální jak pro skicování v plenéru, tak pro náročnější ateliérovou práci.",
    ],
    features: [
      "12 pánviček v kovové paletě",
      "Vysoká světlostálost",
      "Jemně mleté pigmenty",
      "Vyrobeno v Německu",
    ],
    inStock: true,
  },
  {
    id: "mt-washi-pastel-4ks",
    img: productWashi,
    badge: "BESTSELLER",
    badgeTone: "neutral",
    brand: "MT",
    name: "Washi pásky – pastel set 4 ks",
    rating: 4.7,
    reviews: 42,
    price: "320 Kč",
    category: "Dárkové balení",
    tagline: "Jemné pastelové odstíny pro scrapbook i dárky.",
    description: [
      "Sada čtyř washi pásek MT v něžných pastelových tónech. Japonské papírové pásky se snadno trhají rukou, dobře drží a zároveň jdou bez stopy odlepit.",
      "Ideální na zdobení diáře, balení dárků, lepení vzkazů nebo na kreativní projekty s dětmi.",
    ],
    features: [
      "4 role, šířka 15 mm",
      "Japonský papír washi",
      "Snadno se trhá i odlepuje",
      "Pastelová barevná paleta",
    ],
    inStock: true,
  },
  {
    id: "moleskine-classic-l-linkovany",
    img: productNotebook,
    brand: "Moleskine",
    name: "Classic L, linkovaný zápisník",
    rating: 4.6,
    reviews: 31,
    price: "480 Kč",
    category: "Papírnictví",
    tagline: "Legendární zápisník pro každý nápad na cestách.",
    description: [
      "Moleskine Classic ve velikosti L je nadčasový společník pro psaní i skicování. Zaoblené rohy a tvrdé desky odolají každodennímu nošení v tašce.",
      "Krémový linkovaný papír je příjemný pod perem a expandující zadní kapsa pojme lístky i účtenky.",
    ],
    features: [
      "240 stran, linkovaný papír",
      "Tvrdé desky a gumička",
      "Stužková záložka",
      "Expandující zadní kapsa",
    ],
    inStock: true,
  },
  {
    id: "lamy-safari-plnici-pero",
    img: productPen,
    badge: "NOVINKA",
    badgeTone: "neutral",
    brand: "LAMY",
    name: "Safari, plnicí pero",
    rating: 4.9,
    reviews: 18,
    price: "720 Kč",
    category: "Papírnictví",
    tagline: "Ergonomický klasik pro pohodlné psaní.",
    description: [
      "LAMY Safari je ikonické plnicí pero s tvarovaným úchopem, který vede prsty do správné polohy. Robustní tělo z ABS plastu vydrží i náročnější používání.",
      "Pružný kovový klip a ocelový hrot dělají ze Safari skvělou volbu pro studenty i milovníky psaní rukou.",
    ],
    features: [
      "Ergonomický tvarovaný úchop",
      "Ocelový hrot (šíře M)",
      "Pružný kovový klip",
      "Možnost konvertoru i bombiček",
    ],
    inStock: true,
  },
  {
    id: "winsor-newton-cotman-24",
    img: productWatercolor,
    badge: "−10 %",
    badgeTone: "brand",
    brand: "Winsor & Newton",
    name: "Cotman akvarely, 24 ks",
    rating: 4.7,
    reviews: 27,
    price: "990 Kč",
    oldPrice: "1 100 Kč",
    category: "Výtvarné potřeby",
    tagline: "Spolehlivé studijní akvarely za skvělou cenu.",
    description: [
      "Cotman je studijní řada akvarelů od Winsor & Newton s vyváženým poměrem ceny a kvality. 24 půlpánviček pokryje celou základní paletu.",
      "Barvy se snadno rozpíjejí a míchají, takže jsou ideální pro začínající akvarelisty i pro skicování v terénu.",
    ],
    features: [
      "24 půlpánviček v praktické paletě",
      "Dobrá rozpustnost a míchání",
      "Vhodné pro začátečníky",
      "Integrovaná míchací plocha",
    ],
    inStock: true,
  },
  {
    id: "mt-washi-zlata-3ks",
    img: productWashi,
    brand: "MT",
    name: "Washi pásky – zlatá kolekce 3 ks",
    rating: 4.8,
    reviews: 15,
    price: "280 Kč",
    category: "Dárkové balení",
    tagline: "Metalické odstíny pro slavnostní dekorace.",
    description: [
      "Tři role washi pásek MT v elegantní zlaté kolekci. Jemný metalický lesk dodá svátečnímu balení i diáři luxusní nádech.",
      "Pásky se hodí na vánoční dekorace, svatební papírnictví nebo na zvýraznění důležitých dní v kalendáři.",
    ],
    features: [
      "3 role, šířka 15 mm",
      "Metalický zlatý lesk",
      "Japonský papír washi",
      "Snadno se trhá i odlepuje",
    ],
    inStock: true,
  },
  {
    id: "rhodia-goalbook-a5",
    img: productNotebook,
    badge: "BESTSELLER",
    badgeTone: "neutral",
    brand: "Rhodia",
    name: "Goalbook A5, tečkovaný",
    rating: 4.8,
    reviews: 22,
    price: "560 Kč",
    category: "Papírnictví",
    tagline: "Prémiový papír, který milují fanoušci pér.",
    description: [
      "Rhodia Goalbook je oblíbený mezi milovníky plnicích per díky hladkému papíru 90 g/m², který skvěle zvládá i sytější inkousty.",
      "Číslované tečkované stránky a měkká pružná vazba z něj dělají ideální deník na plánování a kreativní zápisky.",
    ],
    features: [
      "224 číslovaných stran, papír 90 g/m²",
      "Tečkovaný rastr",
      "Měkká pružná vazba",
      "Předtištěný obsah a stránkování",
    ],
    inStock: true,
  },
  {
    id: "pilot-g2-gelove-pero",
    img: productPen,
    brand: "Pilot",
    name: "G2 0,5 mm, gelové pero",
    rating: 4.5,
    reviews: 64,
    price: "89 Kč",
    category: "Kancelářské potřeby",
    tagline: "Plynulá gelová stopa pro každodenní psaní.",
    description: [
      "Pilot G2 je celosvětově oblíbené gelové pero s pohodlným pogumovaným úchopem a sytě černou stopou. Stisknutím tlačítka vysunete hrot.",
      "Vodě odolný gelový inkoust a hrot 0,5 mm zaručují přesné a čisté psaní do sešitů, diářů i dokumentů.",
    ],
    features: [
      "Gelový hrot 0,5 mm",
      "Pogumovaný úchop",
      "Výsuvný mechanismus",
      "Vyměnitelná náplň",
    ],
    inStock: true,
  },
  {
    id: "sennelier-akvarel-8",
    img: productWatercolor,
    brand: "Sennelier",
    name: "Akvarel set l'Aquarelle, 8 ks",
    rating: 4.9,
    reviews: 11,
    price: "1 290 Kč",
    category: "Výtvarné potřeby",
    tagline: "Medové akvarely milované umělci po celém světě.",
    description: [
      "Sennelier l'Aquarelle jsou prémiové francouzské akvarely vyráběné s přídavkem včelího medu, který barvám dodává jas a vláčnost.",
      "Sada 8 pánviček obsahuje vyvážený výběr odstínů pro krajinu i portrét a je oblíbená mezi profesionály.",
    ],
    features: [
      "8 pánviček s medovou recepturou",
      "Mimořádný jas a sytost",
      "Vysoká světlostálost",
      "Vyrobeno ve Francii",
    ],
    inStock: false,
  },
  {
    id: "mt-washi-vanocni-5ks",
    img: productWashi,
    badge: "NOVINKA",
    badgeTone: "neutral",
    brand: "MT",
    name: "Washi pásky – vánoční edice 5 ks",
    rating: 4.6,
    reviews: 9,
    price: "360 Kč",
    category: "Sezónní zboží",
    tagline: "Sváteční motivy pro vánoční balení a tvoření.",
    description: [
      "Pět rolí washi pásek MT s vánočními motivy — od jmelí přes vločky až po svátečně červené vzory. Skvělý základ pro adventní tvoření.",
      "Pásky oživí balení dárků, přáníčka i adventní kalendář a snadno se kombinují s ostatními kolekcemi MT.",
    ],
    features: [
      "5 rolí, šířka 15 mm",
      "Vánoční motivy a vzory",
      "Japonský papír washi",
      "Snadno se trhá i odlepuje",
    ],
    inStock: true,
  },
];

export function getProduct(id: string): Product | undefined {
  return products.find((p) => p.id === id);
}

/** Returns up to `count` products in the same category, excluding the given id. */
export function getRelatedProducts(id: string, count = 4): Product[] {
  const current = getProduct(id);
  if (!current) return products.slice(0, count);
  const sameCategory = products.filter(
    (p) => p.id !== id && p.category === current.category,
  );
  const fillers = products.filter(
    (p) => p.id !== id && p.category !== current.category,
  );
  return [...sameCategory, ...fillers].slice(0, count);
}
