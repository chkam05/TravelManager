# Mapy offline — plan integracji

## Założenia

- Rozwiązanie korzysta wyłącznie z Pythona, bibliotek instalowanych przez `pip` oraz lokalnych plików HTML, CSS i JavaScript.
- Nie wymaga Node.js, Dockera, Javy, Tilemakera ani zewnętrznego procesu renderującego.
- Dane źródłowe pochodzą z regionalnych wyciągów OpenStreetMap w formacie `.osm.pbf`, udostępnianych przez Geofabrik.
- Aplikacja nie pobiera hurtowo kafelków z `tile.openstreetmap.org`.
- Pierwszy etap trybu offline obejmuje podkład mapowy. Wyszukiwanie miejsc, routing, Overpass i notatki OSM nadal wymagają połączenia z internetem.
- Gotowe mapy są przechowywane jako lokalne bazy MBTiles zawierające kafelki wektorowe MVT.
- Obecne internetowe podkłady Leafleta pozostają dostępne i nie zmieniają swojego dotychczasowego działania.
- Podkład offline używa jednego standardowego jasnego stylu, podobnie jak obecny podkład OpenStreetMap, niezależnie od motywu interfejsu aplikacji.
- Każdy ukończony krok należy oznaczyć przez zmianę `[ ]` na `[X]`.

## Instrukcja użytkownika

### Pobieranie mapy

1. Otwórz **Ustawienia → Mapa → Mapy offline** i wybierz **Pobierz mapę**.
2. Wskaż kontynent, kraj oraz dostępny region. Podział odzwierciedla katalog
   Geofabrik, dlatego liczba poziomów i rodzaj regionów różnią się między krajami.
3. Poziomy x3–x10 są przygotowywane podczas instalacji. Poziomu danych nie
   wybiera się osobno dla każdego pobrania; maksymalne zbliżenie ustawia się
   globalnie w sekcji **Mapa → Mapy offline**.
4. Sprawdź rozmiar źródła, dostępny szacunek wyniku i ilość wolnego miejsca,
   a następnie rozpocznij pobieranie.

Po pobraniu pliku aplikacja lokalnie analizuje dane OSM, generuje kafelki
wektorowe, buduje MBTiles i sprawdza integralność pakietu. Te etapy mogą trwać
znacznie dłużej niż samo pobieranie. Dialog można pozostawić otwarty albo użyć
opcji **Pobieraj w tle**. Wskaźnik w rogu aplikacji pozwala ponownie otworzyć
postęp. Zamknięcie i ponowne uruchomienie aplikacji wznawia bezpieczny etap
niedokończonego zadania. Przycisk **Anuluj** zatrzymuje zadanie i usuwa pobrany
plik, plik `.part` oraz wszystkie dane robocze tej mapy.

### Używanie mapy

W **Ustawienia → Mapa → Mapy offline** dostępne są trzy tryby:

- **Preferuj mapę offline** — aplikacja wybiera najmniejszy zainstalowany pakiet,
  który obejmuje bieżący środek widoku.
- **Używaj offline tylko bez internetu** — podkład lokalny jest wybierany po
  utracie połączenia.
- **Zawsze używaj mapy internetowej** — automatyczne przełączanie jest wyłączone;
  mapę lokalną nadal można wskazać ręcznie w panelu warstw.

Podkład offline ma jeden standardowy jasny styl niezależny od jasnego lub
ciemnego motywu interfejsu. Wyjście poza granice pakietu powoduje wyświetlenie
ostrzeżenia. Brak pojedynczego kafelka jest traktowany jako pusty fragment mapy,
a nie błąd całego widoku.

Przy pierwszym otwarciu fragmentu na poziomie x11–x19 aplikacja wyszukuje
potrzebne obiekty w zachowanym lokalnym indeksie, generuje kafelek MVT i zapisuje
go w MBTiles. Następne otwarcie korzysta już z zapisanego kafelka, a sąsiednie
kafelki są przygotowywane w tle. Wolniejsze generowanie jest sygnalizowane
wskaźnikiem z postępem w lewym dolnym rogu mapy.

