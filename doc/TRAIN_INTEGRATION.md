# Integracja kolei z transportem publicznym

## Cel i zakres

Dodać wszystkich poniższych przewoźników do istniejącego panelu „Komunikacja miejska”, w osobnej grupie **„Koleje” umieszczonej jako pierwsza na liście**. Pozostałe grupy miejskie zachowują dotychczasową kolejność i działanie. Integracja obejmuje pobieranie rozkładów, stacje i perony, kursy, odjazdy, przebieg na mapie oraz — tam, gdzie źródło je udostępnia — aktualizacje przejazdów.

To integracja modułu transportu publicznego, niezależna od importu własnych warstw. Dokument jest planem implementacji; poniższe zadania nie są jeszcze wdrożone.

## Przewoźnicy i kolejność w grupie

W interfejsie używać nazwy **POLREGIO**, zamiast literówki „POLREGION”. RegioJet i Leo Express umieścić osobno: dokumentacja wspólnego źródła wymienia je jako odrębnych przewoźników. Właściwe identyfikatory `agency_id` trzeba odczytać z aktualnego pliku, a nie zgadywać na podstawie nazw.

| Kolejność | Nazwa w interfejsie | Proponowany stabilny identyfikator aplikacji | Źródło |
|---|---|---|---|
| 1 | PKP Intercity | `rail_pkp_intercity` | Polish Trains |
| 2 | POLREGIO | `rail_polregio` | Polish Trains |
| 3 | Arriva RP | `rail_arriva` | Polish Trains |
| 4 | Koleje Dolnośląskie | `rail_kd` | Polish Trains |
| 5 | Koleje Małopolskie | `rail_kmal` | Polish Trains |
| 6 | Koleje Mazowieckie | `rail_km` | Polish Trains |
| 7 | Koleje Śląskie | `rail_ks` | Polish Trains |
| 8 | Koleje Wielkopolskie | `rail_kw` | Polish Trains |
| 9 | Łódzka Kolej Aglomeracyjna | `rail_lka` | Polish Trains |
| 10 | PKP SKM w Trójmieście | `rail_skm_tricity` | Polish Trains |
| 11 | RegioJet | `rail_regiojet` | Polish Trains |
| 12 | Leo Express | `rail_leo_express` | Polish Trains |
| 13 | SKM Warszawa | `rail_skm_warsaw` | Polish Trains |
| 14 | Warszawska Kolej Dojazdowa | `rail_wkd` | Osobny GTFS WKD |

Identyfikatory aplikacji pozostają stałe mimo ewentualnych zmian identyfikatorów źródłowych. Brak kursów danego przewoźnika w aktualnym okresie nie może powodować przypisania mu kursów innej spółki.

## Źródła danych

Źródła sprawdzone podczas przygotowania planu:

