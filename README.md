# Morpion Masters – site web

## Accès rapide
- Affiche du projet (PDF, sans installation) : [Consulter le PDF](docs/affiche-projet.pdf)
- Démo courte (1 min 21 s) : https://www.youtube.com/watch?v=MiDwoaK5XH4
- Présentation complète (5 min 54 s) : https://www.youtube.com/watch?v=oddrVlaIsCo
- Version web locale : `http://localhost:4242/affiche-projet`

Le PDF et les vidéos permettent de découvrir le projet sans lancer l'application. La version web locale reste disponible pour la démonstration complète en soutenance.

## Vue rapide
Projet BDW (Bases de Données & Web) : un morpion complet avec mode normal (IA Minimax), mode avancé type RPG, statistiques avancées et page d'affiche exportable. Ce README reste bref pour GitHub (Markdown pur).
- Public : étudiants qui reprennent le code et jury de soutenance.
- Routes principales : `/partie`, `/partie-avancee`, `/statistiques-avancees`, `/affiche-projet`.

## Prérequis
- Python 3.11+ (`python3 --version`)
- PostgreSQL sur bd-pedago avec schéma obligatoire `morpion`
- Identifiants personnels `pXXXXXXX` (même valeur pour `POSTGRESQL_USER` et `POSTGRESQL_DATABASE`)

Placeholders :
- `{{REPO_URL}}` : URL du dépôt (HTTPS ou SSH)
- `pXXXXXXX` : utilisateur BDW personnel

## Installation et démarrage
```bash
git clone {{REPO_URL}} && cd project
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.in
```

Configurer la base :
```bash
cp config-bd.toml.example config-bd.toml
# Éditer config-bd.toml avec vos valeurs (server, user, password, database, schema="morpion")
psql -h bd-pedago.univ-lyon1.fr -U pXXXXXXX -d pXXXXXXX -f website-morpion/sql/schema.sql
psql -h bd-pedago.univ-lyon1.fr -U pXXXXXXX -d pXXXXXXX -f website-morpion/sql/add_ai_team.sql
python scripts/db_init.py --reset   # optionnel : données de démo
```

Lancer le serveur :
```bash
python server.py website-morpion
```
Ouvrir http://localhost:4242/

## Vérifications rapides
- Page d'accueil : stats affichées ; si le style manque, lancer `python scripts/build_css.py`.
- Mode normal : créer une partie et choisir l'équipe IA pour valider Minimax.
- Mode avancé : `/partie-avancee` se rafraîchit par fragments.
- `/statistiques-avancees` répond en 200 (CSS maison uniquement).

## Structure essentielle
```
website-morpion/
├─ controllers/        (flux HTTP et orchestration)
├─ models/             (accès BD + logique normale/avancée/IA)
├─ templates/          (base, pages, components, macros Jinja)
├─ static/             (CSS modulaire, JS ponctuel, images)
├─ sql/                (schema.sql, add_ai_team.sql, données)
├─ routes.toml         (routes consommées par server.py)
└─ init.py             (vérifications de démarrage : CSS, DB)
```

## Fonctionnalités clés
- Mode normal avec tours et IA configurable.
- Mode avancé avec attaques, sorts et logs chronologiques (AJAX fragment).
- Statistiques avancées 100 % CSS.
- Export rapide de `/affiche-projet` en PDF via impression navigateur.
- Scripts utiles : `scripts/build_css.py`, `scripts/db_backup.py`, `db_restore.py`, `db_wipe.py`.

## Tests pour contributeurs
```bash
PYTHONPATH=website-morpion python tests/simulate_cases.py
PYTHONPATH=website-morpion python -m unittest tests/test_game_logic_avancee.py
python tests/test_ai_engine.py
```
Avant une soutenance : reconstruire le CSS (`python scripts/build_css.py`) et vérifier `/statistiques-avancees`.

## Documentation complémentaire
- `docs/guide_de_redaction_de_documentation.md`
- `readme_final.md` et `docs/README.md`
- `docs/README_EXPLICATION_GAPS.md`
