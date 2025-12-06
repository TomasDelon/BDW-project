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
</style>

# Instalación guiada con dos vistas

1. **Árbol del proyecto** → muestra solo las carpetas/archivos necesarios para el paso (el resto se representa con `...`).
2. **Flujo del comando** → describe lo que hace la terminal usando el símbolo en forma de flecha escalonada para diferenciarlo del árbol del proyecto.

## 1. Clonar el repositorio

<pre class="cmd-block">
<i cmd></i> git clone &lt;url-del-repo&gt;
</pre>
<pre class="cmd-output">
Cloning into 'project'...
remote: Enumerating objects: 152, done.
remote: Total 152 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (152/152), done.
Resolving deltas: 100% (87/87), done.
</pre>

**Árbol implicado**

<pre class="tree">
<i project></i> project/
┣━━ <i toml></i> config-bd.toml.example
┣━━ <i folder></i> docs/
┃   ┗━━ ...
┣━━ <i folder></i> scripts/
┃   ┗━━ ...
┣━━ <i folder></i> website-morpion/
┃   ┗━━ ...
┗━━ <i file></i> requirements.in
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> git clone <url-del-repo>
    <c>#</c>└──➤ Usa tus llaves ~/.ssh o credenciales HTTPS
        <c>#</c>└──➤ Crea la carpeta local ./project con todo el código
</pre>

## 2. Entrar en la carpeta del proyecto

<pre class="cmd-block">
<i cmd></i> cd project
</pre>

**Árbol implicado**

<pre class="tree">
<i folder></i> ~/workspace/
┗━━ <i project></i> project/
    ┗━━ ...
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> cd project
    <c>#</c>└──➤ Actualiza $PWD para trabajar desde la raíz del repo
</pre>

## 3. Crear el entorno virtual

<pre class="cmd-block">
<i cmd></i> python3 -m venv .venv
</pre>

**Árbol implicado**

<pre class="tree">
<i project></i> project/
┣━━ <i folder></i> .venv/
┃   ┣━━ <i folder></i> bin/
┃   ┣━━ <i folder></i> lib/
┃   ┗━━ ...
┗━━ ...
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> python3 -m venv .venv
    <c>#</c>└──➤ Copia el intérprete de /usr/bin/python3
        <c>#</c>└──➤ Genera .venv/bin, .venv/lib y pyvenv.cfg aislados
</pre>

## 4. Activar el entorno virtual

<pre class="cmd-block">
<i cmd></i> source .venv/bin/activate
</pre>

**Árbol implicado**

<pre class="tree">
<i project></i> project/
┗━━ <i folder></i> .venv/
    ┣━━ ...
    ┗━━ <i folder></i> bin/
        ┗━━ <i py></i> activate
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> source .venv/bin/activate
    <c>#</c>└──➤ Ejecuta el script activate
        <c>#</c>└──➤ Exporta VIRTUAL_ENV y antepone .venv/bin al PATH
</pre>

## 5. Actualizar pip

<pre class="cmd-block">
<i cmd></i> python -m pip install --upgrade pip
</pre>
<pre class="cmd-output">
Requirement already satisfied: pip in ./lib/python3.11/site-packages (23.1.2)
Collecting pip
  Using cached pip-23.2.1-py3-none-any.whl (2.1 MB)
Installing collected packages: pip
Successfully installed pip-23.2.1
</pre>

**Árbol implicado**

<pre class="tree">
<i project></i> project/
┗━━ <i folder></i> .venv/
    ┣━━ <i folder></i> bin/
    ┃   ┣━━ <i py></i> python
    ┃   ┗━━ <i file></i> pip
    ┗━━ <i folder></i> lib/
        ┗━━ ...
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> python -m pip install --upgrade pip
    <c>#</c>└──➤ Usa el intérprete de .venv
        <c>#</c>└──➤ Sustituye el ejecutable pip por la versión más reciente
</pre>

## 6. Instalar dependencias

