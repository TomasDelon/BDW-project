# Morpion Master – Guide pédagogique complet

Projet BDW (Bases de Données & Web) – Licence 2 Informatique UCBL Lyon 1  
Binôme : Tomas Delon & Moustapha Abakar

## 0. Pourquoi ce README ?
> Objectif : permettre à des étudiants n’ayant jamais travaillé avec un serveur web, PostgreSQL ou Jinja de comprendre le projet et de l’étendre sans se perdre.

Ce document suit une progression pas-à-pas :
1. Ce qu’il faut installer (définitions, commandes exactes).
2. Comment lancer une première partie pour valider l’environnement.
3. Comment le code est organisé (diagrammes ASCII, tableaux).
4. Comment écrire/modifier les Models, Views (Jinja + CSS + JS) et Controllers.
5. Checklist finale pour éviter les oublis lors du rendu.

---

## 1. Prérequis & installation guidée

### 1.1. Glossaire rapide
- **Python 3.11+** : langage utilisé côté serveur. Vérifiez avec `python3 --version`.
- **PostgreSQL** : base de données relationnelle fournie par l’UE (serveur `bd-pedago.univ-lyon1.fr`).
- **bdw-server** : mini-framework fourni par l’équipe enseignante. Le fichier `server.py` ne doit jamais être modifié.
- **Jinja2** : moteur de templates (génère le HTML à partir de fichiers `.html` contenant des instructions `{% ... %}`).
- **BEM** : convention de nommage CSS “Block__Element--Modifier” (ex. `game-grid__cell--occupied`).

### 1.2. Préparation du poste

| Étape | Commande | Pourquoi ? |
|-------|----------|------------|
| 1. Cloner le dépôt | `git clone … && cd project` | Récupérer le code source. |
| 2. Créer un venv | `python3 -m venv .venv` | Isoler les dépendances Python. |
| 3. Activer le venv | `source .venv/bin/activate` ou `.venv\Scripts\activate` | Utiliser l’environnement. |
| 4. Installer les libs | `python -m pip install --upgrade pip` puis `python -m pip install -r requirements.in` | Installer les packages (Jinja, psycopg…). |
| 5. Configurer la BD | Copier `config-bd.toml.example` → `config-bd.toml` et renseigner :<br>`POSTGRESQL_SERVER = "bd-pedago.univ-lyon1.fr"`<br>`POSTGRESQL_USER = "pXXXXXXX"`<br>`POSTGRESQL_PASSWORD = "mdp_serveur"`<br>`POSTGRESQL_DATABASE = "pXXXXXXX"`<br>`POSTGRESQL_SCHEMA = "morpion"` (**toujours cette valeur !**) | Permet au serveur de contacter PostgreSQL et garantit que tout le monde travaille dans le même schéma. |
| 6. Peupler la base | Via `psql` ou `pgweb`, exécuter `website-morpion/sql/schema.sql` puis `add_ai_team.sql`. | Crée les tables et des données minimales pour les tests. |

> 📌 Astuce : si `psql` n’est pas installé, utilisez <https://bdw.univ-lyon1.fr/> (pgweb) pour importer le script SQL. `schema.sql` commence par `DROP SCHEMA IF EXISTS morpion;`, crée le schéma si nécessaire, puis `SET search_path TO morpion;`. Vous n’avez donc pas besoin d’ajouter ces commandes manuellement tant que `POSTGRESQL_SCHEMA` vaut `"morpion"`.

### 1.3. Premier lancement
```bash
# Toujours dans le venv
python server.py website-morpion
```
Ouvrez ensuite <http://localhost:4242/> :
- Page d’accueil → vérifiez que les statistiques s’affichent (sinon revoyez les scripts SQL).
- Menu “Nouvelle partie” → suivez les étapes, lancez une grille 3×3.  
Si une erreur apparaît, regardez le message en bas de page (composant `message.html`) et la console du terminal.

---

## 2. Vue d’ensemble (MVC expliqué)