Przycisk z ikoną przekreślonego Wi-Fi w narzędziach mapy pozwala tymczasowo
testować lokalny podkład bez wyłączania internetu w systemie. W tym trybie
internetowy podkład nie jest wybierany, ale nie jest to globalna blokada sieci:
pozostałe funkcje aplikacji mogą nadal wykonywać żądania internetowe.

### Aktualizowanie i usuwanie

Zainstalowane pakiety znajdują się w **Ustawienia → Pamięć → Pobrane mapy
offline**. Dla każdej mapy można użyć akcji **Pokaż na mapie**,
**Aktualizuj** lub **Usuń**. Aktualizacja powstaje obok działającego pakietu;
dotychczasowa mapa pozostaje dostępna i jest zastępowana dopiero po pełnej
walidacji nowej bazy. Nieudana aktualizacja nie usuwa sprawnej wersji. Usunięcie
wymaga potwierdzenia i kasuje lokalny MBTiles, lecz nie usuwa innych danych
aplikacji.

### Rozmiar, czas i wymagania

Rozmiar gotowej mapy zależy od powierzchni i gęstości danych regionu. Wartość
w dialogu jest zgrubnym szacunkiem, a nie gwarancją. Na czas przetwarzania
potrzebne jest miejsce na pobrany PBF, dane
robocze, kafelki i końcowy MBTiles. Kontrola wstępna wymaga bezpiecznego zapasu
wynoszącego co najmniej około czterokrotności rozmiaru PBF; rzeczywiste zużycie
może być większe dla gęstych obszarów i wysokiego zoomu.

Wymagany jest 64-bitowy Python 3.10 lub nowszy oraz zależności z
`requirements.txt`. Generowanie intensywnie wykorzystuje procesor i dysk, ale
odbywa się partiami i ogranicza liczbę równoległych zadań. Dla dużych państw
zalecane jest pobieranie mniejszych podregionów. Komputer nie powinien być
wyłączany podczas atomowej instalacji; po zwykłym zamknięciu aplikacji zadanie
zostanie odzyskane przy następnym uruchomieniu.

### Ograniczenia pierwszej wersji

Tryb offline obejmuje wyłącznie podkład mapowy. Połączenia z internetem nadal
wymagają między innymi: wyszukiwanie i odwrotne wyszukiwanie miejsc, wyznaczanie
tras, dane Overpass, notatki i publiczne ślady GPS OpenStreetMap, aktualizacje
GTFS oraz dane bieżących pozycji pojazdów. Zainstalowana mapa nie jest nawigacją
offline i nie zawiera indeksu adresowego. Pobranie lub aktualizacja pakietu
również wymaga internetu.

## Dane, atrybucja i licencje

