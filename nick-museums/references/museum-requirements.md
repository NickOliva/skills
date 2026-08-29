# Museum Discovery and Visit Planning

**Status:** Ready for review

**Updated:** 2026-08-28

**Recommended deliverable:** Hybrid requirements brief — a stable personal museum plan plus a reusable skill contract

> [!warning] Private preference
> Default public trip origin: **Mamaroneck, NY**. A more precise private origin may be stored in `private.local.md`; use it for local routing estimates only and never reproduce it in generated reports or share it externally.

## Intent

Create a museum workflow that knows Nick's tastes, finds worthwhile exhibitions and permanent-collection opportunities, and turns a free date or time window into a short, practical set of ranked choices. It should optionally use Nick's calendar to find viable windows, estimate the all-in cost of longer trips, and add an approved visit to the calendar. A separate Sunday automation will maintain a forward exhibition calendar. Both workflows will produce polished PDFs through Pandoc and Eisvogel.

The system should optimize for the art, not for the institution's label: a relevant representational or photography exhibition at a modern museum can qualify, while an abstract exhibition at a traditionally strong museum should not.

## Nick's art profile

### Strong interests

- Impressionism and Post-Impressionism, especially **Claude Monet, Paul Cézanne, and Gustave Caillebotte**.
- **J. M. W. Turner**, especially *The Fighting Temeraire*, and related British Romantic, atmospheric, and pre-Impressionist painting.
- Major European painting and recognized masters, including **Leonardo da Vinci** and **El Greco**.
- The **Hudson River School**; liked, though not as highly ranked as Impressionism.
- Chinese painting and handscrolls, especially **Northern Song landscape painting** and rare rotations or loans of famous scrolls.
- Photography with artistic or historical significance, including **Richard Avedon**, large-format work, landscape, and photojournalism.
- Some modern artists, to be learned individually rather than inferred from the word “modern.”

### Favorite work

- **Wen Zhengming, *Deep Snow in Mountain Passes* (關山積雪圖; also translated *Heavy Snow in the Mountain Passes*), 1532, Ming dynasty.** Handscroll, 25.3 × 445.2 cm; National Palace Museum, Taipei.
- Treat any verified display, loan, or focused exhibition involving this work as a top-priority, potentially fly-worthy opportunity. Do not assume it is on permanent display; confirm current on-view status.

### Negative preferences and guardrails

- Strongly avoid abstract, conceptual, avant-garde, and deliberately provocative work whose main value is interpretive rather than visual or technical.
- Do not recommend AI-generated photography or imagery.
- Religious subject matter is usually a negative, but not a categorical exclusion when the artist or work is otherwise a strong match—important for artists such as El Greco and Leonardo.
- Exclude commercial galleries by default. Major nonprofit photography institutions and museum-quality academic exhibition spaces may qualify.
- Do not reject an entire museum because it also shows contemporary or abstract art; assess the specific exhibition and currently displayed collection.

## Requirements

### R1 — Persistent preference and travel context

- **R1.1** The workflow must use the origin in `private.local.md` when present, otherwise **Mamaroneck, NY**, unless Nick supplies another starting point.
- **R1.2** Generated reports must identify the origin only as **Mamaroneck, NY**, never by street address.
- **R1.3** The workflow must apply the art profile, negative preferences, and priority hierarchy in this document.
- **R1.4** It must maintain an evolving list of explicitly stated favorite artists, schools, works, photographers, and exclusions without treating a one-time choice as a permanent preference.
- **R1.5** It must preserve uncertain attributions as uncertainties and update them when user-supplied or first-party evidence resolves them.

### R2 — Regional museum universe

- **R2.1** The normal regional universe is every qualifying institution within roughly the road distance from Mamaroneck to Boston—approximately a three-hour trip in favorable conditions, with an outer band for traffic or overnight practicality.
- **R2.2** The universe must include comprehensive museums, focused collections, university museums, artist sites with meaningful original work, and museum-quality nonprofit photography institutions.
- **R2.3** The universe must exclude commercial galleries and institutions devoted almost entirely to abstract or contemporary art, except when a specific exhibition is an unusually direct match.
- **R2.4** The registry below is the baseline, not a frozen list. The workflow must discover openings, closures, relocations, and newly relevant institutions.

