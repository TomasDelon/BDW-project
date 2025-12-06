# Plan de mejoras para README y EXPLICATION

## Objetivo general
Registrar los puntos que hoy sólo existen en documentos sueltos y que deberían integrarse oficialmente en `README.md` y `EXPLICATION.md` para que la preparación de la soutenance no dependa de archivos dispersos.

## Temas a cubrir

### 1. Uso del design system y utilidades CSS
- Explicar las variables declaradas en `base.css` (tamaños de imágenes, celdas, breakpoints) y cómo se aplican con ejemplos cortos.
- Documentar las clases utilitarias (`flex-*`, `grid-auto-fit`, badges, stats) y cuándo usarlas para evitar estilos inline.
- Resumir los macros clave (`team_badge`, `morpion_selector_card`, `progress_bar`) y su intención.

### 2. Funcionalidad "Statistiques avancées"
- Describir la arquitectura de la página (controller, repository, template, CSS dedicado) y la URL de acceso.
- Enumerar las diez estadísticas generadas y el valor pedagógico de cada una.
- Añadir una checklist de verificación (build CSS, ruta, datos mínimos) para validar el render antes de la defensa.

### 3. Procedimientos de prueba
- Añadir una sección con los comandos oficiales para correr simulaciones (`tests/simulate_cases.py`) y los unit tests (`tests/test_game_logic_avancee.py`).
- Explicar brevemente cuándo ejecutar cada comando (antes de commits, antes de la soutenance, tras refactors).

### 4. Backlog técnico y estado de refactors
- Resumir el backlog activo (por ejemplo lo que queda del `todo_analysis`) indicando qué tareas siguen pendientes y cómo afectan a la demo.
- Mencionar las grandes refactorizaciones ya entregadas (cache de sesión, helpers compartidos) para que el jurado tenga contexto sin revisar `CHANGES.md` completo.

### 5. Instalación y mantenimiento de la IA
- Integrar en README/EXPLICATION la guía actual para verificar la IA (scripts SQL ya ejecutados, comportamiento esperado, troubleshooting rápido).
- Incluir referencias al motor `ai_engine.py`, a los tests y al flujo "cuando es turno IA" para evitar confusiones con versiones antiguas.

## Plan de redacción
1. **Actualizar README.md**
   - Añadir subsección "Design System" dentro del capítulo de Views (explicaciones breves + enlace a ejemplos).
   - Crear sección "Tests & QA" con los comandos imprescindibles y la checklist de stats avanzadas.
   - Incorporar un resumen del estado de la IA en el Quickstart (instalación automática + pruebas básicas).
2. **Actualizar EXPLICATION.md**
   - Integrar un capítulo dedicado a la página de estadísticas (diagramas, queries, visualizaciones) reutilizando el material del doc actual.
   - Añadir un anexo sobre metodologías de refactor (qué se cambió en CSS/JS, motivación) y sobre el backlog pendiente.
   - Documentar la estrategia de design system en el apartado View con ejemplos concretos de macros y utilidades.
3. **Cruzar referencias**
   - En ambos archivos, enlazar explícitamente la sección de stats con la ruta `/statistiques-avancees` y mencionar que es parte del plan de soutenance.
   - Asegurar que toda mención a la IA o a scripts de prueba apunte a las mismas instrucciones para reducir la duplicidad en el futuro.
