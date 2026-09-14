# Mapy offline — plan integracji

## Założenia

- Rozwiązanie korzysta wyłącznie z Pythona, bibliotek instalowanych przez `pip` oraz lokalnych plików HTML, CSS i JavaScript.
- Nie wymaga Node.js, Dockera, Javy, Tilemakera ani zewnętrznego procesu renderującego.
- Dane źródłowe pochodzą z regionalnych wyciągów OpenStreetMap w formacie `.osm.pbf`, udostępnianych przez Geofabrik.
- Aplikacja nie pobiera hurtowo kafelków z `tile.openstreetmap.org`.
- Pierwszy etap trybu offline obejmuje podkład mapowy. Wyszukiwanie miejsc, routing, Overpass i notatki OSM nadal wymagają połączenia z internetem.
- Gotowe mapy są przechowywane jako lokalne bazy MBTiles zawierające kafelki wektorowe MVT.
- Obecne internetowe podkłady Leafleta pozostają dostępne i nie zmieniają swojego dotychczasowego działania.
- Każdy ukończony krok należy oznaczyć przez zmianę `[ ]` na `[X]`.

## Etapy realizacji

1. [ ] Zdefiniowanie modeli map offline
   Dodać modele opisujące region dostępny do pobrania, zainstalowaną mapę oraz zadanie pobierania. Region powinien zawierać stabilny identyfikator Geofabrik, nazwę, identyfikator rodzica, kody ISO, adres PBF, rozmiar źródła, datę aktualizacji oraz granice. Zainstalowana mapa powinna przechowywać identyfikator, region, nazwę, ścieżkę względną do MBTiles, rozmiar, zakres współrzędnych, minimalny i maksymalny zoom, datę instalacji, datę danych źródłowych i wersję schematu. Zadanie powinno zapisywać etap, postęp, liczbę pobranych bajtów, stan anulowania oraz informacje potrzebne do wznowienia.

2. [ ] Utworzenie bezpiecznej struktury katalogów map offline
   Dodać storage zarządzający katalogiem `offline_maps` wewnątrz katalogu danych TravelManagera. Struktura powinna zawierać `catalog.json`, `installed_maps.json`, `jobs.json`, katalogi `sources`, `work` i `maps`. Wszystkie operacje na ścieżkach muszą blokować wyjście poza katalog map, używać stabilnych identyfikatorów i zapisywać pliki JSON atomowo. Pliki tymczasowe powinny mieć rozszerzenie `.part`.

3. [ ] Dodanie zależności do przetwarzania OpenStreetMap
   Dodać do `requirements.txt` biblioteki `osmium`, `shapely`, `mercantile` i `mapbox-vector-tile` w wersjach zgodnych ze wspieranymi wersjami Pythona i systemami docelowymi. Zweryfikować instalację na macOS ARM i Intel, Windows oraz Linux. Brak zależności powinien powodować czytelny komunikat diagnostyczny, a nie błąd uruchomienia całej aplikacji.

4. [ ] Implementacja katalogu regionów Geofabrik
   Dodać usługę pobierającą stabilny indeks `index-v1-nogeom.json` Geofabrik. Na jego podstawie zbudować hierarchię kontynentów, krajów i dostępnych podregionów, wykorzystując pola `id`, `parent`, `name`, `iso3166-1:alpha2`, `iso3166-2` oraz `urls.pbf`. Nie tworzyć ręcznych plików dla każdego kraju. Ostatni poprawny katalog przechowywać lokalnie i udostępniać także bez internetu.

5. [ ] Lokalizacja nazw krajów i regionów
   Zapewnić polskie i angielskie nazwy krajów na podstawie kodów ISO oraz zachować nazwy regionów dostarczane przez źródło, jeśli brak lokalnego tłumaczenia. Sortowanie powinno używać aktualnego języka aplikacji. Struktura interfejsu ma odzwierciedlać rzeczywistą hierarchię Geofabrik, ponieważ nie każdy kraj posiada taki sam poziom podziału administracyjnego.