### R3 — On-demand “I have time for a museum” workflow

- **R3.1** Trigger when Nick provides a date and available time window, with optional travel or overnight constraints.
- **R3.2** Search the complete regional registry plus any plausible exceptional venue for exhibitions and relevant permanent works actually available during that window.
- **R3.3** Verify against first-party sources: exhibition dates, opening hours, holiday closures, timed-entry availability, last admission, and whether fragile works or rotating collection objects are actually on view.
- **R3.4** Rank options using: preference fit, artistic significance or rarity, current availability, travel burden, usable gallery time, and confidence in the evidence.
- **R3.5** Return a decisive top three when possible, followed by at most three credible backups. Do not dump every technically possible venue into the recommendation.
- **R3.6** For each recommended option include why it fits, what to prioritize inside, address, realistic travel estimate, parking or transit guidance, hours, ticket/reservation requirements, suggested visit duration, and official links.
- **R3.7** If the trip reasonably requires an overnight stay, include a small set of well-located lodging choices. Do not book or purchase anything without explicit authorization.
- **R3.8** If no temporary exhibition clears the quality threshold, recommend the best relevant permanent-collection visit rather than lowering the taste threshold.
- **R3.9** Clearly label facts, estimates, and judgment. State when an object-level on-view status could not be confirmed.

### R4 — Weekly exhibition calendar

- **R4.1** Implement later as a separate scheduled task every **Sunday at 6:00 a.m. America/New_York**; do not make background monitoring a hidden behavior of the skill.
- **R4.2** Scan every institution in the regional registry and conduct a separate worldwide search for major exhibitions involving Nick's highest-priority artists, schools, works, Chinese handscrolls, and photography interests.
- **R4.3** Include every announced future regional exhibition that passes the normal fit threshold, with no arbitrary end-date horizon. Include worldwide exhibitions when they clear the higher threshold in R5, whether newly announced or already open.
- **R4.4** Organize exhibitions by calendar month, then by opening date. Mark newly announced, changed, opening soon, and closing soon items.
- **R4.5** Preserve the first-seen date and prior details so unchanged entries do not read as new each week.
- **R4.6** Include a compact source-audit appendix listing institutions checked, failures, and material uncertainties; this is how “complete” remains testable.
- **R4.7** Add a short **Worldwide highlights** section for major exhibitions that clear the higher threshold in R5. Its purpose is awareness and trip consideration, not an assumption that Nick will travel.
- **R4.8** Add a separate **Closing soon and reasonably accessible** section for high-fit exhibitions in the regional universe closing within the next 45 days. Sort by closing date and include the final date, remaining weekends, realistic travel burden, and ticket status.

### R5 — Worldwide major opportunities

- **R5.1** Search worldwide for major retrospectives or reunions involving favorite artists, rare displays of major Chinese scrolls, unusually important representational painting exhibitions, and significant photography.
- **R5.2** Prefer official museum announcements and lending-institution evidence; verify dates before recommending travel.
- **R5.3** Recommend air travel only for an exceptional match, not merely a good exhibition.
- **R5.4** Explain why the opportunity is rare, what key works are expected, the display period, and whether tickets are available or not yet released.
- **R5.5** Seed the worldwide watchlist with Turner, Monet, Cézanne, Caillebotte, Leonardo, El Greco, Wen Zhengming's *Deep Snow in Mountain Passes*, Northern Song and other canonical Chinese handscrolls, Richard Avedon, and major landscape or photojournalism exhibitions.
- **R5.6** Surface qualifying worldwide opportunities even when Nick has not expressed immediate travel intent; present them as options to consider and distinguish simple awareness from an actual travel recommendation.

### R6 — Output and storage

- **R6.1** Every on-demand recommendation and weekly digest must produce both Markdown source and a PDF.
- **R6.2** PDFs must be generated with **Pandoc and Eisvogel** and include working links, clear hierarchy, page numbers, generation date, and a concise sources section.
- **R6.3** Recommended storage is `Art/Museum Briefings/<YYYY>/`, with filenames beginning `YYYY-MM-DD` and distinguishing `museum-options` from `museum-calendar`.
- **R6.4** Reports must be useful on a phone and concise enough to choose quickly; detailed research belongs in an appendix.
- **R6.5** Never put the private street address into a PDF or ordinary report.

