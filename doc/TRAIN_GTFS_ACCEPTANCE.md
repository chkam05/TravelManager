# Odbiór integracji kolejowego GTFS

Stan pomiarów: **2026-09-10**, Python 3.13.14, macOS arm64. Testowane archiwa
to pełne migawki opisane w `TRAIN_GTFS_AUDIT.md`. Pomiar można powtórzyć:

```bash
python3 scripts/benchmark_rail_gtfs.py \
  --polish-trains /tmp/travelmanager-polish-trains.zip \
  --wkd /tmp/travelmanager-wkd.zip
```

## Pierwszy pomiar i progi

| Parametr | Wynik | Próg odbioru |
|---|---:|---:|
| Pobranie Polish Trains (HTTPS) | 20,50 s | ≤ 45 s |
| Pobranie WKD (HTTPS) | 0,62 s | ≤ 5 s |
| Budowa Polish Trains | 7,33 s | ≤ 15 s |
| Budowa WKD | 0,47 s | ≤ 2 s |
| Baza Polish Trains | 147,03 MiB | ≤ 250 MiB |
| Baza WKD | 4,15 MiB | ≤ 10 MiB |
| Wyszukanie stacji IC (507 wyników) | 361,88 ms | ≤ 1 s |
| Odjazdy z przykładowego peronu (13 wyników) | 28,14 ms | ≤ 200 ms |
| Szczytowe RSS całego pomiaru | 108,56 MiB | ≤ 256 MiB |

Pomiar pobrania wykonano bezpośrednio z `mkuran.pl`; zależy on również od łącza
i chwilowego obciążenia serwera. Progi są celowo wyższe od pierwszego wyniku,
aby uwzględnić wolniejszy dysk, inne obciążenie systemu i umiarkowany wzrost źródła. Nie są deklaracją limitu
rozmiaru danych wydawcy; po istotnym wzroście feedu należy wykonać pomiar ponownie.

## Pokrycie automatyczne

- wszystkie 14 mapowań oraz osobne mapowania RegioJet i Leo Express;
- izolacja tras i kursów każdej agencji we wspólnej bazie;
- kolejność grup PL/EN i zachowanie dostawców miejskich;
- pojedyncza budowa Polish Trains dla wielu odbiorców i osobna baza WKD;
- kalendarze, wyjątki, godziny po północy, perony, numery pociągów,
  relacja międzynarodowa i geometria zastępcza;
- dokładne i zastępcze dopasowanie aktualizacji, odrzucanie niejednoznaczności,
  anulowania, pominięcia, wygasanie i awaria źródła;
- błędny ZIP, brak wymaganych plików, utrata sieci, atomowe zachowanie starej
  bazy, zmiana wersji feedu i odczyt miejskiego cache schematu 3;
- pobieranie w tle i ochrona przed spóźnioną odpowiedzią poprzedniego widoku.

## Odbiór ręczny — pozostały zakres

Przed oznaczeniem dwóch ostatnich punktów Etapu 6 należy w uruchomionej aplikacji:

1. dla każdego operatora porównać co najmniej kurs roboczy i weekendowy ze
   źródłem operatora; dodatkowo sprawdzić przejście przez północ;
2. przejść selektor, listę linii i stacji, rozkład, szczegóły kursu i mapę;
3. potwierdzić komunikaty opóźnienia, anulowania i wygaśnięcia danych;
4. potwierdzić, że kolej nie pokazuje aktualizacji rozkładu jako GPS oraz że
   peron z rozkładu nie jest opisany jako potwierdzona zmiana bieżąca.

Wyników ręcznych nie oznaczono jako wykonane, ponieważ wymagają oceny działającego
interfejsu i porównania z zewnętrznym rozkładem każdego przewoźnika.
