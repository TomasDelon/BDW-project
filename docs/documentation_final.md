# Documentation finale – Plan détaillé

## 1. Introduction
1.1 Contexte académique (UE BDW, binôme).  
1.2 Objectifs pédagogiques (stack complète, MVC, BD).  
1.3 Portée du document vs README (profondeur, soutenance).

## 2. Installation & configuration approfondies
2.1 Prérequis logiciels/hardwares + commandes de vérification.  
2.2 Étapes détaillées (clone, venv, pip).  
2.3 Remplissage champ par champ de `config-bd.toml`.  
2.4 Scripts SQL (schema/reset/init, add_ai_team) + risques.  
2.5 Vérification connexion BD (psql, scripts db_utils).

## 3. Architecture générale & server.py
3.1 Diagramme ASCII du flux complet.  
3.2 Arborescence commentée (table + description).  
3.3 Fonctionnement de `server.py` (routes, import dynamique, SESSION/REQUEST_VARS).  
3.4 Variables globales détaillées, cycle de vie.

## 4. Models (repositories, services, IA)
4.1 `team_repository.py`, `game_repository.py`, `advanced_stats_repository.py`.  
4.2 Logiques métier `game_logic_normale/avancee`, `ai_engine`.  
4.3 Helpers BD (`model_pg.py`, `db_utils.py`), caches, transactions.

## 5. Views & Design system
5.1 Organisation base/pages/components/macros.  
5.2 Design system détaillé (variables CSS, utilitaires Flex/Grid, macros badges/morpions/charts).  
5.3 Pipeline CSS (`scripts/build_css.py`, structure core/utilities/components/pages).  
5.4 Exemples Avant/Après pour chaque amélioration.

## 6. Controllers & gestion d’état
6.1 Routes principales et paramètres.  
6.2 Gestion SESSION (clé `game_<id>`, caches, dirty flags).  
6.3 Helpers partagés (`game_session_utils.py`).  
6.4 AJAX & fragments (détection fetch, templates partiels).

## 7. Fonctionnalités détaillées
7.1 Mode normal : diagramme de séquence, gestion de l’IA.  
7.2 Mode avancé : actions (placer/attaquer/sorts), logs, statut morpions.  
7.3 Statistiques avancées : architecture, scripts SQL, description des 10 dashboards + checklist QA.  
7.4 Export affiche : structure HTML/CSS, méthodes d’export.  
7.5 IA (Minimax) : auto-install, difficultés, tests, troubleshooting.

## 8. Tests & QA
8.1 Commandes officielles (simulate_cases, unit tests).  
8.2 Tests IA.  
8.3 Checklist stats avancées (build CSS, route, visuels).  
8.4 Bonnes pratiques avant soutenance (ordre des tests, données minimales).

## 9. Backlog & refactors
9.1 Synthèse des refactors terminés (cache, design system, stats).  
9.2 Tâches restantes (team list perf, etc.) + impact.  
9.3 Conseils pour contributions futures.

## 10. Annexes
10.1 Scripts utilitaires détaillés (db_init, db_backup, db_restore, build_css).  
10.2 Consignes officielles résumées.  
10.3 Manuel de rédaction (référence à `docs/manual_redaction.md`).  
10.4 Plan README v2 (lien vers `docs/README_2.md`).

## 11. Guide soutenance
11.1 Scénario de démo recommandé.  
11.2 Points forts à mettre en avant (stats, IA, design system).  
11.3 Checklist matérielle/logistique.  
11.4 FAQ interne (questions probables, réponses courtes).
