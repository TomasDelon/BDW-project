# README v2 – Plan détaillé

## 0. Intention du document
0.1 Fusionner la clarté pédagogique d’`EXPLICATION.md` avec le côté opérationnel du README actuel.  
0.2 Couvrir explicitement les points identifiés dans `docs/README_EXPLICATION_GAPS.md` (design system, stats avancées, tests, backlog, IA).  
0.3 Servir de structure définitive avant la réécriture complète et garantir qu’aucun livrable (affiche, soutenance) ne dépende de documents dispersés.

## 1. Présentation & contexte
1.1 Objectif du projet  
 1.1.1 Rappeler le cadre académique (UE BDW, binôme, attentes).  
 1.1.2 Décrire en une phrase la proposition de valeur (jeu de morpion avancé + stack complète).  
1.2 Public cible  
 1.2.1 Étudiants reprenant le code.  
 1.2.2 Jury de soutenance (ce qu’ils doivent valider).  
 1.2.3 Contributeurs externes.  
1.3 Fonctionnalités principales  
 1.3.1 Modes normal/avancé.  
 1.3.2 Statistiques/affiche.  
 1.3.3 IA (Minimax).  
 1.3.4 Bonus techniques (design system, scripts DB).

## 2. Installation & configuration
2.1 Prérequis matériels & logiciels  
 2.1.1 Versions Python/PostgreSQL supportées (avec commande de vérification).  
 2.1.2 Accès bd-pedago / VPN / proxy éventuels.  
 2.1.3 Outils facultatifs (pgAdmin, VSCode).  
2.2 Procédure pas-à-pas  
 2.2.1 Clonage du dépôt + création/activation du venv.  
 2.2.2 Installation des dépendances (pip + `requirements.in`).  
 2.2.3 Copie de `config-bd.toml.example` → `config-bd.toml` + détail champ par champ.  
 2.2.4 Scripts SQL obligatoires (`schema.sql`, `add_ai_team.sql`, `db_init.py`).  
 2.2.5 Commandes utiles pour vérifier la connexion BD (`psql`, `python -m scripts.db_utils`).  
2.3 Vérification initiale  
 2.3.1 Lancement du serveur (`python server.py website-morpion`).  
 2.3.2 Pages à visiter (home, création d’équipe, partie normale/avancée).  
 2.3.3 Diagnostic rapide en cas d’erreur (config TOML, logs console, CSS manquant).

## 3. Architecture générale
3.1 Vue d’ensemble MVC  
 3.1.1 Diagramme “navigateur → server.py → controllers → models → BD → templates/static”.  
 3.1.2 Points clés (séparation stricte, pas de SQL hors models).  
3.2 Arborescence essentielle  
 3.2.1 Tableau par dossier (controllers, models, templates, static, scripts).  
 3.2.2 Liens croisés (ex: `controllers/game.py` ↔ `templates/pages/game_play.html`).  
3.3 Rôle du `server.py`  
 3.3.1 Chargement dynamique des routes.  
 3.3.2 Variables globales exposées (`SESSION`, `REQUEST_VARS`, `GET`, `POST`).  
 3.3.3 Processus d’initialisation (`init.py`, build CSS check).  
3.4 environnement BD / config  
 3.4.1 Gestion de la connexion (singleton).  
 3.4.2 Impact des scripts `scripts/db_*.py`.

## 4. Models (M)
4.1 Repositories  
 4.1.1 `team_repository.py` (CRUD équipes/morpions).  
 4.1.2 `game_repository.py` (création partie, logs, configs).  
 4.1.3 `advanced_stats_repository.py` (CTE, agrégations).  
4.2 Logiques métiers  
 4.2.1 `game_logic_normale.py` (placements, check victoire).  
 4.2.2 `game_logic_avancee.py` (attaques, sorts, états HP/Mana).  
 4.2.3 `ai_engine.py` (Minimax, difficultés).  
4.3 Accès BD & helpers  
 4.3.1 `model_pg.py` (initialisation connexion, dict factory).  
 4.3.2 `db_utils.py` (transactions, helpers).  
 4.3.3 Gestion des caches en SESSION vs requêtes directes.