### 2.1. Schéma de communication
```
 Navigateur (HTML+CSS+JS)
        👇 requête HTTP
    bdw-server / server.py
        👇 regarde
        routes.toml ──▶ controllers/ (game.py, game_advanced.py, etc.)
                              👇 appelle
                     models/ (repositories + logiques)
                              👇 parle à
                        PostgreSQL (schéma BDW)
                              👆 données
 templates/ (base/, pages/, components/, macros/) — render Jinja —▶ HTML
 static/ (styles/, js/, img/) ───────────────▶ ressources front
```

### 2.2. Arborescence essentielle

| Dossier / Fichier | Rôle pédagogique | Exemple |
|-------------------|------------------|---------|
| `config-bd.toml` | Identifiants BDW (serveur, utilisateur, schéma). | `POSTGRESQL_SCHEMA = "morpion"` |
| `routes.toml` | Routing HTTP → fonction Python. | `/partie = "controllers.game:start_or_resume_game"` |
| `website-morpion/models/` | Accès aux données et logiques de jeu. | `team_repository.py`, `game_logic_avancee.py`. |
| `website-morpion/controllers/` | Code appelé lors d’une requête. | `game.py`, `team_create.py`. |
| `website-morpion/templates/` | HTML Jinja découpé en pages/components/macros. | `templates/pages/game_play.html`. |
| `website-morpion/static/` | Styles (CSS), JS, images. | `static/styles/components/game-grid.css`. |
| `scripts/build_css.py` | Concatène les modules CSS en `main.css`. | `python scripts/build_css.py`. |

---

## 3. Models (M de MVC)

### 3.1. Philosophie
- **Pattern Repository** : chaque *repository* se charge d’une table ou d’un ensemble de requêtes (lecture, insertion, statistiques). Aucun SQL dans les contrôleurs.
- **Services métier** : `game_logic_normale.py` & `game_logic_avancee.py` décrivent les règles du morpion (placement, victoires, sorts). Ils combinent les repositories pour modifier la base.
- **IA en mode simple** : `ai_engine.py` calcule des coups lorsque vous affrontez l’équipe spéciale “🤖 IA Opponent”. Cette logique n’existe pas dans la partie avancée : les combats et sorts sont exclusivement pilotés par les joueurs humains.
- **Pure functions** : la plupart des fonctions reçoivent explicitement la connexion, l’identifiant de partie, etc. Cela facilite les tests et la réutilisation.

### 3.2. Tableau des modules clés

| Module | Description pédagogique | Points clés |
|--------|-------------------------|-------------|
| `model_pg.py` | Crée une connexion PostgreSQL (utilisée via `get_connection()`). | Utilise `psycopg.connect` avec les paramètres de `config-bd.toml`. |
| `db_utils.py` | Helpers (transactions, conversion en dict). | `dict_factory` transforme les résultats en dictionnaires. |
| `team_repository.py` | CRUD des équipes + sélection de morpions. | Fonctions `list_teams()`, `create_team()`, `delete_team()`. |
| `game_repository.py` | Gestion des parties (création, journal, configurations). | `create_game(...)`, `log_action(...)`. |
| `game_logic_normale.py` | Moteur du morpion “simple”. | Place les morpions, teste la victoire et interagit avec l’IA. |
| `game_logic_avancee.py` | Moteur avancé (attaques, sorts). | Vérifie les cibles adjacentes, gère la mana, la réussite (pas d’IA dans ce mode). |
| `ai_engine.py` | Stratégie de l’adversaire contrôlé par la machine. | Utilisé uniquement par `controllers/game.py` (mode simple) pour choisir les coups d’une équipe IA. |
| `advanced_stats_repository.py` | Requêtes SQL pour les statistiques (top équipes, durée, etc.). | Utilisé par la page d’accueil et la page de stats avancées. |

