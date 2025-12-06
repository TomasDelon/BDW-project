


<style>
img[alt$=" icon"] {
  width: 16px;
  height: 16px;
  vertical-align: text-bottom;
}
</style>

├── ![toml icon][icon-toml] config-bd.toml


<pre>
📁 project
├── ![toml icon][icon-toml] config-bd.toml
├── ![logo icon][icon-logo] config-bd.toml.example
├── 📂 docs
│   └── ...
├── 📂 scripts
│   ├── ![python icon][icon-python] build_css.py
│   ├── ![python icon][icon-python] db_backup.py
│   ├── ![python icon][icon-python] db_init.py
│   ├── ![python icon][icon-python] db_restore.py
│   ├── ![python icon][icon-python] db_utils.py
│   └── ![python icon][icon-python] db_wipe.py
├── ![python icon][icon-python] server.py
├── 📂 tests
│   ├── ![python icon][icon-python] __init__.py
│   ├── ![python icon][icon-python] test_ai_engine.py
│   ├── ![python icon][icon-python] test_game_logic_avancee.py
│   ├── ![python icon][icon-python] test_game_logic_normale.py
│   ├── ![python icon][icon-python] test_game_session_utils.py
│   ├── ![python icon][icon-python] test_repositories.py
│   ├── ![python icon][icon-python] test_scripts.py
│   └── ![python icon][icon-python] test_simulate_cases.py
└── 📂 website-morpion
    ├── ![python icon][icon-python] constants.py
    ├── 📂 controllers
    │   ├── ![python icon][icon-python] affiche.py
    │   ├── ![python icon][icon-python] data_diagram.py
    │   ├── ![python icon][icon-python] game.py
    │   ├── ![python icon][icon-python] game_advanced.py
    │   ├── ![python icon][icon-python] game_session_utils.py
    │   ├── ![python icon][icon-python] home.py
    │   ├── ![python icon][icon-python] morpion_create.py
    │   ├── ![python icon][icon-python] stats_advanced.py
    │   ├── ![python icon][icon-python] team_create.py
    │   └── ![python icon][icon-python] team_list.py
    ├── ![python icon][icon-python] init.py
    ├── 📂 models
    │   ├── ![python icon][icon-python] advanced_stats_repository.py
    │   ├── ![python icon][icon-python] ai_engine.py
    │   ├── ![python icon][icon-python] custom_morpion_repository.py
    │   ├── ![python icon][icon-python] db_utils.py
    │   ├── ![python icon][icon-python] game_logic_avancee.py
    │   ├── ![python icon][icon-python] game_logic_normale.py
    │   ├── ![python icon][icon-python] game_repository.py
    │   ├── ![python icon][icon-python] model_pg.py
    │   ├── ![python icon][icon-python] stats_repository.py
    │   └── ![python icon][icon-python] team_repository.py
    ├── ![toml icon][icon-toml] routes.toml
    ├── 📂 sql
    │   ├── ![sql icon][icon-sql] add_ai_team.sql
    │   ├── ![sql icon][icon-sql] reset.sql
    │   └── ![sql icon][icon-sql] schema.sql
    ├── 📂 static
    │   ├── 📂 img
    │   │   ├── 📂 logos
    │   │   │   └── ...
    │   │   ├── 📂 morpions
    │   │   │   └── ...
    │   │   └── 📂 screenshots
    │   │       └── ...
    │   ├── 📂 js
    │   │   ├── ![javascript icon][icon-javascript] game_advanced.js
    │   │   ├── ![javascript icon][icon-javascript] game_classic.js
    │   │   ├── ![javascript icon][icon-javascript] game_minimal.js
    │   │   └── ![javascript icon][icon-javascript] morpion_create.js
    │   └── 📂 styles
    │       ├── ![css icon][icon-css] base.css
    │       ├── 📂 components
    │       │   ├── ![css icon][icon-css] alerts.css
    │       │   ├── ![css icon][icon-css] badges.css
    │       │   ├── ![css icon][icon-css] buttons.css
    │       │   ├── ![css icon][icon-css] charts.css
    │       │   ├── ![css icon][icon-css] confirmation-dialog.css
    │       │   ├── ![css icon][icon-css] deck-status.css
    │       │   ├── ![css icon][icon-css] design-system.css
    │       │   ├── ![css icon][icon-css] duration-compare.css
    │       │   ├── ![css icon][icon-css] empty-state.css
    │       │   ├── ![css icon][icon-css] footer.css
    │       │   ├── ![css icon][icon-css] forms.css
    │       │   ├── ![css icon][icon-css] game-created-box.css
    │       │   ├── ![css icon][icon-css] game-grid.css
    │       │   ├── ![css icon][icon-css] game-info-header.css
    │       │   ├── ![css icon][icon-css] game-logs.css
    │       │   ├── ![css icon][icon-css] hero.css
    │       │   ├── ![css icon][icon-css] morpion-card.css
    │       │   ├── ![css icon][icon-css] morpion-selector.css
    │       │   ├── ![css icon][icon-css] position-selector.css
    │       │   ├── ![css icon][icon-css] stats.css
    │       │   └── ![css icon][icon-css] team-card.css
    │       ├── ![css icon][icon-css] layout.css
    │       ├── ![css icon][icon-css] main.css
    │       ├── 📂 pages
    │       │   ├── ![css icon][icon-css] affiche.css
    │       │   ├── ![css icon][icon-css] data_diagram.css
    │       │   ├── ![css icon][icon-css] game_play.css
    │       │   ├── ![css icon][icon-css] game_setup.css
    │       │   ├── ![css icon][icon-css] morpion_create.css
    │       │   ├── ![css icon][icon-css] stats_advanced.css
    │       │   ├── ![css icon][icon-css] team_create.css
    │       │   └── ![css icon][icon-css] team_list.css
    │       └── ![css icon][icon-css] utilities.css
    └── 📂 templates
        ├── 📂 base
        │   ├── ![html icon][icon-html] base.html
        │   └── ![html icon][icon-html] base_affiche.html
        ├── 📂 components
        │   ├── ![html icon][icon-html] action_selector.html
        │   ├── ![html icon][icon-html] confirmation_dialog.html
        │   ├── ![html icon][icon-html] deck_status.html
        │   ├── ![html icon][icon-html] footer.html
        │   ├── ![html icon][icon-html] game_cell.html
        │   ├── ![html icon][icon-html] game_duration_compare.html
        │   ├── ![html icon][icon-html] game_grid.html
        │   ├── ![html icon][icon-html] game_info_header.html
        │   ├── ![html icon][icon-html] game_item.html
        │   ├── ![html icon][icon-html] game_logs.html
        │   ├── ![html icon][icon-html] header.html
        │   ├── ![html icon][icon-html] menu.html
        │   ├── ![html icon][icon-html] message.html
        │   ├── ![html icon][icon-html] morpion_card.html
        │   ├── ![html icon][icon-html] morpion_mini_card.html
        │   ├── ![html icon][icon-html] morpion_selector.html
        │   ├── ![html icon][icon-html] position_selector.html
        │   ├── ![html icon][icon-html] spell_selector.html
        │   ├── ![html icon][icon-html] team_card.html
        │   └── ![html icon][icon-html] team_header.html
        ├── 📂 macros
        │   ├── ![html icon][icon-html] charts.html
        │   ├── ![html icon][icon-html] design_system.html
        │   ├── ![html icon][icon-html] forms.html
        │   ├── ![html icon][icon-html] morpions.html
        │   ├── ![html icon][icon-html] stats.html
        │   ├── ![html icon][icon-html] teams.html
        │   └── ![html icon][icon-html] ui.html
        └── 📂 pages
            ├── ![html icon][icon-html] affiche_projet.html
            ├── ![html icon][icon-html] data_diagram.html
            ├── ![html icon][icon-html] game_advanced_play.html
            ├── ![html icon][icon-html] game_advanced_setup.html
            ├── ![html icon][icon-html] game_play.html
            ├── ![html icon][icon-html] game_setup.html
            ├── ![html icon][icon-html] home.html
            ├── ![html icon][icon-html] morpion_create.html
            ├── ![html icon][icon-html] stats_advanced.html
            ├── ![html icon][icon-html] team_create.html
            └── ![html icon][icon-html] team_list.html
</pre>

qsdf

[icon-css]: ../website-morpion/static/img/logos/css.svg "css icon"
[icon-html]: ../website-morpion/static/img/logos/html.svg "html icon"
[icon-javascript]: ../website-morpion/static/img/logos/javascript.svg "javascript icon"
[icon-logo]: ../website-morpion/static/img/logos/logo.png "logo icon"
[icon-python]: ../website-morpion/static/img/logos/python.svg "python icon"
[icon-sql]: ../website-morpion/static/img/logos/sql.svg "sql icon"
[icon-toml]: ../website-morpion/static/img/logos/toml.svg "toml icon"