## 5. Views (V) & design system
5.1 Organisation des templates  
 5.1.1 Layout `base/base.html` et blocs disponibles.  
 5.1.2 `templates/pages/` (pages entières).  
 5.1.3 `templates/components/` (fragments réutilisables).  
 5.1.4 `templates/macros/` (fonctions Jinja).  
5.2 Design system  
 5.2.1 Variables CSS  
  • 5.2.1.1 Tailles d’images et cellules.  
  • 5.2.1.2 Breakpoints et min-height.  
 5.2.2 Utilitaires  
  • 5.2.2.1 Classes Flex (`flex`, `flex-center`, `flex-between`).  
  • 5.2.2.2 Classes Grid (`grid-auto-fit`, `grid-morpions`).  
 5.2.3 Macros  
  • 5.2.3.1 Badges d’équipe (`team_badge`, winner).  
  • 5.2.3.2 Sélecteur de morpion (`morpion_selector_card`).  
  • 5.2.3.3 Composants charts (`progress_bar`, `bar_chart_row`).  
5.3 Build CSS et structure des styles  
 5.3.1 Rôle de `scripts/build_css.py`.  
 5.3.2 Organisation `core/`, `utilities/`, `components/`, `pages/`.  
 5.3.3 Conseils pour ajouter un nouveau module (nommage BEM, import).

## 6. Controllers (C)
6.1 Routes principales  
 6.1.1 Résumé des URL et fichiers (`routes.toml`).  
 6.1.2 Paramètres GET/POST manipulés par chaque contrôleur.  
6.2 Gestion d’état  
 6.2.1 Stockage des parties en SESSION (clé `game_<id>`).  
 6.2.2 Différences entre mode normal vs avancé (caches, logs, dirty flags).  
 6.2.3 Synchronisation DB ↔ SESSION.  
6.3 Helpers partagés  
 6.3.1 `game_session_utils.py` (initialisation, sync, messages).  
 6.3.2 Stratégies pour éviter la duplication (ex: IA, logs).  
6.4 AJAX & fragments  
 6.4.1 Détection des requêtes fetch (`HTTP_X_REQUESTED_WITH`).  
 6.4.2 Templates fragment vs page complète.

## 7. Fonctionnalités clés
7.1 Mode normal  
 7.1.1 Création de partie (formulaire, validations).  
 7.1.2 Déroulement (placements, victoires, fin de partie).  
 7.1.3 Interaction avec l’IA (détection équipe IA, tour automatique).  
7.2 Mode avancé  
 7.2.1 Actions disponibles (placer, attaquer, sorts).  
 7.2.2 Gestion des HP/mana/logs.  
 7.2.3 AJAX et route fragment (`/partie-avancee-fragment`).  
7.3 Statistiques avancées  
 7.3.1 Architecture (controller + repository + template + CSS).  
 7.3.2 Description des 10 analyses avec mini explication utile en soutenance.  
 7.3.3 Checklist rapide de validation (build CSS, route accessible, données minimales).  
7.4 IA (Minimax)  
 7.4.1 Installation automatique (init.py) + scripts SQL requis.  
 7.4.2 Difficultés, limites de profondeur, stockage en SESSION.  
 7.4.3 Tests disponibles (`tests/test_ai_engine.py`).  
7.5 Export affiche  
 7.5.1 Page `/affiche-projet`.  
 7.5.2 Méthodes d’export (navigateur, wkhtmltopdf, puppeteer).  
 7.5.3 Checklist visuelle.

## 8. Design system & Frontend (détails pratiques)
8.1 Variables → exemples "Avant/Après"  
 8.1.1 Tailles d’images (avant: 60px hardcodé, après: `var(--img-morpion-card)`).  
 8.1.2 Tailles de cellule (desktop/tablette/mobile).  
 8.1.3 Breakpoints (`@media` → variables).  