- Rozkład zbiorczy: [polish_trains.zip](https://mkuran.pl/gtfs/polish_trains.zip).
- Aktualizacje zbiorcze: [GTFS-Realtime Trip Updates](https://mkuran.pl/gtfs/polish_trains/updates.pb); alternatywnie [JSON](https://mkuran.pl/gtfs/polish_trains/updates.json).
- WKD: [rozkład GTFS](https://mkuran.pl/gtfs/wkd.zip) i [GTFS-Realtime Trip Updates](https://mkuran.pl/gtfs/wkd.pb).

Wspólny zbiór jest konwersją danych PKP PLK publikowaną przez Mikołaja Kuranowskiego, a nie oficjalnym plikiem GTFS każdego operatora. Katalog źródła wskazuje zastąpienie dawnych osobnych plików Intercity, POLREGIO i Kolei Mazowieckich przez `polish_trains.zip`. Nie budować integracji na tych starych adresach. Zakres, aktualne adresy i warunki wykorzystania sprawdzać w [katalogu wydawcy](https://mkuran.pl/gtfs/).

Dokumentacja opisuje ograniczenia połączeń międzynarodowych, komunikacji zastępczej, stabilności identyfikatorów kursów i aktualizacji. Dane bieżące nie oznaczają pozycji GPS ani potwierdzonych zmian peronów. Szczegóły: [PolishTrainsGTFS](https://github.com/MKuranowski/PolishTrainsGTFS).

## Etap 1 — analiza aktualnych plików i mapowanie przewoźników

- [x] Pobrać oba archiwa i sprawdzić zakres dat, strukturę plików, rozmiar oraz liczbę kursów. Sam dostępny adres ZIP nie potwierdza aktualności rozkładu.
- [x] Odczytać `agency.txt`; przygotować jawne mapowanie wszystkich 14 pozycji na właściwe `agency_id` i źródło. Dopuścić kilka identyfikatorów jednej spółki, jeśli występują w danych.
- [x] Sprawdzić powiązania `routes.agency_id`, nazwy/numerację pociągów, `route_type`, `trip_short_name`, `trip_headsign`, kalendarze, `parent_station`, `platform_code`, geometrię i zasady wsiadania/wysiadania.
- [x] Zweryfikować osobne identyfikatory RegioJet i Leo Express oraz zakres ich połączeń. Nie deklarować pełnej oferty zagranicznej na podstawie obecności operatora w zbiorze.
- [x] Przygotować małe, reprezentatywne pliki testowe, w tym kurs przez północ, zmienny kalendarz i stację z kilkoma peronami.
- [x] Zapisać źródła, wymagane oznaczenia autorstwa i datę pobrania. Warunki danych odróżniać od licencji kodu konwertera.

**Wynik:** sprawdzona tabela identyfikatorów źródłowych i potwierdzony zakres danych każdego przewoźnika.

## Etap 2 — wspólne pobieranie i baza GTFS

Istniejący [GtfsDatabase](../core/gtfs_database.py) przechowuje m.in. `feed_id`, `agency_id`, typy tras, kursy, przystanki i geometrię. Wykorzystać tę bazę, rozszerzając ją o brakujące pola po audycie etapu 1.

- [x] Wprowadzić dwa źródła fizyczne: `polish_trains` i `wkd`. Trzynaście pozycji z pierwszego źródła współdzieli pobrane archiwum i bazę — nie pobierać całej Polski osobno dla każdej spółki.
- [x] Oddzielić identyfikator źródła danych od identyfikatora przewoźnika widocznego w interfejsie.
- [x] Obsłużyć wspólne trwające pobranie/budowanie bazy, postęp, timeout, ponowienie i anulowanie. Anulowanie jednego odbiorcy nie powinno przerywać pobierania potrzebnego pozostałym.
- [x] Budować nową bazę tymczasowo, sprawdzać poprawność i podmieniać ją atomowo. Błąd aktualizacji pozostawia ostatnią poprawną wersję.
- [x] Przechowywać metadane wersji i ważności rozkładu. Pokazywać nieaktualność lub brak danych dla wybranej daty zamiast pustej listy bez wyjaśnienia.
- [x] Zapewnić izolację identyfikatorów między dwoma źródłami, indeksy dla zapytań po przewoźniku/stacji/dacie i migrację wersji schematu, jeśli będzie potrzebna.
- [x] Zachować możliwość pracy na pobranych rozkładach bez sieci. Nie ładować całego `stop_times.txt` do pamięci interfejsu.

## Etap 3 — adapter kolejowy i modele

- [x] Dodać wspólny adapter kolejowy w `utils/public_transport/`, korzystający z istniejącego kontrolera transportu. Z [GzmGtfsRepository](../utils/public_transport/gzm_gtfs_repository.py) przejąć przydatne mechanizmy zapytań, ale nie miejskie założenia o numeracji i typach linii.
- [x] Każde zapytanie o linie, kursy, przystanki i odjazdy ograniczać do właściwego źródła oraz przewoźnika. Wspólna stacja nie oznacza wspólnej listy kursów wszystkich spółek.
- [x] Obsłużyć kolejowe wartości `route_type` występujące w danych, w tym rozszerzone kody, bez domyślnego oznaczania pociągów jako autobusów.
- [x] Rozdzielić linię/relację od konkretnego kursu. Pokazywać numer i nazwę pociągu, jeśli są dostępne; nie łączyć różnych pociągów tylko dlatego, że mają ten sam kierunek.
- [x] Dla kolei aglomeracyjnych zachować oznaczenia linii, a dla dalekobieżnych zapewnić czytelne relacje i numery pociągów bez tworzenia nieużytecznie długiej listy wariantów.
- [x] Uwzględniać datę kursowania, wyjątki kalendarza, strefę czasową źródła i godziny GTFS przekraczające `24:00:00`.
- [x] Grupować perony pod stacją, zachowując odrębne identyfikatory i numery peronów nawet przy identycznych współrzędnych.
- [x] Zachować odrębność przyjazdu i odjazdu oraz zakazy wsiadania/wysiadania. Brak peronu prezentować jako brak informacji.
- [x] Geometrię pobierać z `shapes.txt`. Przy jej braku stosować wyraźnie oznaczony schemat połączenia stacji, bez sugerowania dokładnego przebiegu torów.

## Etap 4 — grupa „Koleje” i rejestracja wszystkich pozycji

Punkty integracji: [rejestr przewoźników](../resources/public_transport/public_transport_providers.py), [kontroler](../controllers/public_transport_controller.py), [widok transportu](../assets/js/views/public_transport.js), szablony selektorów oraz tłumaczenia PL/EN.

- [x] Dodać stabilną kategorię kolei i nazwę „Koleje” / „Rail”. Obecne `options()` sortuje po regionie, a `options_by_region()` grupuje opcje — rozbudować je o priorytet grupy, zamiast polegać na alfabetycznej pozycji przetłumaczonej nazwy.
- [x] W każdym selektorze dostawcy panelu „Komunikacja miejska” pokazywać „Koleje” przed grupami miejskimi, z kolejnością z tabeli. Nie przypisywać przewoźników kolejowych wyłącznie do województw.
- [x] Zarejestrować wszystkie 14 pozycji, ich mapowania, źródła, opisy, ikony i oznaczenia autorstwa.
- [x] Zachować zapamiętywanie wybranego dostawcy i zgodność istniejących ustawień przewoźników miejskich.
- [x] Wyświetlać postęp aktualizacji wspólnego źródła dla dowolnego korzystającego z niego operatora. Nie przedstawiać wspólnego pobrania jako 13 niezależnych importów.
- [x] Dostosować nazwy i etykiety: „stacja”, „peron”, „pociąg”, numer kursu, relacja. Zachować wyszukiwanie i filtrowanie.
- [x] Sprawdzić duplikację SKM Warszawa między ofertą WTP i kolei. Oznaczać źródło i nie podwajać odjazdów w widokach agregujących źródła; nie scalać kursów na podstawie samej nazwy.

## Etap 5 — aktualizacje przejazdów i mapa

- [x] Podłączyć wspólne aktualizacje Polish Trains i osobne WKD; pobierać je raz na źródło, z uwzględnieniem zasad wydawcy, czasu odpowiedzi i ponawiania po błędach.
- [x] Dopasowywać aktualizacje do kursu i dnia operacyjnego. Dla Polish Trains przewidzieć kontrolowany mechanizm zastępczy oparty na przewoźniku, numerze i dacie, zgodnie z dokumentacją źródła; nie przypisywać niejednoznacznej aktualizacji.
- [x] Obsłużyć pola faktycznie występujące w źródle: opóźnienie, prognozowany odjazd/przyjazd, odwołanie czy pominięcie postoju. Nie obiecywać informacji, których źródło nie dostarcza.
- [x] Pokazywać czas ostatniej aktualizacji, nieaktualność danych i powrót do rozkładu planowego po wygaśnięciu danych bieżących. Nie przedstawiać starych danych jako aktualnych.
- [x] Nie wyświetlać aktualizacji rozkładu jako pozycji GPS. Ewentualny marker obliczony z rozkładu i opóźnienia oznaczyć „Pozycja szacowana”, a przy zbyt starych danych wyłączyć estymację.
- [x] Rozróżnić peron z rozkładu od potwierdzonej zmiany bieżącej. Wspólne źródło nie zapewnia bieżących zmian peronu/toru.
- [x] Zmiana operatora lub daty nie może pozwolić spóźnionej odpowiedzi zastąpić aktualnego widoku.
- [x] Zmiana logiki aktualizacji danych. Jeżeli są pobierane dane z widoku pełnoekranowego `templates/views/public_transport.html`, można przejść do innego widoku, a dane dalej będą się pobierać. W przypadku rozpoczęcia pobierania danych przez panel `templates/panels/public_transport`, powinno się też móc zamknąć to co się pojawiło, a dane dalej będą się pobierać w tle. Podczas takiego pobierania w tle, w dolnym lewym rogu strony, powinien się pokazać  mały dymek z informacją o trwającyym pobieraniu w tle. Po przejściu z powrotem do widoku `templates/views/public_transport.html`, lub otwarciu panelu `templates/panels/public_transport`, powinien z powrotem się pojawić widok pobierania.

## Etap 6 — testy i odbiór

- [x] Testy mapowania wszystkich 14 operatorów, w tym RegioJet i Leo Express osobno; brak obcych kursów w wynikach.
- [x] Test kolejności: grupa „Koleje” pierwsza, wewnętrzna kolejność zgodna z tabelą, brak regresji grup miejskich w PL/EN.
- [x] Test wspólnego pobrania/bazy: wybór dwóch operatorów nie tworzy dwóch kopii Polish Trains; WKD pozostaje niezależna.
- [x] Testy kalendarzy, godzin po północy, peronów, różnych numerów pociągów, tras międzynarodowych i braku geometrii.
- [x] Testy aktualizacji: prawidłowe i niejednoznaczne dopasowanie, odwołanie, stare dane, awaria źródła, zmiana wersji rozkładu i spóźniona odpowiedź.
- [x] Testy błędnego ZIP, brakujących plików, utraty sieci, zachowania poprzedniej bazy i migracji cache.
- [x] Pomiar czasu pobierania, budowy bazy, wyszukiwania stacji i odjazdów oraz zużycia pamięci dla pełnego zbioru kolejowego; ustalić akceptowalne wartości po pierwszym pomiarze.
- [ ] Ręcznie porównać kilka kursów każdego przewoźnika z jego rozkładem, w tym dzień roboczy, weekend i zmianę daty.
- [ ] W aplikacji sprawdzić selektor, listy, stacje, szczegóły pociągu, mapę, komunikaty aktualizacji oraz brak prezentowania estymacji jako GPS.

## Kolejność realizacji

1. Analiza źródeł i mapowania wszystkich przewoźników.
2. Wspólne pobieranie i baza dwóch źródeł.
3. Adapter kolejowy i pierwszy test całości na PKP Intercity, POLREGIO oraz WKD.
4. Rejestracja pozostałych operatorów i grupy „Koleje”; weryfikacja każdego mapowania.
5. Aktualizacje przejazdów, oznaczenia świeżości i prezentacja na mapie.
6. Pełne testy, pomiary i odbiór interfejsu.

Pilotaż na trzech przewoźnikach jest etapem technicznym, a nie ograniczeniem zakresu. Zadanie jest ukończone dopiero po obsłużeniu wszystkich pozycji z tabeli oraz opisaniu rzeczywistych ograniczeń źródeł.
