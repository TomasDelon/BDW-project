<style>
:root {
  --logo-html: url("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg");
  --logo-css: url("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg");
  --logo-js: url("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg");
  --logo-python: url("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg");
  --logo-sql: url("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg");

  --logo-markdown: url("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/markdown/markdown-original.svg");
  --logo-text: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect x='1' y='0.5' width='14' height='15' rx='2' ry='2' fill='%23f4f4f4' stroke='%23000' stroke-width='0.8'/%3E%3Ctext x='8' y='11.5' font-family='Arial' font-size='7' text-anchor='middle' fill='%23000'%3ETXT%3C/text%3E%3C/svg%3E");
  --logo-box: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M1 5.2L8 1l7 4.2v6.6L8 15 1 11.8z' fill='%23f0c419' stroke='%238a5a0a' stroke-width='0.8'/%3E%3Cpath d='M1 5.2l7 3.8 7-3.8' fill='none' stroke='%238a5a0a' stroke-width='0.8'/%3E%3Cpath d='M8 1v14' fill='none' stroke='%238a5a0a' stroke-width='0.8'/%3E%3C/svg%3E");
  --logo-folder: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M1.5 4h4l1 1.5h8v7.5a1 1 0 01-1 1h-11a1 1 0 01-1-1z' fill='%23fbd490' stroke='%23c38a2e' stroke-width='0.7'/%3E%3Cpath d='M1.5 4.5h13' stroke='%23c38a2e' stroke-width='0.7'/%3E%3C/svg%3E");
}

i {
  display: inline-block;
  width: 16px;
  height: 16px;
  vertical-align: -3px;
}

i[html]{ background-image: var(--logo-html); }
i[css]{ background-image: var(--logo-css); }
i[js]{ background-image: var(--logo-js); }
i[py]{ background-image: var(--logo-python); }
i[sql]{ background-image: var(--logo-sql); }
i[md]{ background-image: var(--logo-markdown); }
i[file]{ background-image: var(--logo-text); }
i[toml]{ background-image: var(--logo-text); }
i[project]{ background-image: var(--logo-box); }
i[folder]{ background-image: var(--logo-folder); }

</style>


# Tabla 

| Elemento | Código | Vista |
|----------|--------|-------|
| HTML | ``<i html></i>`` | <i html></i> |
| CSS | ``<i css></i>`` | <i css></i> |
| JavaScript | ``<i js></i>`` | <i js></i> |
| Python | ``<i py></i>`` | <i py></i> |
| SQL | ``<i sql></i>`` | <i sql></i> |
| Markdown | ``<i md></i>`` | <i md></i> |
| TOML | ``<i toml></i>`` | <i toml></i> |
| Proyecto | ``<i project></i>`` | <i project></i> |
| Carpeta | ``<i folder></i>`` | <i folder></i> |

# Arbol global