8.2 Utilitaires Flex/Grid  
 8.2.1 `flex-center`, `flex-between` → snippet header de partie.  
 8.2.2 `flex-column-center`, `flex-wrap` → cartes responsive.  
 8.2.3 `grid-auto-fit`, `grid-morpions` → layout d’équipe/morpions.  
8.3 Macros pratiques  
 8.3.1 `team_badge` & variantes (sm/md/lg, winner).  
 8.3.2 `morpion_selector_card` (paramètres `input_type`, `show_stats`).  
 8.3.3 `progress_bar`, `bar_chart_row`, `stat_card_simple`.  
8.4 Build pipeline  
 8.4.1 Quand relancer `scripts/build_css.py`.  
 8.4.2 Conseils pour éviter `main.css` obsolète (vérifications startup).  
 8.4.3 Où ajouter un nouveau fichier (ordre dans `CSS_SOURCES`).

## 9. Tests & QA
9.1 Commandes obligatoires  
 9.1.1 `PYTHONPATH=website-morpion python tests/simulate_cases.py` (scénarios).  
 9.1.2 `PYTHONPATH=website-morpion python -m unittest tests/test_game_logic_avancee.py`.  
9.2 Tests IA  
 9.2.1 `python tests/test_ai_engine.py`.  
 9.2.2 Validation manuelle (créer partie vs IA, observer logs).  
9.3 Checklist stats avancées  
 9.3.1 Build CSS (commande + sortie attendue).  
 9.3.2 Vérifier route /statistiques-avancees (curl + navigateur).  
 9.3.3 Points visuels à contrôler (10 sections, animations, responsive).  
9.4 Recommandations pré-soutenance  
 9.4.1 Ordre des tests à relancer.  
 9.4.2 Logs serveur à surveiller (erreurs DB, CSS).  
 9.4.3 Données minimales à conserver (équipes, parties, stats).

## 10. Backlog & refactors
10.1 Tâches terminées  
 10.1.1 Liste synthétique (factoring controllers, suppression grid_state, design system, stats).  
 10.1.2 Lien vers `CHANGES.md` pour détails.  
10.2 Tâches restantes  
 10.2.1 Issues identifiées dans `todo_analysis` (team list perf, etc.).  
 10.2.2 Priorité/risques avant soutenance.  
10.3 Impact sur la démo  
 10.3.1 Ce qui est stable (modes normal/avancé, IA).  
 10.3.2 Ce qui reste expérimental (optimisations en cours).  
 10.3.3 Stratégie de communication (mentionner limitations vs roadmap).

## 11. Annexes utiles
11.1 Scripts utilitaires  
 11.1.1 `scripts/db_init.py`, `db_backup.py`, `db_restore.py`, `db_wipe.py`.  
 11.1.2 `scripts/build_css.py` (options, erreurs communes).  
11.2 Export affiche  
 11.2.1 Méthodes (navigateur, wkhtmltopdf, puppeteer).  
 11.2.2 Checklist du PDF (infos binôme, fonctionnalités, schéma, captures).  
11.3 Consignes officielles  
 11.3.1 Résumé des obligations (BD obligatoire, architecture, rendu).  
 11.3.2 Lien vers `consigne-project.md` et rappel des livrables.

## 12. Guide soutenance
12.1 Scénario de démo  
 12.1.1 Ouverture (présentation rapide + page d’accueil).  
 12.1.2 Parcours création équipe → partie normale → partie avancée → stats → affiche.  
12.2 Points différenciants à mettre en avant  
 12.2.1 Statistiques avancées (CSS pur, SQL avancé).  
 12.2.2 IA (Minimax + auto-install).  
 12.2.3 Design system (cohérence front, macros).  
12.3 Checklist matérielle  
 12.3.1 Serveur lancé, build CSS à jour, base peuplée.  
 12.3.2 Navigateur configuré (onglets prêts).  
 12.3.3 Plan B en cas de panne (dump BD, notes hors ligne).

---

Ce plan servira de TOC détaillée pour réécrire le README final, en garantissant la couverture des points manquants identifiés.