6. [ ] API katalogu map offline
   Dodać endpoint `GET /api/offline-maps/catalog`. Powinien zwracać zapisany katalog, datę jego aktualizacji i informację, czy pochodzi on z bieżącego pobrania, czy z cache. Dodać możliwość jawnego odświeżenia katalogu bez blokowania interfejsu. Błędy sieciowe nie mogą usuwać ostatniej poprawnej kopii.

7. [ ] API i storage zainstalowanych map
   Dodać `GET /api/offline-maps`, `GET /api/offline-maps/<map_id>/metadata` oraz `DELETE /api/offline-maps/<map_id>`. Lista ma zwracać nazwę, region, rozmiar, datę instalacji i aktualizacji danych, zakres oraz poziomy zoom. Usuwanie musi wymagać prawidłowego identyfikatora, nie może kasować plików poza `offline_maps/maps` i ma odrzucać usunięcie mapy aktualnie przetwarzanej.

8. [ ] Pobieranie plików OSM PBF
   Dodać usługę pobierania z obsługą `Range`, plików `.part`, anulowania, ponawiania prób i wznowienia po ponownym uruchomieniu aplikacji. Akceptować wyłącznie adres PBF pochodzący z zapisanego katalogu Geofabrik, aby uniknąć dowolnych żądań sieciowych. Zapisywać aktualny i całkowity rozmiar oraz prędkość pobierania. Używać identyfikowalnego `User-Agent` TravelManagera.

9. [ ] Trwały menedżer zadań map offline
   Dodać zarządzanie zadaniami w tle dla etapów pobierania, analizy, generowania, optymalizacji i instalacji. Stan zapisywać po każdej istotnej zmianie. Po uruchomieniu aplikacji odnajdywać niedokończone zadania i bezpiecznie je wznawiać. Jednocześnie przetwarzać najwyżej jedną mapę, aby ograniczyć zużycie pamięci i procesora. Anulowanie powinno pozostawiać plik częściowy tylko wtedy, gdy może zostać później wznowiony.

10. [ ] Definicja warstw i filtrowanie danych OSM
    Określić minimalny zestaw warstw wektorowych: woda, użytkowanie terenu, budynki, drogi, koleje, granice, miejscowości oraz podstawowe punkty POI. Dla każdej warstwy zdefiniować obsługiwane tagi OSM, minimalny zoom, priorytet, właściwości trafiające do MVT oraz reguły generalizacji. Pominąć dane, których renderer nie wykorzystuje, aby ograniczyć rozmiar MBTiles.

11. [ ] Strumieniowy odczyt danych OSM
    Zaimplementować handlery `osmium` odczytujące węzły, drogi i wymagane relacje bez ładowania całego kraju do pamięci. Zapewnić magazyn lokalizacji węzłów odpowiedni dla dużych regionów. Normalizować geometrie, odrzucać nieprawidłowe elementy i raportować postęp możliwy do pokazania w interfejsie.

12. [ ] Generator kafelków wektorowych MVT
    Dodać generator przypisujący geometrie do kafelków Web Mercator przy pomocy `mercantile`, przycinający i upraszczający je przez `shapely`, a następnie kodujący przez `mapbox-vector-tile`. Początkowy zakres powinien kończyć się na zoomie 14. Generator musi pracować partiami, ograniczać pamięć, reagować na anulowanie i nie pozostawiać gotowej mapy po błędzie.

13. [ ] Budowanie i walidacja bazy MBTiles
    Utworzyć schemat MBTiles z tabelami `metadata` i `tiles`, indeksami oraz transakcjami partiami. Zapisywać kafelki zgodnie z układem TMS, metadane `bounds`, `center`, `minzoom`, `maxzoom`, `format`, wersję generatora i dane źródłowe. Po generowaniu wykonać walidację integralności, sprawdzić obecność kafelków, zoptymalizować bazę i dopiero wtedy atomowo przenieść ją do katalogu `maps`.

