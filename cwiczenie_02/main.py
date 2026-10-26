
from pathlib import Path

import requests

class DownloadError(Exception):
    pass

class NotFoundError(DownloadError):
    pass

class AccessDeniedError(DownloadError):
    pass

def pobierz_plik(url, nazwa_pliku="latest.txt"):

    response = requests.get(url, timeout=30)

    if response.status_code == 404:
        raise NotFoundError("Nie znaleziono pliku (HTTP 404)")

    if response.status_code == 403:
        raise AccessDeniedError("Brak dostępu do pliku (HTTP 403)")

    response.raise_for_status()

    sciezka = Path(__file__).resolve().parent / nazwa_pliku

    with open(sciezka, "wb") as plik:
        plik.write(response.content)

    print(f"Plik zapisany jako: {sciezka}")


def main():

    adresy = [
        "http://oleksandr-fedoruk.com/sggw/podyplomowe/404",
        "http://oleksandr-fedoruk.com/sggw/podyplomowe/403",
    ]

    for url in adresy:
        print(f"\nSprawdzanie adresu: {url}")

        try:
            pobierz_plik(url)

        except NotFoundError as error:
            print(f"Błąd 404: {error}")

        except AccessDeniedError as error:
            print(f"Błąd 403: {error}")

        except requests.RequestException as error:
            print(f"Inny błąd komunikacji HTTP: {error}")


if __name__ == "__main__":
    main()
