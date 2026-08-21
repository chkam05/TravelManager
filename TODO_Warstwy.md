# Warstwy

Kroki do wykonania by dodać własne warstwy do aplikacji:

- Dodanie przycisku "Tworzenie Warstwy" do menu głównego, pod przycisk "Tworzenie Trasy"
- Dodanie panelu edycji warstwy do (`/templates/panels/layer.html`):

Panel edycji warstwy powinen posiadać:

- Header z tytułem warstwy edytowanej (domyślnie "Nowa warstwa {N}"/"New layer {N}") i przyciskiem zamykania panelu
- Div z przyciskami (tytuł "Rysowanie"):
  - "Rysuj prostą" (tylko ikona lucide `pencil-line`)
  - "Rysuj trasę" (tylko ikona lucide `waypoints`)
  - "Rysuj obszar" (tylko ikona lucide `vector-square`)
  - Separator
  - "Podziel" (tylko ikona lucide `git-commit-horizontal`)
  - "Usuń" (tylko ikona lucide `map-pin-minus`)
- Div z narzędziami:
  - Grubość (punkt, linia) - inputbox z "px"
  - Kolor (kolor punktu linii) - wybór koloru przez dialog
  (Domyślnie te ustawienia będą działać na rysowane elementy, ale po zaznaczeniu elementu do edycji (punktu, prostej, krawędzi), będą zmieniać ich kolor, grubość)
- Lista elementów na danej warstwie, każdy element na warstwie powinien mieć przycisk "more" z ikoną 3 kropek, który otwiera contextMenu z opcjami:
  - "Zmień nazwę" - co zmienia label nazwy elementu na inputbox i obok pokazuje przycisk zapisu
  - "Usuń" - usuwający dany element z warstwy
- Div z przyciskami "Zapisz" i "Usuń" (chodzi tutaj o warstwę, zapisując pojawi się dialog z podaniem nazwy, a przy usuwaniu dialog z pytaniem, czy na pewno chce się usunąć warstwę).

Trzeba pamiętać też o dialogu przy zamykaniu panelu, jeżeli warstwa została zmodyfikowana, lub nie jest jeszcze zapisana. Ponowne naciśnięcie przycisku "Zapisz", jak warstwa została wczesniej zapisana, spowoduje jej nadpisanie.

Pamiętaj o modelu danych warstw w pythonie, które będa zapisywane w `settings_data_model.py -> custom_layers: List[CustomLayer]`

Rysowanie:

- Każdy z elementów będzie można rysować na mapie (jak na nowej warstwie).
- Każdy z elementów będzie mieć punkty, które można przeciągać.  
- Rysowanie linii będzie polegać na tym, że po włączeniu rysowania na mapie będzie się wstawiać punkt, a po jego dodaniu drugi punkt linii. Po dodaniu pierwszego punktu, musi się pokazać podgląd linii, poruszający się drugim końcem pod kursorem, gdzie się będzie chciało wstawić drugi punkt.
- Oczywiście można będzie potem zaznaczyć dodwolny punkt takiej linii, ponownie nacisnąć "Rysuj - Prosta", dzięki czemu zaznaczony punkt obecnej prostej, stanie się pierwszym punktem następnej prostej, a te dwie proste staną się jednym obiektem "Trasą".
- Rysowanie "Trasy ma polegać na tym", że po dodaniu drugiego punktu jak w przypadku "Prostej", będzie można dodawać kolejne punkty, aż do naciśnięcia przycisku "Zakończ rysowanie trasy" w panelu `/templates/panels/layer.html`, albo po kliknięciu przycisku ESC.
- Rysowanie "Obszaru" ma wyglądać podobnie do rysowania trasy, tylko ostatni punkt zawsze ma być punktem początkowym (zamknięty wielokąt), czyli można kliknąć pierwszy punkt by zamknąć obszar, albo zakończyć rysowanie by stworzyła się prosta od ostatniego dodanego punktu do pierwszego.

Zarządzanie warstwami:

- W panelu `/templates/panels/layer_details.html` powinien się dodatkowo pojawić groupBox "Custom Layers", gdzie będzie można zaznaczać i odznaczać warstwy by się pokazywały na mapie lub znikały z niej (takich warst nie można edytować ani klikać bo nie są w trybie edycji).
- W `/templates/views` należy dodać nowy widok `layers.html`, który będzie wyglądać jak `/templates/views/favourites_tags.html` tylko zamiast tagów ulubionych, będzie tam lista utworzonych warstw z przyciskami "Zmień nazwę", "Edytuj" i "Usuń"
