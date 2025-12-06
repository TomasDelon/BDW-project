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
  --logo-terminal: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect x='1' y='2' width='14' height='12' rx='2' ry='2' fill='%23000' stroke='%2300c853' stroke-width='0.8'/%3E%3Cpath d='M4 6l2 2-2 2' stroke='%23fff' stroke-width='1.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M8 10h4' stroke='%23fff' stroke-width='1.2' stroke-linecap='round'/%3E%3C/svg%3E");
  --logo-db: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cellipse cx='8' cy='3.5' rx='6.5' ry='2.5' fill='%232196f3'/%3E%3Cpath d='M1.5 3.5v8c0 1.4 2.9 2.5 6.5 2.5s6.5-1.1 6.5-2.5v-8' fill='%232196f3' stroke='%230c47a1' stroke-width='0.8'/%3E%3Cline x1='1.5' y1='7' x2='14.5' y2='7' stroke='%230c47a1' stroke-width='0.6'/%3E%3Cline x1='1.5' y1='10.5' x2='14.5' y2='10.5' stroke='%230c47a1' stroke-width='0.6'/%3E%3C/svg%3E");
  --logo-linux: url("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg");
  --logo-windows: url("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/windows8/windows8-original.svg");
  --logo-mac: url("https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apple/apple-original.svg");
  --logo-model: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Crect width='20' height='20' rx='3' ry='3' fill='%230d0d16'/%3E%3Cpath d='M2.5 3.5h15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M2.5 6.5h15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M2.5 9.5h15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M2.5 12.5h15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M2.5 15.5h15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M3.5 2.5v15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M6.5 2.5v15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M9.5 2.5v15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M12.5 2.5v15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M15.5 2.5v15' stroke='%23262a3b' stroke-width='0.6'/%3E%3Cpath d='M4.2 4.2h6.2v6.2H4.2z' fill='none' stroke='%23d0d5e0' stroke-width='2.2' stroke-linejoin='round'/%3E%3Cpath d='M11.8 11.4h4.2v4.2h-4.2z' fill='none' stroke='%23d0d5e0' stroke-width='2.2' stroke-linejoin='round'/%3E%3C/svg%3E");
  --logo-view: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Crect x='2.5' y='4' width='15' height='12' rx='1.8' ry='1.8' fill='none' stroke='%23000' stroke-width='1.4'/%3E%3Crect x='2.5' y='4' width='15' height='3' rx='1.4' ry='1.4' fill='%23000'/%3E%3Ccircle cx='5' cy='5.5' r='0.8' fill='%23fff'/%3E%3Ccircle cx='7' cy='5.5' r='0.8' fill='%23fff'/%3E%3Ccircle cx='9' cy='5.5' r='0.8' fill='%23fff'/%3E%3Crect x='5.5' y='9' width='9' height='4.5' rx='0.8' ry='0.8' fill='%23000'/%3E%3C/svg%3E");
  --logo-controller: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath d='M10 3.2l.8 1.7c.6.1 1.3.4 1.8.9l1.8-.6 1.4 1.4-.6 1.8c.3.6.4 1.2.4 1.9s-.1 1.3-.4 1.9l.6 1.8-1.4 1.4-1.8-.6c-.5.5-1.2.8-1.8.9l-.8 1.7h-1.8l-.8-1.7c-.6-.1-1.3-.4-1.8-.9l-1.8.6-1.4-1.4.6-1.8C4.1 12.5 4 11.9 4 11.2s.1-1.3.4-1.9L3.8 7.5l1.4-1.4 1.8.6c.5-.5 1.2-.8 1.8-.9l.8-1.7z' fill='none' stroke='%23000' stroke-width='1.3' stroke-linejoin='round'/%3E%3Ccircle cx='10' cy='10' r='2.4' fill='%23000'/%3E%3Ccircle cx='10' cy='10' r='1.2' fill='%23fff'/%3E%3C/svg%3E");
  --badge-surface:#f3f5fa;
  --badge-border:rgba(15,23,42,0.12);
  --badge-text:#1f2933;
  --badge-os-bg:rgba(30,136,229,0.12);
  --badge-os-fg:#0d47a1;
  --badge-level-bg:rgba(255,193,7,0.18);
  --badge-level-fg:#8d6e00;
  --badge-role-bg:rgba(76,175,80,0.12);
  --badge-role-fg:#1b5e20;
  --badge-mvc-bg:rgba(236,64,122,0.12);
  --badge-mvc-fg:#880e4f;
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
i[cmd]{ background-image: var(--logo-terminal); }
i[db]{ background-image: var(--logo-db); }
i[linux]{ background-image: var(--logo-linux); }
i[windows]{ background-image: var(--logo-windows); }
i[mac]{ background-image: var(--logo-mac); }
i[model]{ background-image: var(--logo-model); }
i[view]{ background-image: var(--logo-view); }
i[controller]{ background-image: var(--logo-controller); }