14. [ ] Czyszczenie danych roboczych
    Po udanej instalacji usunąć źródłowy PBF, pliki `.part` oraz katalog roboczy zadania. Po błędzie pozostawić wyłącznie dane niezbędne do wznowienia. Dodać sprzątanie osieroconych katalogów roboczych i plików tymczasowych, które nie należą do aktywnego zadania.

15. [ ] Lokalne API kafelków MVT
    Dodać endpoint `GET /api/offline-maps/<map_id>/tiles/<z>/<x>/<y>.pbf`. Endpoint ma walidować zakres współrzędnych i zoom, przeliczać XYZ na TMS, otwierać wyłącznie zarejestrowaną bazę MBTiles w trybie tylko do odczytu oraz zwracać poprawny typ MIME i kodowanie. Brak kafelka powinien zwracać przewidywalną odpowiedź bez generowania błędu serwera.

16. [ ] Dodanie lokalnego renderera wektorowego do Leafleta
    Umieścić dystrybucyjne pliki Leaflet.VectorGrid w `assets/vendor`, bez zależności od CDN i Node.js podczas działania aplikacji. Dodać moduł `assets/js/layers/offline_map.js`, który tworzy warstwę `L.vectorGrid.protobuf` korzystającą z lokalnego API. Zachować wymagane przypisanie `© OpenStreetMap contributors`.

17. [ ] Style jasnej i ciemnej mapy offline
    Zdefiniować style MVT dla obu motywów aplikacji. Kolory dróg, wody, budynków, kolei, granic, terenów i etykiet powinny pasować do istniejącego interfejsu oraz zachowywać czytelność. Zmiana motywu ma aktualizować styl lokalnej mapy bez ponownego generowania MBTiles.

18. [ ] Integracja map offline z istniejącym widokiem mapy
    Dodać lokalne mapy do mechanizmu warstw bazowych bez zmiany działania OpenStreetMap, CyclOSM i Humanitarian. Zapewnić przełączanie między źródłami, zachowanie kolejności warstw i poprawną obsługę mapy przy zmianie widoku. Po wyjściu poza zasięg pakietu pokazać czytelny stan braku lokalnych danych.

19. [ ] Automatyczny wybór mapy offline
    Dodać ustawienia: „Preferuj mapę offline”, „Używaj offline tylko bez internetu” i „Zawsze używaj mapy internetowej”. Na podstawie granic zainstalowanych pakietów wybierać najmniejszą mapę zawierającą aktualny środek widoku. Nie przełączać warstwy podczas każdego przesunięcia, jeśli bieżący pakiet nadal obejmuje widok.

20. [ ] Sekcja „Mapy offline” w zakładce „Mapa”
    Dodać sekcję zgodną wizualnie z pozostałymi ustawieniami. Umieścić w niej ustawienia automatycznego wyboru źródła, informację o zakresie pierwszego etapu oraz przycisk „Pobierz mapę”. Wyjaśnić, że routing, wyszukiwanie i dane dodatkowe nadal mogą wymagać internetu.

21. [ ] Dialog wyboru regionu
    Dodać dialog pozwalający wybrać kontynent, kraj i dostępny region. Pokazać źródło, datę danych, rozmiar pobierania, maksymalny zoom i szacowany rozmiar wynikowy. Uniemożliwić rozpoczęcie drugiego zadania dla tej samej mapy i ostrzec przed niewystarczającą ilością wolnego miejsca.

22. [ ] Dialog postępu pobierania i generowania mapy
    Dodać dialog pokazujący bieżący etap, opis operacji, postęp, rozmiar i ewentualną liczbę przetworzonych elementów lub kafelków. Zapewnić przyciski „Pobieraj w tle” i „Anuluj” z właściwymi odstępami. Ponowne otwarcie ustawień podczas aktywnego zadania powinno przywrócić dialog.