<pre class="cmd-block">
<i cmd></i> python -m pip install -r requirements.in
</pre>
<pre class="cmd-output">
Collecting flask==2.3.2
Collecting psycopg2-binary==2.9.9
Collecting bdw-server==0.7.0
Installing collected packages: psycopg2-binary, flask, bdw-server, ...
Successfully installed bdw-server-0.7.0 flask-2.3.2 psycopg2-binary-2.9.9
</pre>

**Árbol implicado**

<pre class="tree">
<i project></i> project/
┣━━ <i file></i> requirements.in
┗━━ <i folder></i> .venv/
    ┗━━ <i folder></i> lib/
        ┗━━ <i folder></i> python*/site-packages/
            ┗━━ ...
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> python -m pip install -r requirements.in
    <c>#</c>└──➤ Lee la lista de paquetes del fichero
        <c>#</c>└──➤ Instala dependencias en .venv/lib/.../site-packages
</pre>

## 7. Configurar credenciales BD

<pre class="cmd-block">
<i cmd></i> cp config-bd.toml.example config-bd.toml
</pre>

**Árbol implicado**

<pre class="tree">
<i project></i> project/
┣━━ <i toml></i> config-bd.toml.example
┗━━ <i toml></i> config-bd.toml
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> cp config-bd.toml.example config-bd.toml
    <c>#</c>└──➤ Duplica la plantilla
        <c>#</c>└──➤ Permite editar usuario/contraseña en config-bd.toml
</pre>

## 8. Crear el esquema SQL obligatorio

<pre class="cmd-block">
<i cmd></i> psql -h bd-pedago.univ-lyon1.fr -U pXXXXXXX -d pXXXXXXX -f website-morpion/sql/schema.sql
</pre>
<pre class="cmd-output">
SET
SET
CREATE TABLE
CREATE FUNCTION
CREATE VIEW
COMMIT
</pre>

**Árbol implicado**

<pre class="tree">
<i project></i> project/
┣━━ <i toml></i> config-bd.toml
┗━━ <i folder></i> website-morpion/
    ┗━━ <i folder></i> sql/
        ┣━━ <i sql></i> schema.sql
        ┗━━ ...
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> psql ... -f website-morpion/sql/schema.sql
    <c>#</c>└──➤ Usa las credenciales configuradas
        <c>#</c>└──➤ Ejecuta schema.sql contra PostgreSQL bd-pedago
</pre>

## 9. Registrar el equipo IA obligatorio

<pre class="cmd-block">
<i cmd></i> psql -h bd-pedago.univ-lyon1.fr -U pXXXXXXX -d pXXXXXXX -f website-morpion/sql/add_ai_team.sql
</pre>
<pre class="cmd-output">
INSERT 0 1
INSERT 0 1
COMMIT
</pre>

**Árbol implicado**

<pre class="tree">
<i project></i> project/
┗━━ <i folder></i> website-morpion/
    ┗━━ <i folder></i> sql/
        ┣━━ <i sql></i> add_ai_team.sql
        ┗━━ ...
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> psql ... -f website-morpion/sql/add_ai_team.sql
    <c>#</c>└──➤ Se conecta al mismo host BD
        <c>#</c>└──➤ Inserta el equipo IA para las partidas avanzadas
</pre>

## 10. (Opcional) Datos de demostración

<pre class="cmd-block">
<i cmd></i> python scripts/db_init.py --reset
</pre>
<pre class="cmd-output">
[db_init] Dropping schema morpion...
[db_init] Creating schema...
[db_init] Loading demo teams & games...
[db_init] Done.
</pre>

**Árbol implicado**

<pre class="tree">
<i project></i> project/
┣━━ <i py></i> scripts/db_init.py
┣━━ <i toml></i> config-bd.toml
┗━━ <i folder></i> website-morpion/
    ┗━━ ...
</pre>

**Flujo del comando**

<pre class="cmd-tree">
<i cmd></i> python scripts/db_init.py --reset
    <c>#</c>└──➤ Lee la configuración BD
        <c>#</c>└──➤ Limpia tablas y carga datos de ejemplo en PostgreSQL
</pre>

Con esta doble visualización puedes ubicar rápidamente qué parte del árbol del proyecto interviene y qué efecto tiene cada comando en la terminal.
