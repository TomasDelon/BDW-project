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
</style>

# Guía rápida para los bloques visuales

Esta guía resume cómo reproducir los bloques que usamos en `docs/instalacion.md` para documentar comandos con árboles e iconos pedagógicos.

## 1. Componentes disponibles

| Bloque | Uso | Clase CSS | Notas |
| --- | --- | --- | --- |
| Comando puro | Mostrar la instrucción lista para copiar | `<pre class="cmd-block">` | Fondo gris `#1f1f1f`. Incluye el icono `<i cmd></i>` delante del comando. |
| Árvore de archivos | Mostrar qué carpetas/archivos son relevantes | `<pre class="tree">` | Fondo gris claro `#efefef`. Utiliza iconos `<i folder></i>`, `<i project></i>`, etc. |
| Flujo del comando | Explicar paso a paso qué hará la terminal | `<pre class="cmd-tree">` | Fondo gris casi negro `#050505`. Cada línea explicativa debe comenzar por `<c>#</c>` para que se copie como un comentario. |

> Si necesitas iconos adicionales, reutiliza los atributos de `<i …></i>` ya definidos en la cabecera de `docs/tree.md` y `docs/instalacion.md`.

## 2. Cómo escribir un paso completo

1. **Comando** (copiable):  
   ```html
   <pre class="cmd-block">
   <i cmd></i> python scripts/db_init.py --reset
   </pre>
   ```

2. **Árbol implicado** (opcional):  
   ```html
   <pre class="tree">
   <i project></i> project/
   ┣━━ <i py></i> scripts/db_init.py
   ┣━━ <i toml></i> config-bd.toml
   ┗━━ ...
   </pre>
   ```

3. **Flujo del comando** (comentado línea a línea):  
   ```html
   <pre class="cmd-tree">
   <i cmd></i> python scripts/db_init.py --reset
       <c>#</c>└──➤ Lee la configuración BD
           <c>#</c>└──➤ Limpia y rellena los datos de demo
   </pre>
   ```

## 3. Regla del caracter `#`

- Siempre que una línea del bloque `cmd-tree` **no sea el comando real**, antepón `<c>#</c>`.  
- La etiqueta `<c>` oculta el `#` en el fondo, pero cuando el lector copie el bloque, la línea seguirá empezando por `#` y la terminal la tratará como comentario.
- Ejemplo de salida tras copiar:
  ```
  python scripts/db_init.py --reset
  # └──➤ Lee la configuración BD
  #     └──➤ Limpia y rellena los datos de demo
  ```

## 4. Consejos de estilo

- Mantén la indentación de los árboles con los símbolos `┣━━`, `┗━━` y el carácter vertical `┃`.  
- Usa `...` para ocultar secciones irrelevantes del árbol.  
- En el flujo del comando limita cada bloque a 2 o 3 niveles para no saturar la lectura.

Con estas pautas puedes extender la documentación con la misma estética y mantener los bloques listos para copiar/pegar sin romper la experiencia del usuario.

## 5. Qué significan los “codos” `└──➤`

- **Serie directa**  
  ```
  └──➤ Paso A
      └──➤ Paso B
  ```
  Paso B ocurre porque Paso A lo lanza. Lo usamos para describir llamadas, subprocesos o acciones dentro del mismo comando.

- **Varios codos alineados**  
  ```
  └──➤ Paso A
  └──➤ Paso B
  ```
  Ambos pasos se disparan de forma independiente (o paralela) tras ejecutar el comando. Sirve para mostrar tareas simultáneas como “compila front” y “compila back”.

- **Codos complejos con condiciones o convergencias**  
  ```
  └──➤ Proceso A
          └──➤ if (condición)
                     └─(true)─➤ ...
                     └─(false)─➤ ...
  └──➤ Proceso B ───➤ Proceso D ◄─┐
  └──➤ Proceso C ───➤ Proceso E ───┘
  ```
  Aquí mostramos ramificaciones condicionales (true/false) y también convergencias donde varios procesos alimentan un mismo resultado (flechas laterales `◄─┐`, `─┘`).

## 6. Ejemplos de casos de uso

### 6.1 Ejemplo básico – Actualizar `pip`

**Render**

<pre class="cmd-tree">
<i cmd></i> python -m pip install --upgrade pip
    <c>#</c>└──➤ Usa el intérprete aislado de .venv
        <c>#</c>└──➤ Reemplaza el ejecutable pip con la última versión