23. [ ] Wskaźnik zadania działającego w tle
    Rozszerzyć istniejący mechanizm wskaźnika pobierania w tle tak, aby obsługiwał również mapy offline. Wskaźnik nie może kolidować z aktualizacją GTFS, ma obracać wyłącznie ikonę i po kliknięciu otwierać właściwy dialog. Powinien rozróżniać pobieranie danych od lokalnego generowania kafelków.

24. [ ] Lista map w „Pamięć i Kopia Zapasowa”
    Dodać sekcję „Pobrane mapy” z tabelaryczną listą: nazwa, region, data aktualizacji, rozmiar i akcje. Dane mają być sortowane lokalnie według nazwy. Udostępnić „Pokaż na mapie”, „Aktualizuj” i „Usuń”. Usuwanie wymaga dialogu potwierdzenia, a po operacji lista i licznik zajętej pamięci muszą się odświeżyć.

25. [ ] Aktualizacja zainstalowanej mapy
    Dodać `POST /api/offline-maps/<map_id>/update`. Aktualizacja ma budować nową bazę obok istniejącej, pozostawiając starą mapę dostępną podczas całej operacji. Dopiero po walidacji nowa baza atomowo zastępuje poprzednią. Nie usuwać sprawnej mapy, jeśli pobieranie lub generowanie aktualizacji zakończy się błędem.

26. [ ] Obsługa braku miejsca i limitów zasobów
    Przed rozpoczęciem sprawdzać dostępne miejsce na dysku z zapasem na PBF, dane robocze i gotową bazę. Podczas generowania kontrolować wolne miejsce oraz umożliwić bezpieczne przerwanie. Ograniczyć liczbę równoległych zadań, wielkość kolejek geometrii i liczbę otwartych połączeń SQLite.

27. [ ] Bezpieczeństwo i integralność pobierania
    Ograniczyć pobieranie do HTTPS i adresów zapisanych w katalogu źródłowym. Nie ufać nazwom plików ani identyfikatorom przesłanym przez klienta. Jeśli źródło udostępnia sumę kontrolną, zweryfikować ją przed przetwarzaniem. Nie zastępować istniejącej mapy plikiem, który nie przeszedł pełnej walidacji.

28. [ ] Testy jednostkowe backendu
    Dodać testy modeli, katalogu, bezpiecznych ścieżek, zapisu atomowego, wznowienia pobierania, anulowania, recovery po restarcie, generatora małego fixture OSM, poprawności XYZ/TMS, odczytu MVT, instalacji, aktualizacji i usuwania. Testy nie mogą pobierać dużych danych z internetu i powinny korzystać z małych lokalnych fixture.

29. [ ] Testy interfejsu i regresji
    Dodać testy JavaScript dla wyboru regionu, postępu, anulowania, pracy w tle, listy pamięci, przełączania warstw, zmiany motywu i braku kafelka. Zweryfikować, że dotychczasowe warstwy mapy, GTFS komunikacji miejskiej i kolei, edytor warstw, routing oraz ustawienia działają bez regresji.

30. [ ] Dokumentacja użytkownika i licencje
    Opisać sposób pobierania, aktualizowania i usuwania map, przewidywane rozmiary, wymagania sprzętowe i ograniczenia pierwszego etapu offline. Dołączyć informacje o OpenStreetMap, ODbL, Geofabrik oraz użytych bibliotekach JavaScript i Python. Atrybucja OpenStreetMap musi pozostawać widoczna także bez połączenia z internetem.

31. [ ] Test akceptacyjny kompletnego przepływu
    Przeprowadzić test na małym regionie: odświeżenie katalogu, wybór regionu, pobranie z możliwością przerwania i wznowienia, generowanie MBTiles, automatyczne przełączenie na lokalną mapę, restart aplikacji, aktualizacja oraz usunięcie. Potwierdzić działanie bez internetu po instalacji pakietu oraz brak prób pobierania kafelków z sieci w trybie offline.
