# Audyt źródeł GTFS dla kolei

Stan na **2026-09-09**, strefa `Europe/Warsaw`. Archiwa zostały pobrane
bezpośrednio z katalogu wydawcy. Ten dokument jest migawką źródła do
implementacji; aplikacja nie powinna zakładać, że identyfikatory wydawcy nigdy
się nie zmienią.

## Źródła i zakres

| Źródło | Adres | ZIP | Wersja feedu | Deklarowany zakres | Kursy | Czasy postojów | Punkty geometrii |
|---|---|---:|---|---|---:|---:|---:|
| `polish_trains` | `https://mkuran.pl/gtfs/polish_trains.zip` | 26 998 196 B | `2026-09-09T02:45:16.545656+02:00` | 2026-09-09–2026-10-09 | 24 404 | 453 287 | 1 463 845 |
| `wkd` | `https://mkuran.pl/gtfs/wkd.zip` | 501 213 B | `2026-08-22T09:08:14` | brak pól zakresu w `feed_info.txt` | 3 702 | 55 386 | 4 584 |

Oba źródła używają wyłącznie `calendar_dates.txt` (same wyjątki typu `1`),
bez `calendar.txt`. Daty wyjątków obejmują odpowiednio 2025-12-14–2026-10-24
i 2025-12-14–2026-12-12. Dla Polish Trains ważność do prezentacji użytkownikowi
należy brać z `feed_info.feed_start_date`/`feed_end_date`, nie ze skrajnych dat
historycznych wyjątków. WKD wymaga wyliczenia zakresu z aktywnych usług.

Polish Trains zawiera 13 agencji, 192 trasy, 12 048 rekordów przystanków i
1 133 B w `agency.txt`. WKD zawiera jedną agencję, 2 trasy i 60 przystanków.
W obu paczkach są `agency.txt`, `calendar_dates.txt`, `feed_info.txt`,
`routes.txt`, `stops.txt`, `trips.txt`, `stop_times.txt` i `shapes.txt`.
Polish Trains ma ponadto `attributions.txt` i `transfers.txt`, a WKD
`fare_attributes.txt`.

## Zweryfikowane mapowanie przewoźników

Mapowanie wykonywalne znajduje się w
`resources/public_transport/rail_gtfs_sources.py`. Kolejność tabeli jest
kolejnością docelową w interfejsie.

| Id aplikacji | Nazwa w interfejsie | Źródło | `agency_id` | Trasy | Kursy w pobranej paczce |
|---|---|---|---|---:|---:|
| `rail_pkp_intercity` | PKP Intercity | `polish_trains` | `IC` | 9 | 3 550 |
| `rail_polregio` | POLREGIO | `polish_trains` | `PR` | 27 | 7 624 |
| `rail_arriva` | Arriva RP | `polish_trains` | `AR` | 2 | 726 |
| `rail_kd` | Koleje Dolnośląskie | `polish_trains` | `KD` | 46 | 2 583 |
| `rail_kmal` | Koleje Małopolskie | `polish_trains` | `KML` | 13 | 932 |
| `rail_km` | Koleje Mazowieckie | `polish_trains` | `KM` | 40 | 2 288 |
| `rail_ks` | Koleje Śląskie | `polish_trains` | `KS` | 33 | 2 318 |
| `rail_kw` | Koleje Wielkopolskie | `polish_trains` | `KW` | 9 | 1 552 |
| `rail_lka` | Łódzka Kolej Aglomeracyjna | `polish_trains` | `LKA` | 4 | 738 |
| `rail_skm_tricity` | PKP SKM w Trójmieście | `polish_trains` | `SKMT` | 1 | 1 096 |
| `rail_regiojet` | RegioJet | `polish_trains` | `RJ` | 1 | 34 |
| `rail_leo_express` | Leo Express | `polish_trains` | `LEO` | 1 | 106 |
| `rail_skm_warsaw` | SKM Warszawa | `polish_trains` | `SKM` | 6 | 857 |
| `rail_wkd` | Warszawska Kolej Dojazdowa | `wkd` | `0` | 2 | 3 702 |

Liczby kursów dotyczą całej zawartości archiwum, a nie jednego dnia.
Nie mogą służyć jako deklaracja pełności oferty. RegioJet ma w tej migawce
postoje w Polsce i Czechach; Leo Express w Polsce, Czechach i Niemczech.
Dokumentacja wydawcy wprost ostrzega, że relacje międzynarodowe mogą być
częściowe lub mieć błędnie przypisaną agencję.

## Struktura istotna dla adaptera kolejowego