<pre class="tree">
<i project></i> project/
┣━━ <i folder></i> docs/
┃   ┗━━ ...
┣━━ <i toml></i> config-bd.toml
┣━━ <i toml></i> config-bd.toml.example
┣━━ <i file></i> requirements.in
┣━━ <i folder></i> scripts/
┃   ┣━━ <i py></i> apply_fontawesome_placeholders.py
┃   ┣━━ <i py></i> build_css.py
┃   ┣━━ <i py></i> db_backup.py
┃   ┣━━ <i py></i> db_init.py
┃   ┣━━ <i py></i> db_restore.py
┃   ┣━━ <i py></i> db_utils.py
┃   ┗━━ <i py></i> db_wipe.py
┣━━ <i py></i> server.py
┣━━ <i folder></i> tests/
┃   ┣━━ <i py></i> __init__.py
┃   ┣━━ <i py></i> test_ai_engine.py
┃   ┣━━ <i py></i> test_game_logic_avancee.py
┃   ┣━━ <i py></i> test_game_logic_normale.py
┃   ┣━━ <i py></i> test_game_session_utils.py
┃   ┣━━ <i py></i> test_repositories.py
┃   ┣━━ <i py></i> test_scripts.py
┃   ┗━━ <i py></i> test_simulate_cases.py
┗━━ <i folder></i> website-morpion/
    ┣━━ <i py></i> constants.py
    ┣━━ <i folder></i> controllers/
    ┃   ┣━━ <i py></i> affiche.py
    ┃   ┣━━ <i py></i> data_diagram.py
    ┃   ┣━━ <i py></i> game.py
    ┃   ┣━━ <i py></i> game_advanced.py
    ┃   ┣━━ <i py></i> game_session_utils.py
    ┃   ┣━━ <i py></i> home.py
    ┃   ┣━━ <i py></i> morpion_create.py
    ┃   ┣━━ <i py></i> stats_advanced.py
    ┃   ┣━━ <i py></i> team_create.py
    ┃   ┗━━ <i py></i> team_list.py
    ┣━━ <i py></i> init.py
    ┣━━ <i folder></i> models/
    ┃   ┣━━ <i py></i> advanced_stats_repository.py
    ┃   ┣━━ <i py></i> ai_engine.py
    ┃   ┣━━ <i py></i> custom_morpion_repository.py
    ┃   ┣━━ <i py></i> db_utils.py
    ┃   ┣━━ <i py></i> game_logic_avancee.py
    ┃   ┣━━ <i py></i> game_logic_normale.py
    ┃   ┣━━ <i py></i> game_repository.py
    ┃   ┣━━ <i py></i> model_pg.py
    ┃   ┣━━ <i py></i> stats_repository.py
    ┃   ┗━━ <i py></i> team_repository.py
    ┣━━ <i toml></i> routes.toml
    ┣━━ <i folder></i> sql/
    ┃   ┣━━ <i sql></i> add_ai_team.sql
    ┃   ┣━━ <i sql></i> reset.sql
    ┃   ┗━━ <i sql></i> schema.sql
    ┣━━ <i folder></i> static/
    ┃   ┣━━ <i folder></i> img/
    ┃   ┃   ┣━━ <i folder></i> logos/
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┣━━ <i folder></i> morpions/
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┗━━ <i folder></i> screenshots/
    ┃   ┃       ┗━━ ...
    ┃   ┣━━ <i folder></i> js/
    ┃   ┃   ┣━━ <i js></i> game_advanced.js
    ┃   ┃   ┣━━ <i js></i> game_classic.js
    ┃   ┃   ┣━━ <i js></i> game_minimal.js
    ┃   ┃   ┗━━ <i js></i> morpion_create.js
    ┃   ┗━━ <i folder></i> styles/
    ┃       ┣━━ <i css></i> base.css
    ┃       ┣━━ <i folder></i> components/
    ┃       ┃   ┣━━ <i css></i> alerts.css
    ┃       ┃   ┣━━ <i css></i> badges.css
    ┃       ┃   ┣━━ <i css></i> buttons.css
    ┃       ┃   ┣━━ <i css></i> charts.css
    ┃       ┃   ┣━━ <i css></i> confirmation-dialog.css
    ┃       ┃   ┣━━ <i css></i> deck-status.css
    ┃       ┃   ┣━━ <i css></i> design-system.css
    ┃       ┃   ┣━━ <i css></i> duration-compare.css
    ┃       ┃   ┣━━ <i css></i> empty-state.css
    ┃       ┃   ┣━━ <i css></i> footer.css
    ┃       ┃   ┣━━ <i css></i> forms.css
    ┃       ┃   ┣━━ <i css></i> game-created-box.css
    ┃       ┃   ┣━━ <i css></i> game-grid.css
    ┃       ┃   ┣━━ <i css></i> game-info-header.css
    ┃       ┃   ┣━━ <i css></i> game-logs.css
    ┃       ┃   ┣━━ <i css></i> hero.css
    ┃       ┃   ┣━━ <i css></i> morpion-card.css
    ┃       ┃   ┣━━ <i css></i> morpion-selector.css
    ┃       ┃   ┣━━ <i css></i> position-selector.css
    ┃       ┃   ┣━━ <i css></i> stats.css
    ┃       ┃   ┗━━ <i css></i> team-card.css
    ┃       ┣━━ <i css></i> layout.css
    ┃       ┣━━ <i css></i> main.css
    ┃       ┣━━ <i folder></i> pages/
    ┃       ┃   ┣━━ <i css></i> affiche.css
    ┃       ┃   ┣━━ <i css></i> data_diagram.css
    ┃       ┃   ┣━━ <i css></i> game_play.css
    ┃       ┃   ┣━━ <i css></i> game_setup.css
    ┃       ┃   ┣━━ <i css></i> morpion_create.css
    ┃       ┃   ┣━━ <i css></i> stats_advanced.css
    ┃       ┃   ┣━━ <i css></i> team_create.css
    ┃       ┃   ┗━━ <i css></i> team_list.css
    ┃       ┗━━ <i css></i> utilities.css
    ┗━━ <i folder></i> templates/
        ┣━━ <i folder></i> base/
        ┃   ┣━━ <i html></i> base.html
        ┃   ┗━━ <i html></i> base_affiche.html
        ┣━━ <i folder></i> components/
        ┃   ┣━━ <i html></i> action_selector.html
        ┃   ┣━━ <i html></i> confirmation_dialog.html
        ┃   ┣━━ <i html></i> deck_status.html
        ┃   ┣━━ <i html></i> footer.html
        ┃   ┣━━ <i html></i> game_cell.html
        ┃   ┣━━ <i html></i> game_duration_compare.html
        ┃   ┣━━ <i html></i> game_grid.html
        ┃   ┣━━ <i html></i> game_info_header.html
        ┃   ┣━━ <i html></i> game_item.html
        ┃   ┣━━ <i html></i> game_logs.html
        ┃   ┣━━ <i html></i> header.html
        ┃   ┣━━ <i html></i> menu.html
        ┃   ┣━━ <i html></i> message.html
        ┃   ┣━━ <i html></i> morpion_card.html
        ┃   ┣━━ <i html></i> morpion_mini_card.html
        ┃   ┣━━ <i html></i> morpion_selector.html
        ┃   ┣━━ <i html></i> position-selector.html
        ┃   ┣━━ <i html></i> spell_selector.html
        ┃   ┣━━ <i html></i> team_card.html
        ┃   ┗━━ <i html></i> team_header.html
        ┣━━ <i folder></i> macros/
        ┃   ┣━━ <i html></i> charts.html
        ┃   ┣━━ <i html></i> design_system.html
        ┃   ┣━━ <i html></i> forms.html
        ┃   ┣━━ <i html></i> morpions.html
        ┃   ┣━━ <i html></i> stats.html
        ┃   ┣━━ <i html></i> teams.html
        ┃   ┗━━ <i html></i> ui.html
        ┗━━ <i folder></i> pages/
            ┣━━ <i html></i> affiche_projet.html
            ┣━━ <i html></i> data_diagram.html
            ┣━━ <i html></i> game_advanced_play.html
            ┣━━ <i html></i> game_advanced_setup.html
            ┣━━ <i html></i> game_play.html
            ┣━━ <i html></i> game_setup.html
            ┣━━ <i html></i> home.html
            ┣━━ <i html></i> morpion_create.html
            ┣━━ <i html></i> stats_advanced.html
            ┣━━ <i html></i> team_create.html
            ┗━━ <i html></i> team_list.html
