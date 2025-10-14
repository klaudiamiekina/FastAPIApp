# Zadanie rekrutacyjne \- FastAPI \+ integracja z OpenLibrary

Zadaniem było wykonanie rozwiązania w Pythonie z użyciem FastAPI, które udostępnia 3 endpointy.

1. ## Wymagania do uruchomienia aplikacji (Prerequisites)

Aby uruchomić aplikację, potrzebne są następujące narzędzia i środowiska:

* Docker i Docker Compose (wersje zalecane: Docker \>= 24.x, Compose \>= 2.x)  
* Python \>= 3.9  
* Internet do pobrania obrazów Dockerowych i zależności Pythona  
* (Opcjonalnie) Narzędzie do testowania endpointów, np. Postman lub interaktywnie Swagger UI

2. ## Jak uruchomić aplikację (Quick Start)

* Sklonuj repozytorium:  
  `git clone https://github.com/klaudiamiekina/FastAPIApp.git`  
  `cd \<nazwa\_sklonowanego\_folderu\>`  
* Uruchom docker desktop \- jeżeli nie korzystasz z Linuxa  
* Zbuduj i uruchom kontenery Dockerowe:  
  `docker-compose up \--build \-d`  
  * Kontener *db-1* \- uruchamia PostgreSQL (automatycznie, bez potrzeby lokalnej instalacji)  
  * Kontener *web-1* \- uruchamia aplikację FastAPI  
* Sprawdzenie działania:  
  * API dostępne pod: http://localhost:8000  
  * Dokumentacja Swagger UI: http://localhost:8000/docs  
* Wyłączanie kontenerów (na koniec pracy z aplikacją):  
  `docker-compose down \-v`  
  * Usuwa również wolumeny, dzięki czemu baza danych jest resetowana.

3. ## Dokumentacja rozwiązania

Endpointy API:

* **GET /health**  
  Sprawdza status aplikacji i połączenia z zewnętrznym API OpenLibrary.  
  **Odpowiedź**: JSON zawierający informacje o statusie aplikacji i API, np.:  
  {  
      "app\_status": "ok",  
      "external\_api\_status": "ok"  
  }  
  * "app\_status": "ok" \- aplikacja działa poprawnie  
  * "external\_api\_status": "ok" \- połączenie z API OpenLibrary działa  
  * "external\_api\_status": "failed" \- połączenie z API OpenLibrary nie powiodło się

* **POST /books**  
  Pobiera listę książek dla autora podanego w request body:  
  * {  
        "author": "J.R.R. Tolkien"  
    }

  
  **Odpowiedź**: JSON informujący o operacji zapisu, np.:  
  {  
      "inserted\_books": 10,  
      "inserted\_authors": 1,  
      "duplicates\_count": 2,  
      "message": "2 books of requested author already exist in the database"  
  }

* **GET /books**  
  Pobiera listę książek z lokalnej bazy z opcjonalnym filtrowaniem:  
  * author \- filtr po autorze  
  * title \- filtr po tytule

  **Odpowiedź:** JSON zawierający listę książek spełniających kryteria filtrowania.

4. ## Uruchomienie testów

Aplikacja zawiera testy jednostkowe napisane z użyciem PyTest, które sprawdzają logikę biznesową (np. BookDataManager) oraz poprawność działania endpointów FastAPI.  
Uruchamianie testów w Dockerze:

1. Upewnij się, że kontener aplikacji jest uruchomiony lub zbudowany:  
   `docker-compose up \--build \-d`  
2. Uruchom testy:

`docker-compose exec web pytest \-v`

Testy zostaną uruchomione wewnątrz kontenera.

5. ## Struktura plików w projekcie:

RecruitmentTask/  
├── app/  
│   ├── [main.py](http://main.py) \# punkt startowy FastAPI  
│   ├── api/v1/ \# endpointy aplikacji  
│   ├── clients/ \# klient zewnętrznego API  
│   ├── core/ \# konfiguracja bazy i ustawienia  
│   ├── dependencies/ \# dependency injection  
│   ├── models/ \# modele danych i Pydantic schemas  
│   └── services/ \# logika biznesowa  
├── tests/ \# testy jednostkowe  
├── docker-compose.yml \# konfiguracja kontenerów  
├── Dockerfile \# obraz aplikacji  
└── requirements.txt \# zależności Pythona  

6. ## Known limitations / TODO:

* Aplikacja udostępnia jedynie API, frontend nie został zaimplementowany w tym zadaniu.  
* Brak mechanizmów autoryzacji i logowania użytkowników.
