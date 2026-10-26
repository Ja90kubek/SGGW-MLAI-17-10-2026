
import csv
from pathlib import Path
from datetime import datetime
from time import perf_counter
from functools import wraps


def loguj_czas(funkcja):

    @wraps(funkcja)
    def wrapper(*args, **kwargs):

        start = datetime.now()
        start_pomiaru = perf_counter()

        print(f"Rozpoczecie: {start:%Y-%m-%d %H:%M:%S}")

        try:
            return funkcja(*args, **kwargs)

        finally:
            koniec = datetime.now()
            czas_wykonania = perf_counter() - start_pomiaru

            print(f"Zakonczenie: {koniec:%Y-%m-%d %H:%M:%S}")
            print(f"Czas wykonania: {czas_wykonania:.4f} s")

    return wrapper

class CSVETL:

    def __init__(self, plik_wejsciowy, folder_wynikowy):
        self.plik_wejsciowy = plik_wejsciowy
        self.folder_wynikowy = folder_wynikowy
        self.nietypowe_wiersze = 0

    def wczytaj_wiersze(self):

        with self.plik_wejsciowy.open(
            "r", encoding="utf-8-sig", newline=""
        ) as plik:

            czytnik = csv.reader(plik, delimiter=",")

            for nr_linii, wiersz in enumerate(czytnik, start=1):

                if wiersz:
                    yield nr_linii, [
                        pole.strip() for pole in wiersz
                    ]

    def przetworz_wiersze(self):

        for nr_linii, wiersz in self.wczytaj_wiersze():

            if len(wiersz) != 8:
                self.nietypowe_wiersze += 1

            numer = wiersz[0]

            brakujace = [
                indeks
                for indeks, wartosc in enumerate(wiersz)
                if indeks > 0 and wartosc == "-"
            ]

            liczby = [
                float(wartosc)
                for wartosc in wiersz[1:]
                if wartosc != "-"
            ]

            suma = sum(liczby)
            srednia = suma / len(liczby) if liczby else None

            yield numer, suma, srednia, brakujace

    @loguj_czas
    def zapisz_wyniki(self):

        self.folder_wynikowy.mkdir(
            parents=True, exist_ok=True
        )

        plik_wartosci = self.folder_wynikowy / "values.csv"
        plik_brakow = self.folder_wynikowy / "missing_values.csv"

        with (
            plik_wartosci.open(
                "w", encoding="utf-8", newline=""
            ) as wartosci,
            plik_brakow.open(
                "w", encoding="utf-8", newline=""
            ) as braki,
        ):

            zapis_wartosci = csv.writer(wartosci)
            zapis_brakow = csv.writer(braki)

            zapis_wartosci.writerow(
                ["numer_porządkowy", "suma", "średnia"]
            )

            zapis_brakow.writerow(
                ["numer_porządkowy", "indeksy_brakujących_kolumn"]
            )

            liczba_wierszy = 0

            for numer, suma, srednia, brakujace in self.przetworz_wiersze():

                zapis_wartosci.writerow([
                    numer,
                    f"{suma:.6f}",
                    f"{srednia:.6f}" if srednia is not None else ""
                ])

                zapis_brakow.writerow([
                    numer,
                    ";".join(map(str, brakujace))
                ])

                liczba_wierszy += 1

        print(f"Przetworzono wierszy: {liczba_wierszy}")
        print(f"Zapisano: {plik_wartosci}")
        print(f"Zapisano: {plik_brakow}")

        if self.nietypowe_wiersze:
            print(
                f"Uwaga: {self.nietypowe_wiersze} wierszy "
                "mialo inna liczbe kolumn niz 8."
            )

def main():

    folder_projektu = Path(__file__).resolve().parent.parent

    plik_wejsciowy = (
        folder_projektu / "cwiczenie_01" / "latest.txt"
    )

    folder_wynikowy = (
        folder_projektu / "cwiczenie_04"
    )

    if not plik_wejsciowy.is_file():
        print(f"Nie znaleziono pliku: {plik_wejsciowy}")
        return

    etl = CSVETL(plik_wejsciowy, folder_wynikowy)

    etl.zapisz_wyniki()

if __name__ == "__main__":
    main()