</pre>

<pre>
<i project></i> project/
┣━━ <i py></i> server.py
┣━━ <i file></i> requirements.in
┣━━ <i toml></i> config-bd.toml
┣━━ <i toml></i> config-bd.toml.example
┣━━ <i folder></i> scripts/
┃   ┗━━ ...
┣━━ <i folder></i> docs/
┃   ┗━━ ...
┣━━ <i folder></i> tests/
┃   ┗━━ ...
┗━━ <i folder></i> website-morpion/
    ┣━━ <i py></i> init.py
    ┣━━ <i toml></i> routes.toml
    ┣━━ <i py></i> constants.py
    ┣━━ <i folder></i> models/
    ┃   ┗━━ ...
    ┣━━ <i folder></i> sql/
    ┃   ┗━━ ...
    ┣━━ <i folder></i> static/
    ┃   ┣━━ <i folder></i> img/
    ┃   ┃   ┣━━ <i folder></i> logos/
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┣━━ <i folder></i> morpions/
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┗━━ <i folder></i> screenshots/
    ┃   ┃       ┗━━ ...
    ┃   ┣━━ <i folder></i> js/
    ┃   ┃   ┗━━ ...
    ┃   ┗━━ <i folder></i> styles/
    ┃       ┣━━ <i folder></i> components/
    ┃       ┃   ┗━━ ...
    ┃       ┣━━ <i folder></i> pages/
    ┃       ┃   ┗━━ ...
    ┃       ┣━━ <i css></i> base.css
    ┃       ┣━━ <i css></i> layout.css
    ┃       ┣━━ <i css></i> main.css
    ┃       ┗━━ <i css></i> utilities.css
    ┣━━ <i folder></i> templates/
    ┃   ┣━━ <i folder></i> base/
    ┃   ┃   ┗━━ ...
    ┃   ┣━━ <i folder></i> components/
    ┃   ┃   ┗━━ ...
    ┃   ┣━━ <i folder></i> macros/
    ┃   ┃   ┗━━ ...
    ┃   ┗━━ <i folder></i> pages/
    ┃       ┗━━ ...
    ┗━━ <i folder></i> controllers/
        ┗━━ ...