### 3.3. Exemple : créer une partie
1. `controllers/game.py` appelle `game_logic_normale.start_game(team1_id, team2_id, grid_size, max_turns)`.
2. `start_game` crée des enregistrements via `game_repository`.
3. `game_repository.create_game` exécute un `INSERT` en SQL et retourne l’ID de la partie.

> ✅ Retenez : **les contrôleurs ne parlent jamais directement à PostgreSQL**. Tout passe par les repositories ou les modules de logique.

---

## 4. Views (le **V** de MVC) : Jinja, CSS, JS

### 4.0. Cartographie du front-end (tree guidé)
Quand on entre dans `website-morpion/`, tout ce qui touche à la vue est volontairement séparé en deux blocs complémentaires : `templates/` pour la génération HTML par Jinja et `static/` pour les ressources servies telles quelles (CSS/JS/images). Cette séparation reflète le cycle MVC : les contrôleurs remplissent des variables, Jinja assemble les pages, et le navigateur télécharge ensuite les assets statiques.

```
website-morpion/
├── controllers/
├── models/
├── static/
│   ├── js/
│   ├── img/
│   └── styles/
└── templates/
    ├── base/
    ├── components/
    ├── macros/
    └── pages/
```

- `templates/` contient tout ce qui génère du HTML. On s’impose une hiérarchie stricte pour éviter la “spaghetti view” : d’abord un layout (`base/`), puis des pages (`pages/`) qui orchestrent des composants (`components/`) et utilisent des macros réutilisables (`macros/`). Les contrôleurs n’appellent jamais directement un composant ; ils rendent une page complète pour garantir une structure cohérente (header/footer/scripts).
- `static/` regroupe les assets non interprétés par Jinja. Les styles sont rangés par rôle (`styles/base`, `styles/components`, `styles/pages`) conformément au standard BEM et sont fusionnés par `scripts/build_css.py`. Les scripts JS suivent la même logique (fichiers très ciblés, sans bundler) et `img/` contient les illustrations référencées par les templates.

#### Zoom sur `templates/`
| Sous-dossier | Rôle | Patron Jinja utilisé |
|--------------|------|----------------------|
| `base/` | Layouts (structure `<html>`, `<head>`, `<body>`, blocs `content`, `scripts`, etc.). | `extends` : toutes les pages héritent de `base/layout.html`. |
| `pages/` | Pages complètes (accueil, création d’équipe, partie normale/avancée). Elles rassemblent plusieurs composants. | `extends` + éventuels `include` pour insérer les blocs importants. |
| `components/` | Morceaux autonomes (grille, logs, bandeaux de messages, cartes morpion/équipe). N’exposent qu’un seul bloc BEM principal. | `include` : on injecte le composant dans une page sans dupliquer le HTML. |
| `macros/` | Fonctions paramétrables qui génèrent un sous-arbre HTML (ex. carte de sélection de morpion, boutons d’actions). | `import`/`from … import …` : on appelle la macro comme une fonction Jinja. |

**Rappels Jinja appliqués au projet :**
- `extends` (héritage) : un fichier de `pages/` n’écrit que l’intérieur des blocs déclarés par `base/layout.html`. Résultat : on peut changer le header/footer pour tout le site sans toucher aux pages.
- `include` (composition) : les composants encapsulent une structure HTML + classes BEM. Une page inclut `components/message.html` pour assurer un rendu homogène des alertes.
- `macros` : définition dans `templates/macros/*.html`, import via `{% from 'macros/morpions.html' import morpion_selector_card %}` puis appel `{{ morpion_selector_card(morpion) }}`. Cela remplace avantageusement un `for` rempli de copier/coller.