- `routes.route_type` ma wartości `2` (kolej) i `3` (ZKA). Polish Trains ma
  140 tras kolejowych i 52 autobusowe; WKD po jednej każdego typu.
- Numer widoczny dla pasażera jest w `trips.trip_short_name`. Polish Trains
  dodaje `plk_category_code`, `plk_train_number` i `plk_train_name`; nie należy
  zastępować nimi bezwarunkowo `trip_short_name`.
- `trip_headsign` zawiera kierunek. Jedna trasa przewoźnika ma wiele numerów
  pociągów i wariantów, więc kierunek nie jest identyfikatorem kursu.
- Polish Trains modeluje stacje przez `location_type=1`, a perony przez
  `parent_station` i `platform_code`: 3 122 stacje, 8 926 rekordów z rodzicem
  i 5 422 rekordy z kodem peronu. Identyczne współrzędne różnych peronów są
  zamierzone. WKD publikuje wyłącznie płaską listę przystanków bez peronów.
- Polish Trains ma również pola `platform` i `track` w `stop_times.txt`.
  Dokumentacja źródła zaznacza, że nie są to potwierdzone zmiany bieżące.
- Występują czasy większe lub równe `24:00:00` (11 681 rekordów Polish Trains,
  2 087 WKD). Do sortowania i obliczeń trzeba zachować liczbę sekund od
  początku dnia operacyjnego, zamiast sprowadzać ją od razu modulo 24 godzin.
- Polish Trains używa zakazów wsiadania (`pickup_type=1`, 2 168 rekordów) i
  wysiadania (`drop_off_type=1`, 12 rekordów). WKD pomija te kolumny, czyli
  stosuje wartości domyślne GTFS.
- Geometria jest dostępna, ale część kursów może nie mieć `shape_id`; adapter
  potrzebuje jawnego trybu geometrii zastępczej.

## Luki w obecnym `GtfsDatabase`

Obecny importer poprawnie izoluje rekordy przez `feed_id`, filtruje usługi bez
ładowania całego `stop_times.txt` do interfejsu, zachowuje `agency_id` tras,
`trip_short_name`, `trip_headsign`, `parent_station`, `platform_code`, czasy
rozszerzone, zakazy wsiadania/wysiadania oraz `shapes.txt`.

Przed adapterem kolejowym schemat wymaga rozszerzenia o:

1. agencje (`agency.txt`) i metadane źródła (`feed_info.txt`), w tym strefę,
   wersję i deklarowaną ważność;
2. `stops.location_type` oraz kolejowe pola dostępności, aby odróżnić stację,
   peron i fallback;
3. źródłowe pola `platform`/`track` z `stop_times.txt` oraz — po decyzji UI —
   rozszerzenia `plk_*` z kursów;
4. indeks obejmujący `routes(feed_id, agency_id)`, potrzebny do bezpiecznego
   filtrowania wspólnej bazy po przewoźniku.

## Autorstwo i warunki

- Katalog wydawcy: <https://mkuran.pl/gtfs/>.
- Polish Trains: dane rozkładowe PKP PLK na warunkach ponownego wykorzystania
  informacji sektora publicznego; część Kolei Mazowieckich ma osobne warunki.
  Bieżący `attributions.txt` wskazuje PKP PLK, Koleje Mazowieckie i autora
  konwersji GTFS, Mikołaja Kuranowskiego. Aplikacja powinna odczytywać ten plik
  z każdej wersji zamiast utrwalać datę autorstwa.
- WKD: katalog wydawcy oznacza rozkład jako CC0 1.0.
- Kod konwertera PolishTrainsGTFS jest na licencji MIT. Nie jest to licencja
  danych wynikowych. Jego ręcznie utrzymywana geometria jest opisana jako
  CC0 1.0.
- Trip Updates Polish Trains mają CC BY 4.0 oraz warunki PKP PLK i mogą być
  okresowo nieaktualne. To osobny kontrakt od statycznego ZIP-a.

Schemat `GtfsDatabase` został rozszerzony w wersji 4, a źródłowy cache buduje
jedną bazę `polish_trains` oraz osobną bazę `wkd`. Wspólne zadanie rozsyła
postęp wszystkim oczekującym, a anulowanie jednego oczekiwania nie zatrzymuje
budowy dla pozostałych. Cache zwraca jawny status brakującej daty, daty poza
zakresem, dnia bez usług i nieaktualnego feedu wraz z komunikatem PL/EN.
Etap 2 jest zakończony; następnym krokiem technicznym jest adapter kolejowy.