@media (prefers-color-scheme: dark){
  :root{
    --badge-surface:rgba(255,255,255,0.04);
    --badge-border:rgba(255,255,255,0.18);
    --badge-text:#f5f5f5;
    --badge-os-bg:rgba(100,181,246,0.18);
    --badge-os-fg:#d0e7ff;
    --badge-level-bg:rgba(255,214,102,0.18);
    --badge-level-fg:#ffecb3;
    --badge-role-bg:rgba(129,199,132,0.18);
    --badge-role-fg:#e8f5e9;
    --badge-mvc-bg:rgba(244,143,177,0.18);
    --badge-mvc-fg:#ffe4ec;
  }
}

pre.tree{
  background:#efefef;
  padding:12px;
  border-radius:6px;
  overflow:auto;
  margin-bottom:8px;
}

pre.cmd-tree{
  background:#050505;
  color:#f2f2f2;
  padding:12px;
  border-radius:6px;
  margin-bottom:32px;
}

pre.cmd-block{
  background:#1f1f1f;
  color:#f2f2f2;
  padding:10px 12px;
  border-radius:6px;
  margin-bottom:8px;
}

pre.cmd-tree c{
  color:#050505;
}

pre.cmd-output{
  background:#141414;
  color:#8de2ff;
  padding:10px 12px;
  border-radius:6px;
  margin-bottom:16px;
  font-size:0.95em;
}

.warning-block{
  background:#2b0410;
  color:#ff8a80;
  border-left:4px solid #ff1744;
  padding:12px 14px;
  border-radius:6px;
  margin:16px 0 8px;
}

.placeholder-table{
  width:100%;
  border-collapse:collapse;
  margin:8px 0 16px;
  font-size:0.95em;
}

.placeholder-table th,
.placeholder-table td{
  border:1px solid #ddd;
  padding:6px 8px;
  text-align:left;
}
.error-block{
  background:#2b040a;
  color:#ffcdd2;
  border-left:4px solid #f44336;
  padding:12px 14px;
  border-radius:6px;
  margin:16px 0 20px;
  box-shadow:0 2px 6px rgba(0,0,0,0.25);
}

.error-block strong{
  color:#ffe5e9;
}

.error-block strong::before{
  content:"⛔ ";
}

.error-block ul{
  margin:8px 0 0 20px;
  padding:0;
}

.error-block li{
  margin-bottom:8px;
  line-height:1.45;
}

.badge-row{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
  margin:8px 0 18px;
}

.badge{
  display:inline-flex;
  align-items:center;
  gap:6px;
  padding:4px 10px;
  border-radius:999px;
  font-size:0.85em;
  text-transform:uppercase;
  letter-spacing:0.05em;
  background:var(--badge-surface);
  border:1px solid var(--badge-border);
  color:var(--badge-text);
  box-shadow:0 2px 6px rgba(15,15,15,0.08);
}

.badge i{
  margin-right:2px;
}

.badge-os{
  background:var(--badge-os-bg);
  border-color:var(--badge-os-fg);
  color:var(--badge-os-fg);
}

.badge-level{
  background:var(--badge-level-bg);
  border-color:var(--badge-level-fg);
  color:var(--badge-level-fg);
}

.badge-role{
  background:var(--badge-role-bg);
  border-color:var(--badge-role-fg);
  color:var(--badge-role-fg);
}

.badge-mvc{
  background:var(--badge-mvc-bg);
  border-color:var(--badge-mvc-fg);
  color:var(--badge-mvc-fg);
}

.badge-basico,
.badge-intermedio,
.badge-avanzado{
  font-weight:600;
  color:inherit;
}
</style>

# Manual de redacción (directivas iniciales)

Estas directrices definen el formato mínimo que debemos seguir cuando generemos documentación detallada. Se amplía con nuevas reglas según avancemos.

## Directiva #1 – Comandos siempre explicados con flechas
<div class="badge-row">
  <span class="badge badge-os"><i linux></i>Linux</span>
  <span class="badge badge-os"><i windows></i>Windows</span>
  <span class="badge badge-os"><i mac></i>macOS</span>
  <span class="badge badge-level badge-intermedio">Nivel: Intermedio</span>
  <span class="badge badge-role badge-dev">Rol: Dev</span>
  <span class="badge badge-role badge-bd">Rol: BD</span>
  <span class="badge badge-mvc"><i model></i>Model</span>
  <span class="badge badge-mvc"><i view></i>View/Vue</span>
  <span class="badge badge-mvc">⚙️ Controller</span>
</div>

