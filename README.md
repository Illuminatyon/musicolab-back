<div align="center">

```
███╗   ███╗██╗   ██╗███████╗██╗ ██████╗ ██████╗ ██╗      █████╗ ██████╗
████╗ ████║██║   ██║██╔════╝██║██╔════╝██╔═══██╗██║     ██╔══██╗██╔══██╗
██╔████╔██║██║   ██║███████╗██║██║     ██║   ██║██║     ███████║██████╔╝
██║╚██╔╝██║██║   ██║╚════██║██║██║     ██║   ██║██║     ██╔══██║██╔══██╗
██║ ╚═╝ ██║╚██████╔╝███████║██║╚██████╗╚██████╔╝███████╗██║  ██║██████╔╝
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝
```

**Backend — API REST Flask**

*SAE S4 — BUT Informatique 2025–2026 — IUT de Montreuil, Université Paris 8*

---

[![CI](https://github.com/DUT-Info-Montreuil/musicolab-back/actions/workflows/ci.yml/badge.svg)](https://github.com/DUT-Info-Montreuil/musicolab-back/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-API_REST-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-Hub-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/mq2vin/musicolab-back)
[![License](https://img.shields.io/badge/Licence-Éducatif-C8102E)](./LICENSE)

</div>

---

## 🎯 Rôle du backend

Ce dépôt contient l'**API REST Flask** qui alimente les modules nécessitant un traitement serveur dans l'application MusicoLab. Le frontend React communique avec cette API pour les opérations qui ne peuvent pas être réalisées côté navigateur.

```
┌─────────────────────────┐        HTTP / REST        ┌──────────────────┐
│   Frontend React        │ ─────────────────────────▶│  Backend Flask   │
│   musicolab-front       │ ◀─────────────────────────│  musicolab-back  │
│   :8081                 │        JSON               │  :5000           │
└─────────────────────────┘                           └──────────────────┘
```

---

## 📦 Modules couverts

### 🎹 Module 1 — Transposition MIDI

Traitement serveur d'un fichier MIDI uploadé par l'utilisateur.

- **`POST /midi/transpose`** — reçoit un fichier `.mid` et un intervalle en demi-tons, retourne le fichier transposé
- Traitement binaire du format MIDI (parsing des événements, décalage des hauteurs)
- Validation des paramètres (format fichier, plage d'intervalle)

### 🎵 Module 4 — Analyse fréquentielle

Analyse spectrale d'un fichier audio uploadé.

- **`POST /audio/analyse`** — reçoit un fichier audio (MP3, WAV, OGG…), retourne le spectre fréquentiel via FFT
- Identification des fréquences dominantes
- Réponse JSON avec les données spectrales prêtes à être visualisées côté frontend

---

## 🛠️ Stack technique

| Technologie | Rôle |
|---|---|
| **Python 3.11** | Langage principal |
| **Flask** | Framework API REST |
| **pytest** | Tests unitaires |
| **GitHub Actions** | CI (lint + tests + build Docker) |
| **Docker** | Conteneurisation et déploiement |

---

## 🚀 Lancement

### Avec Docker (recommandé)

L'image est publiée automatiquement sur Docker Hub à chaque push sur `main`.

```bash
# Lancer uniquement le backend
docker run -p 5000:5000 mq2vin/musicolab-back:main
```

Ou via le `docker-compose.yml` du dépôt frontend (recommandé pour lancer l'application complète) :

```bash
# Depuis musicolab-front/
docker compose up
```

→ Backend accessible sur **http://localhost:5000**

---

### En local (développement)

**Prérequis :** Python 3.11+

```bash
# 1. Cloner le dépôt
git clone https://github.com/DUT-Info-Montreuil/musicolab-back.git
cd musicolab-back

# 2. Créer un environnement virtuel
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer le serveur
flask run
# → http://localhost:5000
```

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Avec rapport de couverture
pytest --cov
```

Les tests couvrent :
- Transposition MIDI (Module 1) — parsing, décalage des hauteurs, cas limites
- Analyse fréquentielle (Module 4) — calcul FFT, extraction des pics

La CI GitHub Actions exécute automatiquement `pytest` sur chaque push et pull request.

---

## ⚙️ CI / CD

```
Push sur main
      ↓
GitHub Actions
  ├── pytest (tests unitaires)
  ├── Build image Docker
  └── Push vers Docker Hub (mq2vin/musicolab-back:main)
```

L'image Docker Hub est automatiquement utilisée par le `docker-compose.yml` du frontend.

---

## 📁 Structure du projet

```
musicolab-back/
├── .github/
│   └── workflows/
│       └── ci.yml          ← GitHub Actions (pytest + Docker build/push)
├── app/
│   ├── __init__.py         ← Création de l'application Flask
│   ├── routes/
│   │   ├── midi.py         ← Routes Module 1 (transposition MIDI)
│   │   └── audio.py        ← Routes Module 4 (analyse fréquentielle)
│   └── services/
│       ├── midi_service.py ← Logique de transposition
│       └── audio_service.py← Logique d'analyse spectrale (FFT)
├── tests/
│   ├── test_midi.py        ← Tests unitaires Module 1
│   └── test_audio.py       ← Tests unitaires Module 4
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 👥 Équipe

<div align="center">

| Contributeur | Rôle |
|---|---|
| **Parchemal NGUINGO** | Module 1 (MIDI) · Module 4 (Analyse) · Architecture |
| **mq2vin** | CI/CD · Docker · GitHub Actions |

</div>

---

## 🔗 Dépôt frontend

Le frontend React associé est disponible ici :
**[DUT-Info-Montreuil/musicolab-front](https://github.com/Illuminatyon/musicolab-front)**

---

<div align="center">

Projet éducatif — BUT Informatique Parcours Réalisation d'Applications (2027)

**IUT de Montreuil, Université Paris 8 — 2025–2026**

</div>
