# Plan de Tests Pendientes

## 1. Lógica Modo Normal (`game_logic_normale.py`)
1.1 Victoria y empate
- Test filas/columnas/diagonales para grillas 3×3 y 4×4.
- Empate por grilla llena y por `max_turns`.
1.2 Validaciones
- Coordenadas fuera de rango, morpion ya usado, selección sin morpion.
- Estado SESSION actualizado correctamente (turno, ganador, logs).

## 2. Repositorios SQL
2.1 `team_repository`
- Creación de equipo válida (6-8 morpions, couleur unique).
- Errores esperados: color duplicado, <6 morpions.
2.2 `game_repository`
- Crear partida + config + logs; verificar `log_num` incremental.
- Actualizar ganador y ended_at.
2.3 `advanced_stats_repository`
- Retornos ordenados, manejo de BD vacía, cálculo de pourcentages sin division by zero.

## 3. Controladores
3.1 Tests funcionales
- `/equipe` GET/POST: REQUEST_VARS pobladas, errores en formularios.
- `/partie` POST: creación, clamps de `grid_size`/`max_turns`.
- `/partie-avancee` AJAX: respuesta JSON/fragment válida.
3.2 Integración SESSION
- Verificar que SESSION se crea/sincroniza (`game_<id>`), logs marcados dirty.

## 4. IA & Integración
4.1 Ampliar `test_ai_engine.py`
- Añadir casos 4×4, empates, turno sin movimientos.
4.2 Test end-to-end vs IA
- Simular partida con controllers + AI (sin BD, usando fixtures en memoria).

## 5. Scripts utilitarios
5.1 `db_backup.py`, `db_restore.py`, `db_wipe.py`
- Mock `subprocess.run` para asegurar comandos correctos y manejo de errores.
5.2 `build_css.py`
- Smoke test: generar main.css en tmp y verificar que incluye fuentes esperadas.

## 6. Simulador → Tests automatizados
- Convertir `tests/simulate_cases.py` en tests con asserts (p.ej. `test_simulate_cases.py`).
- Añadir casos: stalemate, armageddon sobre cellule détruite, mana insuficiente, tour sin acciones válidas.

## 7. Cobertura Frontend (opcional)
- Tests Jinja (render macros claves con contextos).  
- Validar orden de `CSS_SOURCES` en `build_css.py`.

## 8. Ejecución y reporting
- Documentar en `CHANGES.md` cada suite añadida.  
- Actualizar README/documentación con comandos de tests recién creados.