- Dane map pochodzą od współtwórców **OpenStreetMap** i są udostępniane na
  licencji [Open Data Commons Open Database License 1.0 (ODbL)](https://opendatacommons.org/licenses/odbl/1-0/).
  Informacje o prawach autorskich są dostępne na
  [openstreetmap.org/copyright](https://www.openstreetmap.org/copyright).
- Regionalne wyciągi `.osm.pbf` i katalog regionów dostarcza
  [Geofabrik](https://download.geofabrik.de/). Geofabrik nie jest twórcą danych
  OSM; przy korzystaniu z wyciągów nadal obowiązują warunki i atrybucja OSM.
- Napis **© OpenStreetMap contributors** jest zapisany w lokalnej konfiguracji
  renderera i w metadanych każdego MBTiles. Pozostaje widoczny w kontrolce
  atrybucji Leaflet również wtedy, gdy komputer nie ma połączenia z internetem.
- Lokalny renderer wykorzystuje dołączony **Leaflet.VectorGrid 1.3.0**. Jego
  informacja licencyjna znajduje się w
  `assets/vendor/leaflet-vectorgrid/LICENSE` (Beerware), a kod jest ładowany z
  aplikacji bez CDN.
- Przetwarzanie po stronie Python wykorzystuje **osmium/pyosmium**
  (BSD-2-Clause), **Shapely** (BSD-3-Clause), **mercantile** (BSD) oraz
  **mapbox-vector-tile** (MIT). Dokładne wersje używane przez projekt są
  przypięte w `requirements.txt`; pakiety zachowują własne informacje
  licencyjne dostarczane wraz z dystrybucją.

Jeżeli użytkownik publicznie rozpowszechnia zmodyfikowaną bazę danych powstałą z
danych OSM, powinien samodzielnie sprawdzić obowiązki wynikające z ODbL. Niniejszy
opis nie stanowi porady prawnej.

## Etapy realizacji

1. [X] Zdefiniowanie modeli map offline
   Dodać modele opisujące region dostępny do pobrania, zainstalowaną mapę oraz zadanie pobierania. Region powinien zawierać stabilny identyfikator Geofabrik, nazwę, identyfikator rodzica, kody ISO, adres PBF, rozmiar źródła, datę aktualizacji oraz granice. Zainstalowana mapa powinna przechowywać identyfikator, region, nazwę, ścieżkę względną do MBTiles, rozmiar, zakres współrzędnych, minimalny i maksymalny zoom, datę instalacji, datę danych źródłowych i wersję schematu. Zadanie powinno zapisywać etap, postęp, liczbę pobranych bajtów, stan anulowania oraz informacje potrzebne do wznowienia.

2. [X] Utworzenie bezpiecznej struktury katalogów map offline
   Dodać storage zarządzający katalogiem `offline_maps` wewnątrz katalogu danych TravelManagera. Struktura powinna zawierać `catalog.json`, `installed_maps.json`, `jobs.json`, katalogi `sources`, `work` i `maps`. Wszystkie operacje na ścieżkach muszą blokować wyjście poza katalog map, używać stabilnych identyfikatorów i zapisywać pliki JSON atomowo. Pliki tymczasowe powinny mieć rozszerzenie `.part`.

3. [X] Dodanie zależności do przetwarzania OpenStreetMap
   Dodać do `requirements.txt` biblioteki `osmium`, `shapely`, `mercantile` i `mapbox-vector-tile` w wersjach zgodnych ze wspieranymi wersjami Pythona i systemami docelowymi. Zweryfikować instalację na macOS ARM i Intel, Windows oraz Linux. Brak zależności powinien powodować czytelny komunikat diagnostyczny, a nie błąd uruchomienia całej aplikacji.

4. [X] Implementacja katalogu regionów Geofabrik
   Dodać usługę pobierającą stabilny indeks `index-v1-nogeom.json` Geofabrik. Na jego podstawie zbudować hierarchię kontynentów, krajów i dostępnych podregionów, wykorzystując pola `id`, `parent`, `name`, `iso3166-1:alpha2`, `iso3166-2` oraz `urls.pbf`. Nie tworzyć ręcznych plików dla każdego kraju. Ostatni poprawny katalog przechowywać lokalnie i udostępniać także bez internetu.

5. [X] Lokalizacja nazw krajów i regionów
   Zapewnić polskie i angielskie nazwy krajów na podstawie kodów ISO oraz zachować nazwy regionów dostarczane przez źródło, jeśli brak lokalnego tłumaczenia. Sortowanie powinno używać aktualnego języka aplikacji. Struktura interfejsu ma odzwierciedlać rzeczywistą hierarchię Geofabrik, ponieważ nie każdy kraj posiada taki sam poziom podziału administracyjnego.

6. [X] API katalogu map offline
   Dodać endpoint `GET /api/offline-maps/catalog`. Powinien zwracać zapisany katalog, datę jego aktualizacji i informację, czy pochodzi on z bieżącego pobrania, czy z cache. Dodać możliwość jawnego odświeżenia katalogu bez blokowania interfejsu. Błędy sieciowe nie mogą usuwać ostatniej poprawnej kopii.

7. [X] API i storage zainstalowanych map
   Dodać `GET /api/offline-maps`, `GET /api/offline-maps/<map_id>/metadata` oraz `DELETE /api/offline-maps/<map_id>`. Lista ma zwracać nazwę, region, rozmiar, datę instalacji i aktualizacji danych, zakres oraz poziomy zoom. Usuwanie musi wymagać prawidłowego identyfikatora, nie może kasować plików poza `offline_maps/maps` i ma odrzucać usunięcie mapy aktualnie przetwarzanej.

8. [X] Pobieranie plików OSM PBF
   Dodać usługę pobierania z obsługą `Range`, plików `.part`, anulowania, ponawiania prób i wznowienia po ponownym uruchomieniu aplikacji. Akceptować wyłącznie adres PBF pochodzący z zapisanego katalogu Geofabrik, aby uniknąć dowolnych żądań sieciowych. Zapisywać aktualny i całkowity rozmiar oraz prędkość pobierania. Używać identyfikowalnego `User-Agent` TravelManagera.

9. [X] Trwały menedżer zadań map offline
   Dodać zarządzanie zadaniami w tle dla etapów pobierania, analizy, generowania, optymalizacji i instalacji. Stan zapisywać po każdej istotnej zmianie. Po uruchomieniu aplikacji odnajdywać niedokończone zadania i bezpiecznie je wznawiać. Jednocześnie przetwarzać najwyżej jedną mapę, aby ograniczyć zużycie pamięci i procesora. Zamknięcie aplikacji zachowuje dane potrzebne do wznowienia, natomiast jawne anulowanie usuwa wszystkie pliki zadania.

10. [X] Definicja warstw i filtrowanie danych OSM
    Określić minimalny zestaw warstw wektorowych: woda, użytkowanie terenu, budynki, drogi, koleje, granice, miejscowości oraz podstawowe punkty POI. Dla każdej warstwy zdefiniować obsługiwane tagi OSM, minimalny zoom, priorytet, właściwości trafiające do MVT oraz reguły generalizacji. Pominąć dane, których renderer nie wykorzystuje, aby ograniczyć rozmiar MBTiles.

11. [X] Strumieniowy odczyt danych OSM
    Zaimplementować handlery `osmium` odczytujące węzły, drogi i wymagane relacje bez ładowania całego kraju do pamięci. Zapewnić magazyn lokalizacji węzłów odpowiedni dla dużych regionów. Normalizować geometrie, odrzucać nieprawidłowe elementy i raportować postęp możliwy do pokazania w interfejsie.

12. [X] Generator kafelków wektorowych MVT
    Dodać generator przypisujący geometrie do kafelków Web Mercator przy pomocy `mercantile`, przycinający i upraszczający je przez `shapely`, a następnie kodujący przez `mapbox-vector-tile`. Początkowy zakres powinien kończyć się na zoomie 14. Generator musi pracować partiami, ograniczać pamięć, reagować na anulowanie i nie pozostawiać gotowej mapy po błędzie.

13. [X] Budowanie i walidacja bazy MBTiles
    Utworzyć schemat MBTiles z tabelami `metadata` i `tiles`, indeksami oraz transakcjami partiami. Zapisywać kafelki zgodnie z układem TMS, metadane `bounds`, `center`, `minzoom`, `maxzoom`, `format`, wersję generatora i dane źródłowe. Po generowaniu wykonać walidację integralności, sprawdzić obecność kafelków, zoptymalizować bazę i dopiero wtedy atomowo przenieść ją do katalogu `maps`.

14. [X] Czyszczenie danych roboczych
    Po udanej instalacji usunąć źródłowy PBF, pliki `.part` oraz katalog roboczy zadania. Po błędzie pozostawić wyłącznie dane niezbędne do wznowienia. Dodać sprzątanie osieroconych katalogów roboczych i plików tymczasowych, które nie należą do aktywnego zadania.

15. [X] Lokalne API kafelków MVT
    Dodać endpoint `GET /api/offline-maps/<map_id>/tiles/<z>/<x>/<y>.pbf`. Endpoint ma walidować zakres współrzędnych i zoom, przeliczać XYZ na TMS, otwierać wyłącznie zarejestrowaną bazę MBTiles w trybie tylko do odczytu oraz zwracać poprawny typ MIME i kodowanie. Brak kafelka powinien zwracać przewidywalną odpowiedź bez generowania błędu serwera.

16. [X] Dodanie lokalnego renderera wektorowego do Leafleta
    Umieścić dystrybucyjne pliki Leaflet.VectorGrid w `assets/vendor`, bez zależności od CDN i Node.js podczas działania aplikacji. Dodać moduł `assets/js/layers/offline_map.js`, który tworzy warstwę `L.vectorGrid.protobuf` korzystającą z lokalnego API. Zachować wymagane przypisanie `© OpenStreetMap contributors`.

17. [X] Standardowy jasny styl mapy offline
    Zdefiniować jeden jasny styl MVT spójny ze standardowym podkładem OpenStreetMap. Kolory dróg, wody, budynków, kolei, granic, terenów i punktów powinny zachowywać czytelność niezależnie od jasnego lub ciemnego motywu interfejsu. Nie dodawać osobnego przełącznika motywu podkładu mapowego.

18. [X] Integracja map offline z istniejącym widokiem mapy
    Dodać lokalne mapy do mechanizmu warstw bazowych bez zmiany działania OpenStreetMap, CyclOSM i Humanitarian. Zapewnić przełączanie między źródłami, zachowanie kolejności warstw i poprawną obsługę mapy przy zmianie widoku. Po wyjściu poza zasięg pakietu pokazać czytelny stan braku lokalnych danych.

19. [X] Automatyczny wybór mapy offline
    Dodać ustawienia: „Preferuj mapę offline”, „Używaj offline tylko bez internetu” i „Zawsze używaj mapy internetowej”. Na podstawie granic zainstalowanych pakietów wybierać najmniejszą mapę zawierającą aktualny środek widoku. Nie przełączać warstwy podczas każdego przesunięcia, jeśli bieżący pakiet nadal obejmuje widok.

20. [X] Sekcja „Mapy offline” w zakładce „Mapa”
    Dodać sekcję zgodną wizualnie z pozostałymi ustawieniami. Umieścić w niej ustawienia automatycznego wyboru źródła, informację o zakresie pierwszego etapu oraz przycisk „Pobierz mapę”. Wyjaśnić, że routing, wyszukiwanie i dane dodatkowe nadal mogą wymagać internetu.

21. [X] Dialog wyboru regionu
    Dodać dialog pozwalający wybrać kontynent, kraj i dostępny region. Pokazać źródło, datę danych, rozmiar pobierania i szacowany rozmiar wynikowy. Poziom szczegółowości pakietu nie jest wybierany podczas pobierania. Uniemożliwić rozpoczęcie drugiego zadania dla tej samej mapy i ostrzec przed niewystarczającą ilością wolnego miejsca.

22. [X] Dialog postępu pobierania i generowania mapy
    Dodać dialog pokazujący bieżący etap, opis operacji, postęp, rozmiar i ewentualną liczbę przetworzonych elementów lub kafelków. Zapewnić przyciski „Pobieraj w tle” i „Anuluj” z właściwymi odstępami. Ponowne otwarcie ustawień podczas aktywnego zadania powinno przywrócić dialog.

23. [X] Wskaźnik zadania działającego w tle
    Rozszerzyć istniejący mechanizm wskaźnika pobierania w tle tak, aby obsługiwał również mapy offline. Wskaźnik nie może kolidować z aktualizacją GTFS, ma obracać wyłącznie ikonę i po kliknięciu otwierać właściwy dialog. Powinien rozróżniać pobieranie danych, lokalne przygotowanie pakietu, anulowanie ze sprzątaniem oraz generowanie szczegółowych kafelków na żądanie.

24. [X] Lista map w „Pamięć”
    Dodać sekcję „Pobrane mapy” z tabelaryczną listą: nazwa, region, data aktualizacji, rozmiar i akcje. Dane mają być sortowane lokalnie według nazwy. Udostępnić „Pokaż na mapie”, „Aktualizuj” i „Usuń”. Usuwanie wymaga dialogu potwierdzenia, a po operacji lista i licznik zajętej pamięci muszą się odświeżyć.

25. [X] Aktualizacja zainstalowanej mapy
    Dodać `POST /api/offline-maps/<map_id>/update`. Aktualizacja ma budować nową bazę obok istniejącej, pozostawiając starą mapę dostępną podczas całej operacji. Dopiero po walidacji nowa baza atomowo zastępuje poprzednią. Nie usuwać sprawnej mapy, jeśli pobieranie lub generowanie aktualizacji zakończy się błędem.

26. [X] Obsługa braku miejsca i limitów zasobów
    Przed rozpoczęciem sprawdzać dostępne miejsce na dysku z zapasem na PBF, dane robocze i gotową bazę. Podczas generowania kontrolować wolne miejsce oraz umożliwić bezpieczne przerwanie. Ograniczyć liczbę równoległych zadań, wielkość kolejek geometrii i liczbę otwartych połączeń SQLite.

27. [X] Bezpieczeństwo i integralność pobierania
    Ograniczyć pobieranie do HTTPS i adresów zapisanych w katalogu źródłowym. Nie ufać nazwom plików ani identyfikatorom przesłanym przez klienta. Jeśli źródło udostępnia sumę kontrolną, zweryfikować ją przed przetwarzaniem. Nie zastępować istniejącej mapy plikiem, który nie przeszedł pełnej walidacji.

28. [X] Testy jednostkowe backendu
    Dodać testy modeli, katalogu, bezpiecznych ścieżek, zapisu atomowego, wznowienia pobierania, anulowania, recovery po restarcie, generatora małego fixture OSM, poprawności XYZ/TMS, odczytu MVT, instalacji, aktualizacji i usuwania. Testy nie mogą pobierać dużych danych z internetu i powinny korzystać z małych lokalnych fixture.

29. [X] Testy interfejsu i regresji
    Dodać testy JavaScript dla wyboru regionu, postępu, anulowania, pracy w tle, listy pamięci, przełączania warstw, zmiany motywu i braku kafelka. Zweryfikować, że dotychczasowe warstwy mapy, GTFS komunikacji miejskiej i kolei, edytor warstw, routing oraz ustawienia działają bez regresji.

30. [X] Dokumentacja użytkownika i licencje
    Opisać sposób pobierania, aktualizowania i usuwania map, przewidywane rozmiary, wymagania sprzętowe i ograniczenia pierwszego etapu offline. Dołączyć informacje o OpenStreetMap, ODbL, Geofabrik oraz użytych bibliotekach JavaScript i Python. Atrybucja OpenStreetMap musi pozostawać widoczna także bez połączenia z internetem.

31. [X] Hybrydowe generowanie szczegółowych kafelków na żądanie
    Przy instalacji generować wyłącznie bazowe poziomy do x10 i zachować obok MBTiles przestrzenny indeks obiektów. Dla x11–x19 generować tylko kafelki żądane przez bieżący widok, zapisywać je trwale w MBTiles i współdzielić wynik kolejnych żądań. Po wyświetleniu kafelka przygotowywać w tle również jego sąsiadów. Maksymalny poziom ustawiać globalnie w sekcji „Mapa”, a wolniejsze generowanie pokazywać wraz z rzeczywistym postępem we wskaźniku działającym w tle. Usunięcie mapy musi usuwać również indeks, a lista pamięci ma uwzględniać jego rozmiar oraz rosnący cache kafelków.

32. [X] Ponowne użycie zainstalowanych map podrzędnych
    Podczas instalowania kraju wykrywać zainstalowane regiony podrzędne o zgodnej lub nowszej dacie danych. Zasilać nimi indeks obiektów, deduplikując rekordy według typu i identyfikatora OSM oraz warstwy. Kopiować wyłącznie kompletne kafelki mieszczące się w całości w zakresie mapy podrzędnej, natomiast kafelki brakujące i graniczne generować ponownie. Po udanej instalacji proponować usunięcie mniejszych pakietów objętych nową mapą.

33. [ ] Test akceptacyjny kompletnego przepływu
    Przeprowadzić test na małym regionie: odświeżenie katalogu, wybór regionu, pobranie z możliwością przerwania i wznowienia, generowanie MBTiles, automatyczne przełączenie na lokalną mapę, restart aplikacji, aktualizacja oraz usunięcie. Potwierdzić działanie bez internetu po instalacji pakietu oraz brak prób pobierania kafelków z sieci w trybie offline.
