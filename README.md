# MarkTrackAdd commentMore actions

## Descriere
MarkTrack este o aplicație web pentru gestionarea notelor, claselor și utilizatorilor (elevi, profesori, administratori) în mediul educațional. Oferă funcționalități pentru administrarea catalogului școlar online, cu accent pe securitate și ușurință în utilizare.

## Tehnologii folosite
- Frontend: Next.js, React, TypeScript, TailwindCSS
- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Containerizare: Docker, Docker Compose

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

### Folosește Docker Compose
1. Clonează repository-ul:

   ```sh
   git clone git@gitlab.dev.info.uvt.ro:didactic/2025/licenta/ir/licentacatalinraevschi2025.git

   ```
2. Pornește aplicația:


   ```sh
   docker compose up --build

   ```