#### Zoom sur `static/`
- `styles/` : petits fichiers orientés par domaine (`components/_game-grid.css`, `pages/_home.css`, etc.). Le script `scripts/build_css.py` garantit l’ordre d’inclusion (variables → base → layout → composants → pages → responsive) ainsi que l’unicité des classes BEM.
- `js/` : scripts modestes qui ciblent une interaction précise (`game_minimal.js` pour la partie classique, `game_advanced.js` pour l’AJAX). Chaque fichier suppose que le HTML a déjà été généré par les templates correspondants.
- `img/` : ressources statiques référencées dans les templates via `{{ static('img/morpion-logo.svg') }}`. En garder la maîtrise évite les chemins relatifs fragiles et documente les assets réellement utilisés.

> 🔎 Pourquoi détailler ce tree ? Les étudiants repèrent immédiatement où placer une nouvelle vue ou un nouveau composant, comprennent quels fichiers peuvent être modifiés sans casser le layout global et réutilisent les mêmes patrons (`extends`, `include`, macros) plutôt que de mélanger logique et présentation.

### 4.1. Comprendre Jinja2
Un template Jinja est un fichier HTML enrichi de balises :
- **Variables** : `{{ game.team1_name }}` affiche une valeur Python.
- **Contrôle** : `{% if current_player == 1 %} ... {% endif %}` gère les conditions.
- **Boucles** : `{% for morpion in team %} ... {% endfor %}` répète un bloc.
- **Macros** : fonctions réutilisables définies dans `templates/macros/`.

Organisation :
- `templates/base/` → squelettes (`base/layout.html`) avec les balises `<head>`, `<body>`, `<header>`, etc.
- `templates/pages/` → pages complètes (`home.html`, `team_create.html`, `game_play.html`, `game_advanced_play.html`).
- `templates/components/` → fractions de pages (grille de jeu, logs, messages flash).
- `templates/macros/` → fonctions (ex. `morpion_selector_card`) pour générer des mini-blocs HTML avec paramètres.

#### Étendre un layout (`extends`)
```jinja
{% extends 'base/layout.html' %}
{% block content %}
  <h1>Liste des équipes</h1>
{% endblock %}
```
La page injecte son contenu dans les blocs (`content`, `scripts`, etc.) définis dans `base/layout.html`.

#### Réutiliser un composant (`include`)
```jinja
<section class="teams">
  {% include 'components/message.html' %}
  {% include 'components/team_card.html' %}
</section>
```
`include` insère le contenu tel quel. Chaque composant utilise ses propres classes BEM (`team-card__header`, `team-card__stats`), ce qui simplifie la maintenance.

#### Créer et appeler une macro
`templates/macros/morpions.html` :
```jinja
{% macro morpion_selector_card(morpion, input_name='morpion_id') %}
  <div class="morpion-selector__option">
    <input type="radio" name="{{ input_name }}" value="{{ morpion.id_morpion }}">
    <label class="morpion-selector__label">{{ morpion.name }}</label>
  </div>
{% endmacro %}
```
Utilisation :
```jinja
{% from 'macros/morpions.html' import morpion_selector_card %}
{{ morpion_selector_card(morpion, input_name='team1_morpion') }}
```
Les macros évitent de copier/coller le même HTML dans plusieurs pages.

#### Exemple concret : composant de grille (`components/game_grid.html`)
```jinja
<div class="game-grid">
  <h3 class="game-grid__title">🎲 Grille de jeu</h3>
  <table class="game-grid__board game-grid__board--size-{{ grid_size }}">
    {% for row in range(grid_size) %}
      <tr>
        {% for col in range(grid_size) %}
          {% set cell = grid.get((row, col)) %}
          {% include 'components/game_cell.html' %}
        {% endfor %}
      </tr>
    {% endfor %}
  </table>
</div>
```
Le composant appelle lui-même `game_cell.html` pour remplir chaque cellule, ce qui découpe clairement la vue.

### 4.2. CSS modulaire + build_css.py
- Tous les styles sont rangés par rôle (`base/`, `components/`, `pages/`, `layout/`, `utilities/`).
- `main.css` est **généré automatiquement** :
  ```bash
  python scripts/build_css.py
  ```
  Pourquoi ? Pour garantir l’ordre (variables → utilitaires → composants → pages → responsive), éviter les conflits d’imports et faciliter l’entretien de fichiers courts. On modifie les petits fichiers puis on régénère `main.css`.