</pre>


### despues de hacer el git clone 

<pre>
<i project></i> project/
</pre>
### despues de hacer cd project y despues ls 

<pre>
<i project></i> project/
┣━━ <i py></i> server.py
┣━━ <i file></i> requirements.in
┣━━ <i toml></i> config-bd.toml
┣━━ <i toml></i> config-bd.toml.example
┣━━ <i folder></i> scripts/
┣━━ <i folder></i> docs/
┣━━ <i folder></i> tests/
┗━━ <i folder></i> website-morpion/
</pre>

### cuando vaya a hacer python server.py website-morpion/


<pre>
<i project></i> project/
┣━━ <i py></i> server.py
┣━━ <i file></i> requirements.in
┣━━ <i toml></i> config-bd.toml
┣━━ <i toml></i> config-bd.toml.example
┣━━ <i folder></i> scripts/
┃   ┗━━ ...
┣━━ <i folder></i> docs/
┃   ┗━━ ...
┣━━ <i folder></i> tests/
┃   ┗━━ ...
┗━━ <i folder></i> website-morpion/
    ┣━━ <i py></i> init.py
    ┣━━ <i toml></i> routes.toml
    ┣━━ <i py></i> constants.py
    ┣━━ <i folder></i> models/
    ┃   ┗━━ ...
    ┣━━ <i folder></i> sql/
    ┃   ┗━━ ...
    ┣━━ <i folder></i> static/
    ┃   ┣━━ <i folder></i> img/
    ┃   ┃   ┣━━ <i folder></i> logos/
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┣━━ <i folder></i> morpions/
    ┃   ┃   ┃   ┗━━ ...
    ┃   ┃   ┗━━ <i folder></i> screenshots/
    ┃   ┃       ┗━━ ...
    ┃   ┣━━ <i folder></i> js/
    ┃   ┃   ┗━━ ...
    ┃   ┗━━ <i folder></i> styles/
    ┃       ┣━━ <i folder></i> components/
    ┃       ┃   ┗━━ ...
    ┃       ┣━━ <i folder></i> pages/
    ┃       ┃   ┗━━ ...
    ┃       ┣━━ <i css></i> base.css
    ┃       ┣━━ <i css></i> layout.css
    ┃       ┣━━ <i css></i> main.css
    ┃       ┗━━ <i css></i> utilities.css
    ┣━━ <i folder></i> templates/
    ┃   ┣━━ <i folder></i> base/
    ┃   ┃   ┗━━ ...
    ┃   ┣━━ <i folder></i> components/
    ┃   ┃   ┗━━ ...
    ┃   ┣━━ <i folder></i> macros/
    ┃   ┃   ┗━━ ...
    ┃   ┗━━ <i folder></i> pages/
    ┃       ┗━━ ...
    ┗━━ <i folder></i> controllers/
        ┗━━ ...
</pre>