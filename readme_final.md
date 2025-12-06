# Morpion Masters – README final

## 1. Présentation rapide
**Morpion Masters** est notre projet BDW (Bases de Données & Web) : un morpion enrichi qui illustre toute la stack imposée (Python + bdw-server, PostgreSQL bd-pedago, Jinja2, CSS modulaire). Ce README est volontairement court pour permettre aux évaluateurs et aux utilisateurs de lancer l’application en quelques minutes.
- **Public** : étudiants reprenant le code & jury de soutenance.
- **Fonctionnalités** : création d’équipes (16 morpions), modes normal/avancé, IA Minimax prête à l’emploi, page de statistiques avancées, export d’affiche.

## 2. Installation express
> Exécuter toutes les commandes depuis la racine du dépôt.

1. **Clonage & environnement**
   ```bash
   git clone <url-du-dépôt>
   cd project
   python3 -m venv .venv && source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.in
   ```
2. **Configuration BD**
   - Copier `config-bd.toml.example` → `config-bd.toml`.
   - Renseigner vos identifiants BDW :
     ```toml
     POSTGRESQL_SERVER = "bd-pedago.univ-lyon1.fr"
     POSTGRESQL_USER = "pXXXXXXX"
     POSTGRESQL_PASSWORD = "mdp_serveur"
     POSTGRESQL_DATABASE = "pXXXXXXX"
     POSTGRESQL_SCHEMA = "morpion"
     ```
3. **Scripts SQL obligatoires**
   ```bash
   psql -h bd-pedago.univ-lyon1.fr -U pXXXXXXX -d pXXXXXXX -f website-morpion/sql/schema.sql
   psql -h bd-pedago.univ-lyon1.fr -U pXXXXXXX -d pXXXXXXX -f website-morpion/sql/add_ai_team.sql
   ```
4. **(Optionnel) Données de démo**
   ```bash
   python scripts/db_init.py --reset
   ```

## 3. Lancement & vérifications
```bash
python server.py website-morpion
```
Ouvrir http://localhost:4242/ et vérifier le fonctionnement des differentes pages.

> **Tips** : si le style semble cassé, relancer `python scripts/build_css.py`. En cas d’erreur BD, recontrôler `config-bd.toml` et les scripts SQL.

## 4. Architecture en bref
```
Navigateur → server.py → routes.toml → controllers → models → PostgreSQL
                                        ↓
                                 templates & static
```
- `server.py` (bdw-server) charge les routes et expose `SESSION` (état persistant) et `REQUEST_VARS` (données envoyées aux templates).
- `controllers/` gère les flux métiers (équipe, partie, stats, affiche).
- `models/` encapsule l’accès BD (`team_repository`, `game_repository`, `advanced_stats_repository`) et la logique (`game_logic_*`, `ai_engine`).
- `templates/` et `static/` fournissent le design system (macros, CSS modulaire, JS minimal pour la partie avancée).

## 5. Fonctionnalités majeures
- **Mode normal** : configuration de partie, placement tour par tour, IA auto (sélectionner « 🤖 IA – Facile/Moyen/Difficile »).
- **Mode avancé** : actions RPG (placer, attaquer, sorts), logs chronologiques, rafraîchissement AJAX via `/partie-avancee-fragment`.
- **Statistiques avancées** : route `/statistiques-avancees`, 10 dashboards CSS-only (performances équipes, morpions, durées, sorts, etc.).
- **Affiche** : `/affiche-projet`, exportable en PDF via Ctrl+P.
- **Scripts utilitaires** : `scripts/db_backup.py`, `db_restore.py`, `db_wipe.py` pour administrer le schéma `morpion`.

## 6. Tests (pour contributeurs)
Les utilisateurs finaux n’ont pas besoin de lancer les tests. Pour les développeurs :
```bash
PYTHONPATH=website-morpion python tests/simulate_cases.py          # scénarios complets
PYTHONPATH=website-morpion python -m unittest tests/test_game_logic_avancee.py
python tests/test_ai_engine.py                                    # IA Minimax
```
Checklist stats : `python scripts/build_css.py` doit réussir puis `curl -I http://localhost:4242/statistiques-avancees` doit répondre 200.

## 7. Ressources
- Documentation détaillée (architecture, design system, soutenance) : `documentation_final.md`.
- Plan d’écriture avancé : `docs/README_2.md` + `docs/manual_redaction.md`.
- Consignes officielles : voir `soutenance/trash/consigne-project.md`.
