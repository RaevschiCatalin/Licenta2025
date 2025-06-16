# MarkTrack

## Descriere
MarkTrack este o aplicație web pentru gestionarea notelor, claselor și utilizatorilor (elevi, profesori, administratori) în mediul educațional. Oferă funcționalități pentru administrarea catalogului școlar online, cu accent pe securitate și ușurință în utilizare.

## Tehnologii folosite
- Frontend: Next.js, React, TypeScript, TailwindCSS
- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Containerizare: Docker, Docker Compose

## Clonează repository-ul:
   ```sh
   git clone git@gitlab.dev.info.uvt.ro:didactic/2025/licenta/ir/licentacatalinraevschi2025.git
   ```

## Configurare fișiere .env

### Frontend (în root-ul proiectului)
Creează un fișier `.env` cu următoarele câmpuri:
```
NEXT_PUBLIC_API_BASE_URL=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

### Backend (în `mark-track/backend/.env`)
Creează un fișier `.env` cu următoarele câmpuri:
```
SECRET_KEY=
DATABASE_URL=
```
## Instrucțiuni de rulare


## Generare certificate SSL self-signed

Pentru a activa HTTPS local, poți genera certificate SSL self-signed folosind comanda de mai jos. Fisierele generate trebuie plasate într-un director dedicat, de exemplu `mark-track/traefik/certs/`:

```sh
mkdir -p mark-track/traefik/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mark-track/traefik/certs/server.key -out mark-track/traefik/certs/server.crt -subj "/CN=localhost"
```

- `server.key` și `server.crt` vor fi folosite de proxy-ul Traefik sau serverul web pentru HTTPS local.
- Asigură-te că ai configurat corect Traefik sau serverul să folosească aceste fișiere.

### Folosește Docker Compose

## Pornește aplicația:
   ```sh
   docker compose up --build
   ```