### 4.3. Méthodologie BEM
- **Bloc** : entité indépendante (`game-grid`, `morpion-selector`, `game-play-layout`).
- **Élément** : partie du bloc (`game-grid__cell`, `morpion-selector__card`).
- **Modificateur** : variation (`game-grid__cell--occupied`, `game-grid__cell-content--advanced`).

Avantages pédagogiques :
1. Le HTML et le CSS portent le même vocabulaire → on trouve rapidement les styles.
2. Un composant peut être déplacé ou dupliqué sans effet de bord.
3. Les fichiers CSS sont lisibles par n’importe qui (pas besoin de connaître la cascade complète).

### 4.4. JavaScript minimaliste mais utile
- `static/js/game_minimal.js` : se contente de synchroniser les boutons radio pour la partie normale.
- `static/js/game_advanced.js` : ajoute une couche AJAX pour la partie avancée.

#### Comment fonctionne l’AJAX (détaillé)
```
1. L’utilisateur clique sur un bouton (attaque, sort…)
2. Le formulaire .ajax-form est intercepté par game_advanced.js
3. Le script sérialise les champs + le bouton cliqué (`event.submitter`)
4. Il envoie la requête via `fetch()` vers `/partie-avancee-fragment`
5. Le serveur renvoie uniquement la section HTML mise à jour (pas tout le layout)
6. Le script remplace `.game-play-section` par la nouvelle version
7. `history.replaceState` garde l’URL “propre” (`/partie-avancee?...`)
```
Extrait simplifié :
```javascript
const forms = root.querySelectorAll('form.ajax-form');
forms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new URLSearchParams(new FormData(form));
    fetch(form.action, { method: form.method, body: data })
      .then((res) => res.text())
      .then((html) => {
        const fragment = new DOMParser().parseFromString(html, 'text/html');
        document.querySelector('.game-play-section')
                .replaceWith(fragment.querySelector('.game-play-section'));
      });
  });
});
```
Ce mécanisme évite les rechargements complets, améliore la fluidité et permet d’afficher rapidement les retours (succès, erreurs) après chaque action.

Résultat : l’interface reste fluide même quand on enchaîne attaques, sorts ou actions IA.

---

## 5. Controllers (C de MVC)

### 5.1. Routage
`routes.toml` associe chaque URL à un contrôleur :
```
/             = "controllers.home:home"
/partie       = "controllers.game:start_or_resume_game"
/partie-avancee = "controllers.game_advanced:play"
/equipes      = "controllers.team_list:list_teams"
/creer-equipe = "controllers.team_create:create_team"
```
Ainsi `bdw-server` sait quelle fonction appeler pour chaque requête.

### 5.2. Patrons appliqués
- **Contrôleurs fins** : chaque module Python gère une fonctionnalité. Exemple :
  - `controllers/game.py` → partie classique (placements uniquement).
  - `controllers/game_advanced.py` → tours avancés (attaque, sorts, AJAX).
  - `controllers/team_create.py` → formulaire de création d’équipe.
- **IA côté contrôleur normal** : `controllers/game.py` importe `MorpionAI` depuis `models.ai_engine`. Lorsque vous définissez l’équipe “🤖 IA Opponent”, ce contrôleur appelle l’IA pour jouer à votre place. `game_advanced.py` ne déclenche jamais l’IA : ce mode est 100 % manuel.
- **Utilitaires partagés** : `controllers/game_session_utils.py` centralise la logique de session (joueur actuel, parties en cours) pour éviter la duplication.
- **Messages uniformes** : les contrôleurs renvoient des statuts (succès, avertissement, erreur) que `components/message.html` affiche systématiquement.