### R7 — Research quality

- **R7.1** Prefer official museum collection, exhibition, visit, and ticket pages. Use reputable secondary sources only to discover leads or resolve context.
- **R7.2** Treat hours, prices, parking, construction status, and exhibition schedules as volatile and recheck them for each recommendation.
- **R7.3** Distinguish a museum's ownership of a work from the work being on view.
- **R7.4** For photography, reject AI-generated imagery and favor authored photographic work of artistic, historical, landscape, portrait, or journalistic significance.
- **R7.5** Cite the supporting page for every recommended exhibition and every consequential logistical fact.

### R8 — Calendar integration

- **R8.1** With Nick's authorization, the workflow should read calendar availability so it can match real free windows to museum hours, travel time, timed-entry availability, and a safe travel buffer.
- **R8.2** Calendar access must remain provider-agnostic until implementation identifies the calendar system and available connector.
- **R8.3** After Nick chooses a visit, offer to create a calendar event containing the museum and exhibition, public location, opening and ticket times, official links, reservation details, and useful notes. Add separate travel blocks when the trip warrants them.
- **R8.4** Creating or changing a calendar event always requires Nick's explicit approval of the proposed event. Never alter or delete unrelated events.
- **R8.5** The Sunday digest may identify calendar-compatible opportunities and propose holds, but it must not automatically populate the calendar or create speculative events.
- **R8.6** Use the calendar's timezone and account for daylight-saving changes, museum-local time, travel duration, and last-admission rules.

### R9 — Travel-cost estimation and Expedia

- **R9.1** For distant regional, overnight, and fly-worthy options, provide a current all-in cost estimate when cost could affect the recommendation.
- **R9.2** Compare sensible modes when useful: driving (fuel, tolls, and parking), rail, and flying (fare, ground transport or rental car, lodging, and museum admission).
- **R9.3** Expedia is a preferred optional source for live flight and lodging estimates when usable through an authorized browser session or supported API. The workflow must not depend exclusively on Expedia and may use airline, rail, hotel, mapping, or other reputable first-party sources.
- **R9.4** State traveler-count, cabin, room, baggage, cancellation, tax, fee, and date assumptions. Show a realistic range and estimated trip total rather than false precision.
- **R9.5** Timestamp every price search and warn that availability and prices can change. Refresh estimates before a purchase decision.
- **R9.6** Cost research is read-only. Do not sign in, transmit personal information, hold inventory, or book flights, hotels, cars, trains, or tickets without separate explicit authorization.
- **R9.7** Use Mamaroneck or the appropriate airport/rail station as the public trip origin; never submit the private street address to a travel provider unless Nick specifically authorizes it for that transaction.

## Regional museum registry

This is the baseline search universe as of 2026-08-28. **Core** means the permanent collection is intrinsically aligned. **Selective** means monitor exhibitions and recommend only a direct match. **Outer** means comparable to or somewhat beyond the Boston trip and usually merits a long day or overnight.

### Westchester, Fairfield County, and nearby Lower Hudson

