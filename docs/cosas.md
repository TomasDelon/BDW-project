<script src="https://kit.fontawesome.com/9ef4105ff0.js" crossorigin="anonymous"></script>

<style>
.placeholder-icon {
  color: #1f2933;
  font-size: 1rem;
  width: 1em;
}
</style>

# Font Awesome placeholders sin HTML visible

El archivo solo contiene marcadores como `::html`, `::js` o `::python`. Un script que se ejecuta automáticamente cuando se renderiza el preview convierte esas cadenas en `<i class="fa-...">` antes de mostrarlo, de modo que:

1. En el editor ves únicamente los placeholders (`::html`, `::js`, …).  
2. En el preview se muestran los iconos reales gracias al script incluido abajo.  

## Ejemplo

<pre>
📁 project
├── ::html docs
├── ::js scripts
└── ::python server.py
</pre>

Por ahora esa es la sintaxis que debes usar: escribe `::html` para obtener el icono de HTML5, `::js` para JavaScript, etc. El script reemplaza los marcadores de manera automática, no necesitas ejecutar nada extra; basta con guardar y refrescar el preview.

## Cómo extender el mapa de iconos

Si quieres más iconos solo tienes que ampliar `PLACEHOLDER_MAP` dentro del script: el mapeo entre el placeholder y la clase de Font Awesome define qué glyph se renderiza.

<script>
document.addEventListener("DOMContentLoaded", () => {
  const placeholderMap = {
    "::html": "fa-brands fa-html5",
    "::js": "fa-brands fa-js",
    "::python": "fa-brands fa-python",
  };

  const pattern = Object.keys(placeholderMap)
    .map((placeholder) => placeholder.replace(/[:]/g, "\\$&"))
    .join("|");

  const regex = new RegExp(pattern, "g");

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  const nodes = [];

  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (regex.test(node.nodeValue ?? "")) {
      nodes.push(node);
      regex.lastIndex = 0;
    }
  }

  for (const node of nodes) {
    if (!node.nodeValue) {
      continue;
    }

    const fragment = document.createDocumentFragment();
    let lastIndex = 0;
    for (const match of node.nodeValue.matchAll(regex)) {
      const placeholder = match[0];
      const index = match.index ?? 0;

      if (index > lastIndex) {
        fragment.appendChild(document.createTextNode(node.nodeValue.slice(lastIndex, index)));
      }

      const icon = document.createElement("i");
      icon.className = placeholderMap[placeholder] + " placeholder-icon";
      icon.setAttribute("aria-hidden", "true");
      fragment.appendChild(icon);

      lastIndex = index + placeholder.length;
    }

    if (lastIndex < node.nodeValue.length) {
      fragment.appendChild(document.createTextNode(node.nodeValue.slice(lastIndex)));
    }

    node.replaceWith(fragment);
  }
});
</script>

Cuando el preview cargue Font Awesome, el script reemplaza automáticamente los `::placeholder` por los iconos correspondientes y tú sigues viendo esos marcadores en el editor. Si necesitas más iconos, basta con añadir el nuevo placeholder (por ejemplo `::css`) y registrarlo en `PLACEHOLDER_MAP` con la clase Font Awesome que quieras usar.