</pre>

**Código**

```html
<pre class="cmd-tree">
<i cmd></i> python -m pip install --upgrade pip
    <c>#</c>└──➤ Usa el intérprete aislado de .venv
        <c>#</c>└──➤ Reemplaza el ejecutable pip con la última versión
</pre>
```

### 6.2 Ejemplo paralelo – Construir assets y servidor

**Render**

<pre class="cmd-tree">
<i cmd></i> make dev
    <c>#</c>└──➤ Lanza `npm run watch` (frontend)
    <c>#</c>└──➤ Arranca `python server.py website-morpion`
</pre>

**Código**

```html
<pre class="cmd-tree">
<i cmd></i> make dev
    <c>#</c>└──➤ Lanza `npm run watch` (frontend)
    <c>#</c>└──➤ Arranca `python server.py website-morpion`
</pre>
```

### 6.3 Ejemplo “llamada” – Subproceso dependiente

**Render**

<pre class="cmd-tree">
<i cmd></i> python scripts/db_backup.py
    <c>#</c>└──➤ Verifica conexión PostgreSQL
        <c>#</c>└──➤ Ejecuta `pg_dump` y guarda el archivo
</pre>

**Código**

```html
<pre class="cmd-tree">
<i cmd></i> python scripts/db_backup.py
    <c>#</c>└──➤ Verifica conexión PostgreSQL
        <c>#</c>└──➤ Ejecuta `pg_dump` y guarda el archivo
</pre>
```

### 6.4 Ejemplo condicional y convergente

**Render**

<pre class="cmd-tree">
<i cmd></i> python scripts/db_init.py --reset
    <c>#</c>└──➤ Lee config-bd.toml
        <c>#</c>└──➤ if (schema existe?)
            <c>#</c>└─(true)─➤ Limpia tablas existentes
            <c>#</c>└─(false)─➤ Crea esquema desde schema.sql
    <c>#</c>└──➤ Inserta datos de demo ───➤ Actualiza contadores ◄─┐
    <c>#</c>└──➤ Genera IA de ejemplo ───➤ Actualiza contadores ───┘
</pre>

**Código**

```html
<pre class="cmd-tree">
<i cmd></i> python scripts/db_init.py --reset
    <c>#</c>└──➤ Lee config-bd.toml
        <c>#</c>└──➤ if (schema existe?)
            <c>#</c>└─(true)─➤ Limpia tablas existentes
            <c>#</c>└─(false)─➤ Crea esquema desde schema.sql
    <c>#</c>└──➤ Inserta datos de demo ───➤ Actualiza contadores ◄─┐
    <c>#</c>└──➤ Genera IA de ejemplo ───➤ Actualiza contadores ───┘
</pre>
```

### 6.5 Ejemplo completo (comando + árbol + flujo)

**Render**

<pre class="cmd-block">
<i cmd></i> psql -h bd-pedago.univ-lyon1.fr -U pXXXXXXX -d pXXXXXXX -f website-morpion/sql/schema.sql
</pre>
<pre class="tree">
<i project></i> project/
┗━━ <i folder></i> website-morpion/
    ┗━━ <i folder></i> sql/
        ┗━━ <i sql></i> schema.sql
</pre>
<pre class="cmd-tree">
<i cmd></i> psql ... schema.sql
    <c>#</c>└──➤ Lee credenciales desde config-bd.toml
        <c>#</c>└──➤ Establece conexión con bd-pedago
            <c>#</c>└──➤ Ejecuta archivo schema.sql
</pre>

**Código**

```html
<pre class="cmd-block">
<i cmd></i> psql -h bd-pedago.univ-lyon1.fr -U pXXXXXXX -d pXXXXXXX -f website-morpion/sql/schema.sql
</pre>
<pre class="tree">
<i project></i> project/
┗━━ <i folder></i> website-morpion/
    ┗━━ <i folder></i> sql/
        ┗━━ <i sql></i> schema.sql
</pre>
<pre class="cmd-tree">
<i cmd></i> psql ... schema.sql
    <c>#</c>└──➤ Lee credenciales desde config-bd.toml
        <c>#</c>└──➤ Establece conexión con bd-pedago
            <c>#</c>└──➤ Ejecuta archivo schema.sql
</pre>
```

Con estos ejemplos puedes crear desde explicaciones simples hasta flujos complejos con condicionales, procesos paralelos y convergencias, manteniendo siempre el formato copiable y autodocumentado.