- Cualquier comando que el lector deba ejecutar **debe incluir** un bloque de flujo con codos (ver guía `docs/guia_bloques.md` sección 6, referencia # [1]).
- El bloque debe indicar claramente:
  - El comando en sí (copiable).
  - Cada paso o subproceso desencadenado usando los símbolos `└──➤` y ramificaciones paralelas si aplica.
  - Comentarios precedidos por `<c>#</c>` para no romper copia/pega.
- **Ejemplo simple A (activar entorno)**  
  Código:
  ```html
  <pre class="cmd-tree">
  <i cmd></i> source .venv/bin/activate
      <c>#</c>└──➤ Exporta VIRTUAL_ENV
          <c>#</c>└──➤ Antepone .venv/bin al PATH
  </pre>
  ```
  Render:
  <pre class="cmd-tree">
  <i cmd></i> source .venv/bin/activate
      <c>#</c>└──➤ Exporta VIRTUAL_ENV
          <c>#</c>└──➤ Antepone .venv/bin al PATH
  </pre>

- **Ejemplo simple B (actualizar pip)**  
  Código:
  ```html
  <pre class="cmd-tree">
  <i cmd></i> python -m pip install --upgrade pip
      <c>#</c>└──➤ Usa el intérprete de .venv
          <c>#</c>└──➤ Sustituye el ejecutable pip
  </pre>
  ```
  Render:
  <pre class="cmd-tree">
  <i cmd></i> python -m pip install --upgrade pip
      <c>#</c>└──➤ Usa el intérprete de .venv
          <c>#</c>└──➤ Sustituye el ejecutable pip
  </pre>

- **Ejemplo complejo (make dev con procesos paralelos y condicionales)**  
  Código:
  ```html
  <pre class="cmd-tree">
  <i cmd></i> make dev
      <c>#</c>└──➤ Lanza npm run watch
          <c>#</c>└──➤ if (webpack falla?)
              <c>#</c>└─(true)─➤ Muestra log y reinicia watcher
              <c>#</c>└─(false)─➤ Continúa emitiendo bundles
      <c>#</c>└──➤ Arranca python server.py website-morpion
          <c>#</c>└──➤ Carga rutas.toml ───➤ Refresca SESSION ◄─┐
      <c>#</c>└──➤ Ejecuta scripts/build_css.py ───➤ Refresca SESSION ───┘
  </pre>
  ```
  Render:
  <pre class="cmd-tree">
  <i cmd></i> make dev
      <c>#</c>└──➤ Lanza npm run watch
          <c>#</c>└──➤ if (webpack falla?)
              <c>#</c>└─(true)─➤ Muestra log y reinicia watcher
              <c>#</c>└─(false)─➤ Continúa emitiendo bundles
      <c>#</c>└──➤ Arranca python server.py website-morpion
          <c>#</c>└──➤ Carga rutas.toml ───➤ Refresca SESSION ◄─┐
      <c>#</c>└──➤ Ejecuta scripts/build_css.py ───➤ Refresca SESSION ───┘
  </pre>

## Directiva #2 – Arboles de archivos antes/después de comandos que manipulan el sistema
<div class="badge-row">
  <span class="badge badge-os"><i linux></i>Linux</span>
  <span class="badge badge-os"><i windows></i>Windows</span>
  <span class="badge badge-os"><i mac></i>macOS</span>
  <span class="badge badge-level badge-basico">Nivel: Básico</span>
  <span class="badge badge-role badge-dev">Rol: Dev</span>
  <span class="badge badge-role badge-frontend">Rol: Frontend</span>
  <span class="badge badge-mvc"><i model></i>Model</span>
  <span class="badge badge-mvc"><i view></i>View/Vue</span>
  <span class="badge badge-mvc"><i controller></i>Controller</span>
</div>

- Cuando un comando cree, mueva o modifique archivos/carpetas, debemos mostrar el impacto usando árboles (como en `docs/tree.md`, referencia # [2]).
- Requisitos:
  - Incluir un árbol “antes” y otro “después” si el cambio lo justifica.
  - Resaltar únicamente las rutas relevantes; el resto se representa con `...`.
  - Mantener los mismos iconos `<i folder></i>`, `<i project></i>`, etc., para facilitar el reconocimiento visual.
- Esto ayuda a verificar que los resultados del comando coinciden con la expectativa.

### Ejemplos para la Directiva #2

- **Ejemplo simple A (crear entorno virtual)**  
  Código:
  ```html
  <pre class="tree">
  <i project></i> project/
  ┗━━ ...
  </pre>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> .venv/
  ┗━━ ...
  </pre>
  ```
  Render:
  <pre class="tree">
  <i project></i> project/
  ┗━━ ...
  </pre>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> .venv/
  ┗━━ ...
  </pre>

- **Ejemplo simple B (copiar config)**  
  Código:
  ```html
  <pre class="tree">
  <i project></i> project/
  ┗━━ <i toml></i> config-bd.toml.example
  </pre>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i toml></i> config-bd.toml
  ┗━━ <i toml></i> config-bd.toml.example
  </pre>
  ```
  Render:
  <pre class="tree">
  <i project></i> project/
  ┗━━ <i toml></i> config-bd.toml.example
  </pre>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i toml></i> config-bd.toml
  ┗━━ <i toml></i> config-bd.toml.example
  </pre>

- **Ejemplo complejo (ejecutar db_init con impacto múltiple)**  
  Código:
  ```html
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> website-morpion/sql/
  ┃   ┗━━ <i sql></i> schema.sql
  ┗━━ <i folder></i> backups/
      ┗━━ ...
  </pre>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> backups/
  ┃   ┗━━ <i file></i> db_init_2024-05-01.sql
  ┗━━ <i folder></i> website-morpion/sql/
      ┗━━ <i sql></i> schema.sql
  </pre>
  ```
  Render:
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> website-morpion/sql/
  ┃   ┗━━ <i sql></i> schema.sql
  ┗━━ <i folder></i> backups/
      ┗━━ ...
  </pre>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> backups/
  ┃   ┗━━ <i file></i> db_init_2024-05-01.sql
  ┗━━ <i folder></i> website-morpion/sql/
      ┗━━ <i sql></i> schema.sql
  </pre>

## Directiva #3 – Contexto visual para explicar código o estructuras
<div class="badge-row">
  <span class="badge badge-os"><i linux></i>Linux</span>
  <span class="badge badge-os"><i windows></i>Windows</span>
  <span class="badge badge-os"><i mac></i>macOS</span>
  <span class="badge badge-level badge-intermedio">Nivel: Intermedio</span>
  <span class="badge badge-role badge-dev">Rol: Dev</span>
  <span class="badge badge-role badge-frontend">Rol: Frontend</span>
  <span class="badge badge-mvc"><i model></i>Model</span>
  <span class="badge badge-mvc"><i view></i>View/Vue</span>
  <span class="badge badge-mvc"><i controller></i>Controller</span>
</div>

- Cada vez que describamos el contenido de una carpeta, módulo o conjunto de archivos, debemos incluir un árbol contextual siguiendo el mismo formato (referencia # [3]).
- Este árbol funciona como mapa mental para ubicar los archivos claves antes de entrar en el detalle del texto.
- Subpuntos:
  - Incluye todos los elementos necesarios para entender la explicación (por ejemplo, controllers, models, templates).
- Utiliza codos y `...` para omitir lo irrelevante sin perder el contexto global.

### Ejemplos para la Directiva #3

- **Ejemplo simple A (controllers)**  
  Código:
  ```html
  <pre class="tree">
  <i folder></i> controllers/
  ┣━━ <i py></i> home.py
  ┣━━ <i py></i> game.py
  ┗━━ ...
  </pre>
  ```
  Render:
  <pre class="tree">
  <i folder></i> controllers/
  ┣━━ <i py></i> home.py
  ┣━━ <i py></i> game.py
  ┗━━ ...
  </pre>

- **Ejemplo simple B (plantillas base)**  
  Código:
  ```html
  <pre class="tree">
  <i folder></i> templates/
  ┗━━ <i folder></i> base/
      ┣━━ <i html></i> base.html
      ┗━━ <i html></i> base_affiche.html
  </pre>
  ```
  Render:
  <pre class="tree">
  <i folder></i> templates/
  ┗━━ <i folder></i> base/
      ┣━━ <i html></i> base.html
      ┗━━ <i html></i> base_affiche.html
  </pre>

- **Ejemplo complejo (mapa completo de website-morpion)**  
  Código:
  ```html
  <pre class="tree">
  <i folder></i> website-morpion/
  ┣━━ <i folder></i> controllers/
  ┃   ┗━━ ...
  ┣━━ <i folder></i> models/
  ┃   ┗━━ ...
  ┣━━ <i folder></i> templates/
  ┃   ┗━━ <i folder></i> components/
  ┃       ┗━━ ...
  ┗━━ <i folder></i> static/
      ┣━━ <i folder></i> styles/
      ┗━━ ...
  </pre>
  ```
  Render:
  <pre class="tree">
  <i folder></i> website-morpion/
  ┣━━ <i folder></i> controllers/
  ┃   ┗━━ ...
  ┣━━ <i folder></i> models/
  ┃   ┗━━ ...
  ┣━━ <i folder></i> templates/
  ┃   ┗━━ <i folder></i> components/
  ┃       ┗━━ ...
  ┗━━ <i folder></i> static/
      ┣━━ <i folder></i> styles/
      ┗━━ ...
  </pre>

## Directiva #4 – Salida esperada tras cada comando
<div class="badge-row">
  <span class="badge badge-os"><i linux></i>Linux</span>
  <span class="badge badge-os"><i windows></i>Windows</span>
  <span class="badge badge-os"><i mac></i>macOS</span>
  <span class="badge badge-level badge-basico">Nivel: Básico</span>
  <span class="badge badge-role badge-dev">Rol: Dev</span>
  <span class="badge badge-role badge-bd">Rol: BD</span>
  <span class="badge badge-mvc"><i model></i>Model</span>
  <span class="badge badge-mvc"><i view></i>View/Vue</span>
  <span class="badge badge-mvc"><i controller></i>Controller</span>
</div>

- Después de cada bloque `<pre class="cmd-block">`, añade inmediatamente un `<pre class="cmd-output">` que muestre la salida típica.
- Si el comando no genera salida visible o no aplica, se puede omitir el bloque de output (pero debe mencionarse en la explicación).
- El objetivo es que el lector confirme rápidamente que obtuvo el mismo resultado sin ejecutar pasos extra.

### Ejemplos para la Directiva #4

- **Ejemplo simple A (git clone)**  
  Código:
  ```html
  <pre class="cmd-block">
  <i cmd></i> git clone &lt;url&gt;
  </pre>
  <pre class="cmd-output">
  Cloning into 'project'...
  Receiving objects: 100% (152/152), done.
  </pre>
  ```
  Render:
  <pre class="cmd-block">
  <i cmd></i> git clone &lt;url&gt;
  </pre>
  <pre class="cmd-output">
  Cloning into 'project'...
  Receiving objects: 100% (152/152), done.
  </pre>

- **Ejemplo simple B (actualizar pip)**  
  Código:
  ```html
  <pre class="cmd-block">
  <i cmd></i> python -m pip install --upgrade pip
  </pre>
  <pre class="cmd-output">
  Collecting pip
  Installing collected packages: pip
  Successfully installed pip-23.2.1
  </pre>
  ```
  Render:
  <pre class="cmd-block">
  <i cmd></i> python -m pip install --upgrade pip
  </pre>
  <pre class="cmd-output">
  Collecting pip
  Installing collected packages: pip
  Successfully installed pip-23.2.1
  </pre>

- **Ejemplo complejo (psql + resumen)**  
  Código:
```html
<pre class="cmd-block">
<i cmd></i> psql -h {{HOST}} -U {{USER}} -d {{DB}} -f schema.sql
</pre>
<pre class="cmd-output">
SET
CREATE TABLE
CREATE FUNCTION
COMMIT
</pre>
<div class="error-block">
  <strong>Errores frecuentes:</strong><br>
  <ul>
    <li><code>psql: FATAL: password authentication failed</code><br> ➔ Usuario o contraseña incorrectos. Revisa <code>{{USER}}</code>, la contraseña en <code>config-bd.toml</code> y vuelve a intentarlo.</li>
    <li><code>psql: could not connect to server</code><br> ➔ El host no responde o estás sin VPN. Comprueba <code>{{HOST}}</code> y tu conexión.</li>
  </ul>
</div>
```
Render:
<pre class="cmd-block">
<i cmd></i> psql -h {{HOST}} -U {{USER}} -d {{DB}} -f schema.sql
</pre>
<pre class="cmd-output">
SET
CREATE TABLE
CREATE FUNCTION
COMMIT
</pre>
<div class="error-block">
  <strong>Errores frecuentes:</strong><br>
  <ul>
    <li><code>psql: FATAL: password authentication failed</code><br> ➔ Usuario o contraseña incorrectos. Revisa <code>{{USER}}</code>, la contraseña en <code>config-bd.toml</code> y vuelve a intentarlo.</li>
    <li><code>psql: could not connect to server</code><br> ➔ El host no responde o estás sin VPN. Comprueba <code>{{HOST}}</code> y tu conexión.</li>
  </ul>
</div>

## Directiva #6 – Resaltado de riesgos
<div class="badge-row">
  <span class="badge badge-os"><i linux></i>Linux</span>
  <span class="badge badge-os"><i windows></i>Windows</span>
  <span class="badge badge-os"><i mac></i>macOS</span>
  <span class="badge badge-level badge-avanzado">Nivel: Avanzado</span>
  <span class="badge badge-role badge-dev">Rol: Dev</span>
  <span class="badge badge-role badge-bd">Rol: BD</span>
  <span class="badge badge-mvc"><i model></i>Model</span>
  <span class="badge badge-mvc"><i view></i>View/Vue</span>
  <span class="badge badge-mvc"><i controller></i>Controller</span>
</div>

- Comandos destructivos (DROP, `rm -rf`, `db_wipe`) deben precederse de un banner de advertencia.
- En los árboles relacionados, marca en rojo los archivos/carpeta afectados usando `<span style="color:#d32f2f">...</span>`.
- Evita repetir consecuencias: es preferible conectar múltiples procesos a un único nodo de “riesgo” mediante flechas convergentes.

### Ejemplos para la Directiva #6

- **Ejemplo simple A (eliminar carpeta tmp)**  
  Código:
  ```html
  <div class="warning-block">⚠️ Este comando eliminará definitivamente ./tmp.</div>
  <pre class="cmd-tree">
  <i cmd></i> rm -rf tmp
      <c>#</c>└──➤ Borra <span style="color:#d32f2f">tmp/</span>
  </pre>
  ```
  Render:
  <div class="warning-block">⚠️ Este comando eliminará definitivamente ./tmp.</div>
  <pre class="cmd-tree">
  <i cmd></i> rm -rf tmp
      <c>#</c>└──➤ Borra <span style="color:#d32f2f">tmp/</span>
  </pre>

- **Ejemplo simple B (DROP SCHEMA)**  
  Código:
  ```html
  <div class="warning-block">⚠️ DROP SCHEMA morpion CASCADE borrará todas las tablas.</div>
  <pre class="cmd-tree">
  <i cmd></i> psql ... -c "DROP SCHEMA morpion CASCADE"
      <c>#</c>└──➤ Remueve <span style="color:#d32f2f">morpion.*</span>
  </pre>
  <div class="error-block">
    <strong>Errores frecuentes:</strong><br>
    <ul>
      <li><code>ERROR: must be owner of schema morpion</code><br> ➔ El usuario conectado no es dueño. Repite con el owner o pide a la docencia que otorgue permisos.</li>
      <li><code>ERROR: schema "morpion" does not exist</code><br> ➔ El esquema ya fue eliminado o el nombre no coincide. Verifícalo con <code>\dn</code> antes de ejecutar el DROP.</li>
    </ul>
  </div>
  ```
  Render:
  <div class="warning-block">⚠️ DROP SCHEMA morpion CASCADE borrará todas las tablas.</div>
  <pre class="cmd-tree">
  <i cmd></i> psql ... -c "DROP SCHEMA morpion CASCADE"
      <c>#</c>└──➤ Remueve <span style="color:#d32f2f">morpion.*</span>
  </pre>
  <div class="error-block">
    <strong>Errores frecuentes:</strong><br>
    <ul>
      <li><code>ERROR: must be owner of schema morpion</code><br> ➔ El usuario conectado no es dueño. Repite con el owner o pide a la docencia que otorgue permisos.</li>
      <li><code>ERROR: schema "morpion" does not exist</code><br> ➔ El esquema ya fue eliminado o el nombre no coincide. Verifícalo con <code>\dn</code> antes de ejecutar el DROP.</li>
    </ul>
  </div>

- **Ejemplo complejo (db_wipe con múltiples efectos)**  
  Código:
  ```html
  <div class="warning-block">⚠️ `python scripts/db_wipe.py` vacía la base y borra el último backup.</div>
  <pre class="cmd-tree">
  <i cmd></i> python scripts/db_wipe.py
      <c>#</c>└──➤ Confirma credenciales
      <c>#</c>└──➤ DROP SCHEMA morpion
      <c>#</c>└──➤ Elimina <span style="color:#d32f2f">backups/latest.sql</span>
  </pre>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> backups/
  ┃   ┗━━ <span style="color:#d32f2f"><i file></i> latest.sql</span>
  ┗━━ ...
  </pre>
  ```
  Render:
  <div class="warning-block">⚠️ `python scripts/db_wipe.py` vacía la base y borra el último backup.</div>
  <pre class="cmd-tree">
  <i cmd></i> python scripts/db_wipe.py
      <c>#</c>└──➤ Confirma credenciales
      <c>#</c>└──➤ DROP SCHEMA morpion
      <c>#</c>└──➤ Elimina <span style="color:#d32f2f">backups/latest.sql</span>
  </pre>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> backups/
  ┃   ┗━━ <span style="color:#d32f2f"><i file></i> latest.sql</span>
  ┗━━ ...
  </pre>

## Directiva #7 – Inputs parametrizables
<div class="badge-row">
  <span class="badge badge-os"><i linux></i>Linux</span>
  <span class="badge badge-os"><i windows></i>Windows</span>
  <span class="badge badge-os"><i mac></i>macOS</span>
  <span class="badge badge-level badge-intermedio">Nivel: Intermedio</span>
  <span class="badge badge-role badge-dev">Rol: Dev</span>
  <span class="badge badge-role badge-bd">Rol: BD</span>
  <span class="badge badge-mvc"><i model></i>Model</span>
  <span class="badge badge-mvc"><i view></i>View/Vue</span>
  <span class="badge badge-mvc"><i controller></i>Controller</span>
</div>

- Usa placeholders `{{PLACEHOLDER}}` para cualquier valor que el lector deba personalizar.
- Añade una tabla inmediatamente después del comando describiendo cada placeholder y un ejemplo válido.
- Esto reduce dudas y mantiene el bloque copiable.

### Ejemplos para la Directiva #7

- **Ejemplo simple A (psql)**  
  Código:
  ```html
  <pre class="cmd-block">
  <i cmd></i> psql -h {{HOST}} -U {{USER}} -d {{DB}} -f schema.sql
  </pre>
  <table class="placeholder-table">
    <tr><th>Placeholder</th><th>Descripción</th><th>Ejemplo</th></tr>
    <tr><td>{{HOST}}</td><td>Servidor PostgreSQL</td><td>bd-pedago.univ-lyon1.fr</td></tr>
    <tr><td>{{USER}}</td><td>Login BDW</td><td>p2023001</td></tr>
    <tr><td>{{DB}}</td><td>Base objetivo</td><td>p2023001</td></tr>
  </table>
  <div class="error-block">
    <strong>Errores frecuentes:</strong><br>
    <ul>
      <li><code>psql: FATAL: password authentication failed</code><br> ➔ Usuario/contraseña incorrectos. Confirma <code>{{USER}}</code> y la contraseña almacenada.</li>
      <li><code>psql: could not connect to server</code><br> ➔ Host inaccesible o VPN desconectada. Verifica <code>{{HOST}}</code> y la red.</li>
    </ul>
  </div>
  ```
  Render:
  <pre class="cmd-block">
  <i cmd></i> psql -h {{HOST}} -U {{USER}} -d {{DB}} -f schema.sql
  </pre>
  <table class="placeholder-table">
    <tr><th>Placeholder</th><th>Descripción</th><th>Ejemplo</th></tr>
    <tr><td>{{HOST}}</td><td>Servidor PostgreSQL</td><td>bd-pedago.univ-lyon1.fr</td></tr>
    <tr><td>{{USER}}</td><td>Login BDW</td><td>p2023001</td></tr>
    <tr><td>{{DB}}</td><td>Base objetivo</td><td>p2023001</td></tr>
  </table>
  <div class="error-block">
    <strong>Errores frecuentes:</strong><br>
    <ul>
      <li><code>psql: FATAL: password authentication failed</code><br> ➔ Usuario/contraseña incorrectos. Confirma <code>{{USER}}</code> y la contraseña almacenada.</li>
      <li><code>psql: could not connect to server</code><br> ➔ Host inaccesible o VPN desconectada. Verifica <code>{{HOST}}</code> y la red.</li>
    </ul>
  </div>

- **Ejemplo simple B (script con ruta de salida)**  
  Código:
  ```html
  <pre class="cmd-block">
  <i cmd></i> python scripts/db_backup.py --out {{OUTPUT_PATH}}
  </pre>
  <table class="placeholder-table">
    <tr><th>Placeholder</th><th>Descripción</th><th>Ejemplo</th></tr>
    <tr><td>{{OUTPUT_PATH}}</td><td>Ruta destino del backup</td><td>backups/morpion.sql</td></tr>
  </table>
  <div class="error-block">
    <strong>Errores frecuentes:</strong><br>
    <ul>
      <li><code>FileNotFoundError: [Errno 2] No such file or directory: '{{OUTPUT_PATH}}'</code><br> ➔ La carpeta destino no existe. Crea <code>$(dirname {{OUTPUT_PATH}})</code> antes de correr el script.</li>
      <li><code>psycopg2.OperationalError: connection to server ... failed</code><br> ➔ El script no logró conectarse a PostgreSQL. Revisa <code>config-bd.toml</code> y la VPN.</li>
    </ul>
  </div>
  ```
  Render:
  <pre class="cmd-block">
  <i cmd></i> python scripts/db_backup.py --out {{OUTPUT_PATH}}
  </pre>
  <table class="placeholder-table">
    <tr><th>Placeholder</th><th>Descripción</th><th>Ejemplo</th></tr>
    <tr><td>{{OUTPUT_PATH}}</td><td>Ruta destino del backup</td><td>backups/morpion.sql</td></tr>
  </table>
  <div class="error-block">
    <strong>Errores frecuentes:</strong><br>
    <ul>
      <li><code>FileNotFoundError: [Errno 2] No such file or directory: '{{OUTPUT_PATH}}'</code><br> ➔ La carpeta destino no existe. Crea <code>$(dirname {{OUTPUT_PATH}})</code> antes de correr el script.</li>
      <li><code>psycopg2.OperationalError: connection to server ... failed</code><br> ➔ El script no logró conectarse a PostgreSQL. Revisa <code>config-bd.toml</code> y la VPN.</li>
    </ul>
  </div>

- **Ejemplo complejo (docker compose parametrizado)**  
  Código:
  ```html
  <pre class="cmd-block">
  <i cmd></i> docker compose --env-file {{ENV_FILE}} up -d {{SERVICE}}
  </pre>
  <table class="placeholder-table">
    <tr><th>Placeholder</th><th>Descripción</th><th>Ejemplo</th></tr>
    <tr><td>{{ENV_FILE}}</td><td>Archivo .env a cargar</td><td>.env.dev</td></tr>
    <tr><td>{{SERVICE}}</td><td>Servicio específico (opcional)</td><td>frontend</td></tr>
  </table>
  <div class="error-block">
    <strong>Errores frecuentes:</strong><br>
    <ul>
      <li><code>Error: Couldn't find env file: {{ENV_FILE}}</code><br> ➔ La ruta del .env es incorrecta. Ajusta el nombre o crea el archivo antes de levantar los servicios.</li>
      <li><code>No such service: {{SERVICE}}</code><br> ➔ El servicio no existe en <code>docker-compose.yml</code>. Corrige el placeholder o ejecuta sin el flag.</li>
    </ul>
  </div>
  ```
  Render:
  <pre class="cmd-block">
  <i cmd></i> docker compose --env-file {{ENV_FILE}} up -d {{SERVICE}}
  </pre>
  <table class="placeholder-table">
    <tr><th>Placeholder</th><th>Descripción</th><th>Ejemplo</th></tr>
    <tr><td>{{ENV_FILE}}</td><td>Archivo .env a cargar</td><td>.env.dev</td></tr>
    <tr><td>{{SERVICE}}</td><td>Servicio específico (opcional)</td><td>frontend</td></tr>
  </table>
  <div class="error-block">
    <strong>Errores frecuentes:</strong><br>
    <ul>
      <li><code>Error: Couldn't find env file: {{ENV_FILE}}</code><br> ➔ La ruta del .env es incorrecta. Ajusta el nombre o crea el archivo antes de levantar los servicios.</li>
      <li><code>No such service: {{SERVICE}}</code><br> ➔ El servicio no existe en <code>docker-compose.yml</code>. Corrige el placeholder o ejecuta sin el flag.</li>
    </ul>
  </div>

## Directiva #8 – Resumen final por sección
<div class="badge-row">
  <span class="badge badge-os"><i linux></i>Linux</span>
  <span class="badge badge-os"><i windows></i>Windows</span>
  <span class="badge badge-os"><i mac></i>macOS</span>
  <span class="badge badge-level badge-basico">Nivel: Básico</span>
  <span class="badge badge-role badge-dev">Rol: Dev</span>
  <span class="badge badge-role badge-frontend">Rol: Frontend</span>
  <span class="badge badge-mvc"><i model></i>Model</span>
  <span class="badge badge-mvc"><i view></i>View/Vue</span>
  <span class="badge badge-mvc"><i controller></i>Controller</span>
</div>

- Al finalizar cada **bloque significativo** (ej. “instalación de dependencias”, “preparar BD”), redacta un breve párrafo + opcionalmente **un solo árbol** que explique qué se hizo y qué se logró.
- No es necesario hacerlo tras cada paso; solo cuando se cierra un hito importante.
- La idea es ofrecer una síntesis narrativa (“Ahora contamos con…”) que ayude al lector a entender el progreso antes de avanzar.

### Ejemplos para la Directiva #8

- **Ejemplo simple A (tras crear el entorno virtual)**  
  Código:
  ```html
  <p>Tras estos pasos ya contamos con un entorno aislado (.venv) listo para instalar dependencias sin afectar el sistema.</p>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> .venv/
  ┗━━ ...
  </pre>
  ```
  Render:
  <p>Tras estos pasos ya contamos con un entorno aislado (.venv) listo para instalar dependencias sin afectar el sistema.</p>
  <pre class="tree">
  <i project></i> project/
  ┣━━ <i folder></i> .venv/
  ┗━━ ...
  </pre>

- **Ejemplo simple B (después de instalar requirements)**  
  Código:
  ```html
  <p>La lista de paquetes base quedó instalada dentro de .venv; podemos verificarla en site-packages.</p>
  <pre class="tree">
  <i folder></i> .venv/lib/python*/site-packages/
  ┣━━ <i folder></i> flask/
  ┣━━ <i folder></i> psycopg2_binary-2.9.9.dist-info/
  ┗━━ ...
  </pre>
  ```
  Render:
  <p>La lista de paquetes base quedó instalada dentro de .venv; podemos verificarla en site-packages.</p>
  <pre class="tree">
  <i folder></i> .venv/lib/python*/site-packages/
  ┣━━ <i folder></i> flask/
  ┣━━ <i folder></i> psycopg2_binary-2.9.9.dist-info/
  ┗━━ ...
  </pre>

- **Ejemplo complejo (post `make dev`)**  
  Código:
  ```html
  <p>Con `make dev` dejamos corriendo el watcher de assets y el servidor Flask, además de recompilar las hojas de estilo.</p>
  <pre class="tree">
  <i folder></i> project/
  ┣━━ <i folder></i> website-morpion/static/styles/
  ┃   ┗━━ <i css></i> main.css
  ┗━━ <i file></i> server.py (listening 4242)
  </pre>
  ```
  Render:
  <p>Con `make dev` dejamos corriendo el watcher de assets y el servidor Flask, además de recompilar las hojas de estilo.</p>
  <pre class="tree">
  <i folder></i> project/
  ┣━━ <i folder></i> website-morpion/static/styles/
  ┃   ┗━━ <i css></i> main.css
  ┗━━ <i file></i> server.py (listening 4242)
  </pre>

---

Estas tres reglas son obligatorias mientras no se especifique lo contrario. Las próximas directivas se añadirán sobre este mismo archivo para mantener todo el manual en un solo lugar.