| Institution | Level | Why it belongs |
|---|---|---|
| [Bruce Museum](https://brucemuseum.org/) — Greenwich | Core | American Impressionism, nineteenth- and early-twentieth-century art, growing photography collection. |
| [Hudson River Museum](https://www.hrm.org/) — Yonkers | Core | Hudson River School and documentary photography. |
| [Katonah Museum of Art](https://www.katonahmuseum.org/) — Katonah | Selective | Non-collecting museum with rotating loan exhibitions. |
| [Neuberger Museum of Art](https://www.purchase.edu/neuberger-museum-of-art/) — Purchase | Selective | Modern/contemporary emphasis; recommend only representational or photography matches. |
| [Fairfield University Art Museum](https://www.fairfield.edu/museum/) — Fairfield | Core | Kress Renaissance/Baroque paintings, American and European art, photography, and rotating exhibitions. |
| [Edward Hopper House Museum](https://www.edwardhopperhouse.org/) — Nyack | Core | Focused artist site and exhibition program devoted to Hopper and related American art. |

### New York City

| Institution | Level | Why it belongs |
|---|---|---|
| [The Metropolitan Museum of Art](https://www.metmuseum.org/) | Core | Primary benchmark: European masters, Impressionism, American art, Asian painting, photography. |
| [The Frick Collection](https://www.frick.org/) | Core | Concentrated Old Masters and nineteenth-century European painting. |
| [The Morgan Library & Museum](https://www.themorgan.org/) | Core | Old Master drawings, manuscripts, paintings, and focused loan exhibitions. |
| [Hispanic Society Museum & Library](https://hispanicsociety.org/) | Core | Spanish masters including El Greco, Velázquez, Goya, and Sorolla; verify gallery availability during renovation phases. |
| [Neue Galerie New York](https://www.neuegalerie.org/) | Core | German and Austrian art, especially representational early modernism. |
| [Brooklyn Museum](https://www.brooklynmuseum.org/) | Core | American and European paintings plus photography and strong rotating exhibitions. |
| [International Center of Photography](https://www.icp.org/) | Core | Dedicated photography museum; particularly relevant to historical, fashion, documentary, and journalistic work. |
| [The New York Historical](https://www.nyhistory.org/) | Core | American painting, Hudson River material, and historical photography. |
| [Asia Society Museum](https://asiasociety.org/new-york/museum) | Core | Traditional through modern Asian loan exhibitions; important for Chinese painting rotations. |
| [Japan Society Gallery](https://japansociety.org/gallery/) | Core | Museum-quality Japanese painting, prints, photography, and historical material. |
| [Nicholas Roerich Museum](https://www.roerich.org/) | Core | Small focused collection of representational, spiritual, and mountain landscapes. |
| [American Folk Art Museum](https://folkartmuseum.org/) | Selective | Representational and self-taught American work; fit depends on exhibition. |
| [Museum of Modern Art](https://www.moma.org/) | Selective | Search for strong representational modernists and major photography; filter abstract/conceptual shows. |
| [Whitney Museum of American Art](https://whitney.org/) | Selective | Search for Hopper, representational American art, and photography; do not recommend by default. |
| [Solomon R. Guggenheim Museum](https://www.guggenheim.org/) | Selective | Consider only specific artist or representational exhibitions. |
| [Museum of the City of New York](https://www.mcny.org/) | Selective | Historical and documentary photography can be a direct match. |
| [The Met Cloisters](https://www.metmuseum.org/plan-your-visit/met-cloisters) | Selective | High-quality medieval art, but religious emphasis lowers priority. |
| [Society of Illustrators](https://societyillustrators.org/) | Selective | Nonprofit museum-quality illustration exhibitions; an exception to the general gallery exclusion. |
| [Fotografiska New York](https://newyork.fotografiska.com/en/thank-you) | Inactive watch | Its New York physical location is closed; monitor only for an official reopening announcement. |

### Long Island

| Institution | Level | Why it belongs |
|---|---|---|
| [The Heckscher Museum of Art](https://www.heckscher.org/) — Huntington | Core | American landscape and representational art with rotating collection displays. |
| [Nassau County Museum of Art](https://www.nassaumuseum.org/) — Roslyn Harbor | Core | Nineteenth- and twentieth-century American/European art and substantial loan exhibitions. |
| [Parrish Art Museum](https://parrishart.org/) — Water Mill | Selective | Strong Long Island and American artist context; exhibition fit varies. |

### Connecticut

| Institution | Level | Why it belongs |
|---|---|---|
| [Yale University Art Gallery](https://artgallery.yale.edu/) — New Haven | Core | Encyclopedic university collection with European, American, Asian, and photographic holdings. |
| [Yale Center for British Art](https://britishart.yale.edu/) — New Haven | Core | Largest British art collection outside the UK; Turner and British landscape are central strengths. |
| [Wadsworth Atheneum Museum of Art](https://www.thewadsworth.org/) — Hartford | Core | Hudson River School, French and American Impressionism, European Baroque, photography. |
| [Hill-Stead Museum](https://www.hillstead.org/) — Farmington | Core | Focused collection including Monet, Degas, Manet, Whistler, and Cassatt. |
| [New Britain Museum of American Art](https://nbmaa.org/) — New Britain | Core | Hudson River School, Ashcan, American Impressionism, illustration, realism, and photography. |
| [Florence Griswold Museum](https://florencegriswoldmuseum.org/) — Old Lyme | Core | American Impressionism and the Lyme Art Colony. |
| [Lyman Allyn Art Museum](https://www.lymanallyn.org/) — New London | Core | American and European painting plus rotating exhibitions. |
| [William Benton Museum of Art](https://benton.uconn.edu/) — Storrs | Selective | University museum with American/European art and photography; check specific rotations. |
| [Slater Memorial Museum](https://www.slatermuseum.org/) — Norwich | Selective | Academic collection with American, European, Asian, and historical holdings. |
| [Mattatuck Museum](https://www.mattmuseum.org/) — Waterbury | Selective | Connecticut art, American history, and rotating exhibitions. |

### Hudson Valley, Catskills, and Capital Region

| Institution | Level | Why it belongs |
|---|---|---|
| [Frances Lehman Loeb Art Center](https://www.vassar.edu/theloeb) — Poughkeepsie | Core | Hudson River School, European art, Asian art, and a 4,000-work photography collection. |
| [Center for Photography at Woodstock](https://www.cpw.org/) — Kingston | Core | Nonprofit photography institution; include as a photography-specific exception. |
| [Samuel Dorsky Museum of Art](https://www.newpaltz.edu/museum/) — New Paltz | Selective | Regional, American, and international exhibitions; fit varies. |
| [Woodstock Artists Association & Museum](https://www.woodstockart.org/) — Woodstock | Selective | Historic regional collection and changing exhibitions; noncommercial exception. |
| [Thomas Cole National Historic Site](https://thomascole.org/) — Catskill | Core | Cole, original paintings, and Hudson River School context. |
| [Olana State Historic Site](https://olana.org/) — Hudson | Core | Frederic Edwin Church paintings, studies, photography, archives, house, and landscape. |
| [Albany Institute of History & Art](https://www.albanyinstitute.org/) — Albany | Core | Permanent Hudson River School installation and regional historical art. |
| [The Hyde Collection](https://www.hydecollection.org/) — Glens Falls | Core | Old Masters including El Greco, Botticelli, Rembrandt, and Rubens, plus American painting. |
| [Arkell Museum](https://www.arkellmuseum.org/) — Canajoharie | Core | Winslow Homer, American painting, and illustration. |
| [Fenimore Art Museum](https://fenimoreartmuseum.org/) — Cooperstown | Outer/Core | American masterworks, folk art, and the history of photography. Seasonal schedule matters. |
| [Munson Museum of Art](https://www.munson.art/) — Utica | Outer/Core | Hudson River School, American realism and modernism, works on paper, and photography. |

### New Jersey

| Institution | Level | Why it belongs |
|---|---|---|
| [The Newark Museum of Art](https://newarkmuseumart.org/) — Newark | Core | American art, Arts of Asia, photography, and broad temporary exhibitions. |
| [Montclair Art Museum](https://www.montclairartmuseum.org/) — Montclair | Core | American art, George Inness, landscape, and rotating collection displays. |
| [Princeton University Art Museum](https://artmuseum.princeton.edu/) — Princeton | Core | Reopened in its new building in October 2025; encyclopedic painting, Asian art, works on paper, and photography. |
| [Zimmerli Art Museum](https://zimmerli.rutgers.edu/) — New Brunswick | Core | American and European art, illustration, photography, and selective modern holdings. |
| [New Jersey State Museum Fine Art Collection](https://www.nj.gov/state/museum/) — Trenton | Selective | American and New Jersey art; evaluate current display and exhibition fit. |

### Eastern Pennsylvania, Philadelphia, and Delaware

| Institution | Level | Why it belongs |
|---|---|---|
| [Allentown Art Museum](https://www.allentownartmuseum.org/) — Allentown | Core | Kress Renaissance/Baroque painting, American art, prints, and photography. |
| [Philadelphia Art Museum](https://www.philamuseum.org/) — Philadelphia | Core | European masters, Impressionism/Post-Impressionism, American and Asian art, photography. |
| [Barnes Foundation](https://www.barnesfoundation.org/) — Philadelphia | Core | Exceptional Renoir, Cézanne, Matisse, Van Gogh, and other Impressionist/Post-Impressionist holdings. |
| [Pennsylvania Academy of the Fine Arts](https://www.pafa.org/museum) — Philadelphia | Core | American painting and works on paper; Historic Landmark Building reopened in 2026. |
| [Woodmere Art Museum](https://woodmeremuseum.org/) — Philadelphia | Core | Deep collection of Philadelphia-area American art. |
| [La Salle University Art Museum](https://www.lasalle.edu/museum/) — Philadelphia | Selective | University collection of European and American art; verify public hours. |
| [TILT Institute for the Contemporary Image](https://tiltinstitute.org/) — Philadelphia | Selective/Core photography | Nonprofit photography institution; recommend historical, authored, or otherwise direct matches. |
| [Michener Art Museum](https://michenerartmuseum.org/) — Doylestown | Core | World-class Pennsylvania Impressionism and touring exhibitions. |
| [Brandywine Museum of Art](https://www.brandywine.org/museum) — Chadds Ford | Core | Wyeth family, American landscape, realism, still life, and illustration. |
| [Delaware Art Museum](https://delart.org/) — Wilmington | Core | Pre-Raphaelites, American painting, Howard Pyle, and illustration. |
| [Reading Public Museum](https://www.readingpublicmuseum.org/) — Reading | Selective | Mixed museum with European and American art; recommend when exhibitions or displays fit. |
| [Biggs Museum of American Art](https://www.biggsmuseum.org/) — Dover | Outer/Core | American fine and decorative art; requires a longer trip. |
| [Palmer Museum of Art](https://palmermuseum.psu.edu/) — State College | Outer/Core | Major academic collection of American/European painting, Asian art, and photography; beyond the normal same-day radius. |

### Berkshires, western and central Massachusetts

| Institution | Level | Why it belongs |
|---|---|---|
| [Norman Rockwell Museum](https://www.nrm.org/) — Stockbridge | Core | Definitive Rockwell and American illustration collection. |
| [The Clark Art Institute](https://www.clarkart.edu/) — Williamstown | Core | European and American painting with major Impressionist strength. |
| [Williams College Museum of Art](https://artmuseum.williams.edu/) — Williamstown | Limited watch | Partially open with reduced installations while preparing for a projected fall 2027 new building. |
| [Berkshire Museum](https://berkshiremuseum.org/) — Pittsfield | Selective | Mixed art/science museum; evaluate specific exhibitions. |
| [Smith College Museum of Art](https://scma.smith.edu/) — Northampton | Core | Broad painting, works on paper, Asian art, and photography collection. |
| [Mount Holyoke College Art Museum](https://artmuseum.mtholyoke.edu/) — South Hadley | Core | Academic collection with European, American, Asian art, and photography. |
| [Mead Art Museum](https://www.amherst.edu/museums/mead) — Amherst | Core | Academic collection of American, European, Asian, and photographic work. |
| [D'Amour Museum of Fine Arts](https://springfieldmuseums.org/about/damour-museum-of-fine-arts/) — Springfield | Core | European and American paintings with Currier & Ives and regional strengths. |
| [Worcester Art Museum](https://www.worcesterart.org/) — Worcester | Core | American/European painting, Impressionism, Asian art, prints, and early photography collecting. |
| [Fitchburg Art Museum](https://fitchburgartmuseum.org/) — Fitchburg | Selective | Regional museum with American, European, and rotating exhibitions. |

### Rhode Island, Boston, North Shore, and southern New Hampshire

| Institution | Level | Why it belongs |
|---|---|---|
| [RISD Museum](https://risdmuseum.org/) — Providence | Core | Comprehensive collection with French Impressionism, American/European art, Asian art, and photography. |
| [Newport Art Museum](https://newportartmuseum.org/) — Newport | Core | American painting, Whistler/Homer context, marine art, and photography. |
| [Museum of Fine Arts, Boston](https://www.mfa.org/) | Core | Monet, Impressionism, European and American painting, Asian art, and photography. |
| [Isabella Stewart Gardner Museum](https://www.gardnermuseum.org/) — Boston | Core | Focused European, Asian, and American master collection in an intact historic setting. |
| [Harvard Art Museums](https://harvardartmuseums.org/) — Cambridge | Core | European painting, early Renaissance, nineteenth-century French art, Asian art, and photography. |
| [Davis Museum at Wellesley College](https://www.wellesley.edu/davismuseum) — Wellesley | Core | University collection spanning European, American, Asian, and photographic art. |
| [McMullen Museum of Art](https://www.bc.edu/sites/artmuseum/) — Boston College | Selective | Scholarly loan exhibitions; recommend by subject. |
| [Griffin Museum of Photography](https://griffinmuseum.org/) — Winchester | Core | New England's dedicated photography museum. |
| [Addison Gallery of American Art](https://addison.andover.edu/) — Andover | Core | Major American painting collection and more than 16,000 photographs. |
| [Peabody Essex Museum](https://www.pem.org/) — Salem | Core | American art, maritime painting, Asian material, and internationally significant photography. |
| [Cape Ann Museum](https://www.capeannmuseum.org/) — Gloucester | Core | Fitz Henry Lane, maritime and regional American painting, photography. |
| [New Bedford Whaling Museum](https://www.whalingmuseum.org/) — New Bedford | Selective | Maritime painting and historical photography; fit depends on display or exhibition. |
| [Currier Museum of Art](https://currier.org/) — Manchester, NH | Outer/Core | European and American painting, decorative arts, and photography. |
| [Hood Museum of Art](https://hoodmuseum.dartmouth.edu/) — Hanover, NH | Outer/Core | Broad university collection; farther than Boston but worthwhile for a direct exhibition match. |

### Southern outer ring

| Institution | Level | Why it belongs |
|---|---|---|
| [The Walters Art Museum](https://thewalters.org/) — Baltimore | Outer/Core | Old Masters, nineteenth-century European painting, manuscripts, and Asian art. |
| [Baltimore Museum of Art](https://artbma.org/) — Baltimore | Outer/Core | Cézanne, major Matisse holdings, European/American painting, Asian art, and photography. |

## Skill contract

### Working name and invocation examples

**Working name:** `museum-guide`

- “I have Saturday from 10 to 5. What museum should I visit?”
- “What is worth seeing within two hours next Friday?”
- “Plan a visit to the Barnes for October 12.”
- “Update my museum calendar.”
- “Is anything worth flying for this winter?”
- “Check my calendar for a museum day next month.”
- “What would it cost to see that exhibition in Chicago?”
- “Add the trip I chose to my calendar.”

### Inputs

- Required for on-demand ranking: date and available time window.
- Optional: starting-point override, maximum drive, transport mode, overnight willingness, companion needs, and a named artist/museum.
- Optional authorized integrations: calendar free/busy data and an Expedia browser session or travel-shopping API.
- Additional cost inputs when relevant: traveler count, preferred departure airports or rail stations, cabin, baggage, hotel standard, room count, and budget.
- Persistent context: art profile from this note and, when present, the private default origin from `private.local.md`.
- Current external context: official exhibition, collection, hours, ticket, mapping, parking, and lodging sources.

### Adaptive workflow and stopping condition

1. Interpret the available time and travel constraints; if authorized, use calendar free/busy data to identify real candidate windows. Ask at most one clarifying question only when the answer would change feasibility or price.
2. Search all plausible registry institutions and any newly discovered qualified venue.
3. Verify the strongest candidates with first-party pages and current logistical data.
4. Estimate all-in travel cost for candidates where cost could change the ranking.
5. Rank by fit, importance, feasibility, cost, and confidence.
6. Produce the concise choice document and its PDF. After Nick chooses, offer a fully drafted calendar event for approval.
7. Stop when Nick can make a decision without doing more research; calendar creation is a separate approved action.

### Important exclusions and authorization boundaries

- Do not buy tickets, book travel or lodging, join memberships, contact institutions, or publish/share reports without explicit authorization.
- Do not create, edit, or delete calendar events without explicit authorization for the specific event.
- Do not log into Expedia or another travel provider, submit traveler data, hold inventory, or begin a booking flow merely to obtain an estimate.
- Do not expose the private street address in searches when city/ZIP-level routing is sufficient, in reports, or in citations.
- Do not fabricate an object's on-view status, an exhibition announcement, or an attribution.
- Do not recommend AI-generated art or photography.

## Success evidence and behavioral tests

- **S1 — Local free day:** Given a Saturday window, the output offers a verified top three that can actually be visited, explains the ranking, and includes enough logistics to leave home.
- **S2 — Closed or mistimed candidate:** A perfect-fit exhibition outside the available hours is not presented as feasible; it may appear only as a clearly labeled future option.
- **S3 — Fragile scroll:** Collection ownership alone is insufficient. The report confirms the scroll is on view or explicitly says that display status is unverified.
- **S4 — Modern museum, good exhibit:** A strong Avedon or Caillebotte exhibition at a modern/contemporary institution is considered on its merits.
- **S5 — Traditional museum, bad fit:** An abstract exhibition at a core museum does not receive a recommendation merely because the museum is on the registry.
- **S6 — Weekly completeness:** The digest shows every registry institution was checked or identifies the check failure, groups matching announcements by month, distinguishes new from unchanged entries, and includes a separate closing-soon section for accessible exhibitions.
- **S7 — Worldwide watch:** A major retrospective, reunion, or canonical scroll rotation anywhere in the world appears as an option to consider even without a planned trip. A routine loan does not trigger a flight recommendation.
- **S8 — Privacy and production:** The PDF is produced with Pandoc/Eisvogel, contains citations and working links, and does not expose the street address.
- **S9 — Calendar-aware choice:** With authorized calendar access, a proposed visit fits an actual free window including travel buffers. No event is created until Nick approves the exact proposal.
- **S10 — Cost-aware trip:** A fly-worthy recommendation includes a timestamped, sourced range covering the material transport, lodging, local travel, and admission costs, with assumptions visible and no booking action taken.

## Decisions and rationale

- Use a **hybrid** brief: tastes and the museum universe are stable personal context; live exhibitions, hours, and routing must be researched at run time.
- Separate the on-demand skill from the Sunday automation so invocation behavior stays predictable.
- Rank specific exhibitions rather than whole institutions. This accommodates Nick's selective interest in modern art without admitting low-fit abstraction.
- Make nonprofit photography institutions an explicit exception to the gallery exclusion; otherwise important photography would be missed.
- Treat “complete” as an auditable registry sweep, not an unsupported claim that every cultural venue on the map was found.
- Keep calendar access provider-agnostic and separate availability reading from event creation; this preserves usefulness without granting broad write behavior.
- Treat Expedia as a preferred price source, not a hard dependency. Its direct APIs are partner products, while browser access and other first-party sources can still support read-only estimates.

## Risks and open items

- **Taste coverage:** The favorite-artist list is an initial seed, not the full list Nick expects to develop over time.
- **Volatility:** Museum schedules, closures, and displays change; the registry needs runtime verification and periodic maintenance.
- **PDF implementation:** The downstream skill must verify that Pandoc, Eisvogel, fonts, and PDF dependencies are available in its execution environment.
- **Calendar integration:** The calendar provider, target calendar, and preferred event/travel-block conventions remain implementation choices for Nick.
- **Expedia integration:** Expedia's direct travel APIs require partner access. Implementation must choose between an available connector, an authorized browser session, partner credentials, or a provider-agnostic fallback.

## Selected research anchors

- [The Met — European Paintings](https://www.metmuseum.org/departments/european-paintings-1250-1800)
- [Yale Center for British Art — Collections](https://britishart.yale.edu/collections-overview)
- [Bruce Museum — Art Collection](https://brucemuseum.org/the-collection/art/)
- [Hudson River Museum — Collection](https://www.hrm.org/collection/)
- [The Barnes Collection](https://www.barnesfoundation.org/whats-on/collection)
- [Worcester Art Museum — Collections](https://www.worcesterart.org/collection/)
- [Addison Gallery — Collection](https://addison.andover.edu/collection/about-the-collection/)
- [Peabody Essex Museum — Photography](https://www.pem.org/the-pem-collection/photography)
- [National Palace Museum — *Deep Snow in Mountain Passes*](https://digitalarchive.npm.gov.tw/Collection/Detail?dep=P&id=3674)
- [Expedia Group Developer Hub — API products](https://developers.expediagroup.com/docs/api)
- [Expedia Group — Rapid API setup](https://developers.expediagroup.com/rapid/setup)

## Recommended next step

Review this brief and correct or expand the preference list. After approval, use it as the input to a separate skill-creation session; create the Sunday automation only after the skill's output path and PDF pipeline are tested.
