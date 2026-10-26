
from pathlib import Path

import requests


def pobierz_plik(url, nazwa_pliku="latest.txt"):
    response = requests.get(url, timeout=30)

    response.raise_for_status()

    sciezka = Path(__file__).resolve().parent / nazwa_pliku

    with open(sciezka, "wb") as plik:
        plik.write(response.content)

    print(f"Plik zapisany jako: {sciezka}")


def main():
    url = "https://oleksandr-fedoruk.com/sggw/podyplomowe/file"
    pobierz_plik(url)


if __name__ == "__main__":
    main()