### 5.3. Exemple détaillé : lancer une partie avancée
1. `GET /partie-avancee` → `controllers.game_advanced.play`.
2. Le contrôleur :
   - lit les paramètres (équipes, taille de grille, limite de tours) ;
   - appelle `game_logic_avancee` pour préparer ou actualiser la partie ;
   - récupère le plateau et les journaux depuis `game_repository`.
3. Il stocke toutes les données dans `REQUEST_VARS` (structure fournie par bdw-server).
4. Il rend `templates/pages/game_advanced_play.html` ou, en AJAX, `pages/partials/game_advanced_fragment.html`.

> 🧠 À retenir : les contrôleurs sont des “coordonateurs”. Ils orchestrent les repositories, la logique métier et le rendu Jinja mais ne contiennent pas eux-mêmes de calcul lourd.

---

## 6. Base de données & scripts SQL

### 6.1. Structure minimale
- Tables : `morpion`, `team`, `team_morpion` (association), `game_config`, `game`, `game_log`.
- Contraintes : par exemple un morpion appartient à plusieurs équipes via `team_morpion`, chaque équipe contient 6–8 morpions (vérifié côté contrôleur), `game_log` possède un `log_num` unique par partie.

### 6.2. Scripts fournis
| Fichier | Contenu |
|---------|---------|
| `website-morpion/sql/schema.sql` | Création des tables + quelques données d’exemple. |
| `website-morpion/sql/add_ai_team.sql` | Ajoute une équipe contrôlée par l’IA pour les tests. |

> 💡 Astuce : `schema.sql` recrée le schéma `morpion` et exécute `SET search_path TO morpion;`. Si une page vous indique “Aucune équipe disponible”, réexécutez ce script puis `add_ai_team.sql` pour restaurer les données de base.

---

## 7. Tests et qualité
- Tests Python : `pytest tests/` (ex. `tests/test_game_logic_avancee.py` simule des tours pour vérifier que les règles avancées restent cohérentes).
- Linting/formatting : suivez `flake8` / `black` si votre IDE les propose, même si non imposé par l’UE.
- Vérifications manuelles à chaque itération :
  1. `python scripts/build_css.py` (après modification des styles).
  2. `python server.py website-morpion` puis navigation manuelle (partie normale + avancée).
  3. Requêtes SQL directes (ex. `SELECT * FROM journal ORDER BY created_at DESC LIMIT 5;`) pour confirmer que les actions sont enregistrées.

---

## 8. Checklist “super novice”

1. ✅ Installer Python ≥ 3.11, créer le venv, installer `requirements.in`.
2. ✅ Configurer `config-bd.toml` (serveur BDW + schéma).
3. ✅ Importer `schema.sql` + `add_ai_team.sql`.
4. ✅ Lancer `python server.py website-morpion` et visiter <http://localhost:4242/>.
5. ✅ Tester :  
   - Créer une nouvelle partie normale (3×3).  
   - Créer une partie avancée, essayer une attaque et un sort.  
   - Supprimer/ajouter une équipe dans “Gestion des équipes”.
6. ✅ Si vous modifiez les styles → `python scripts/build_css.py`.
7. ✅ Avant le rendu : préparer le ZIP complet (code + configuration + scripts SQL + documents de conception) et l’affiche 1 page (captures + diagramme E/A + noms du binôme).

---

## 9. Ressources utiles
- Consigne officielle : `docs/statements/consigne-projet.pdf`.
- Aide TP BDW : `docs/statements/aide-tp.pdf`.
- Diagrammes + synthèses CSS/optimisations : dossier `docs/`.
- Support Jinja2 : <https://jinja.palletsprojects.com/>.
- PostgreSQL pour débutant·e·s : <https://www.postgresqltutorial.com/>.

---

En suivant ce guide, vous pouvez :
- comprendre où se situent les fichiers importants,
- modifier les règles de jeu sans casser le reste,
- créer vos propres composants Jinja + CSS BEM,
- déboguer rapidement grâce aux messages standardisés et à la structure MVC claire.

Bon développement et bonne soutenance ! 🚀
