"""
Funciones de lógica de juego para partie avancée (Fonctionnalité 4).
Implementa sistema de combate con probabilidades, hechizos y eliminación.

Todas las funciones son puras (sin efectos secundarios ni acceso a BD),
lo que facilita testing y razonamiento sobre el comportamiento del juego.
"""

import random

# Constantes de balanceo de probabilidades de éxito
# Estos valores fueron ajustados para reducir la frustración del jugador
# manteniendo un elemento de aleatoriedad interesante.
DEFAULT_SUCCESS_RATE_SCALE = 1.6  # Multiplica accuracy para amplificar diferencias
DEFAULT_SUCCESS_RATE_FLAT_BONUS = 10.0  # Bonus base para evitar demasiados fallos

# Contexto de balanceo:
# - Sin bonificación: accuracy=5 → 50% éxito (demasiados fallos)
# - Con estos valores: accuracy=5 → (5*1.6)+10 = 18% → min(18, 100) = 18% éxito
# - Morpion fuerte (accuracy=8): (8*1.6)+10 = 22.8% éxito
# El sistema favorece ligeramente a los morpions con alta accuracy

try:
    from constants import SUCCESS_RATE_SCALE, SUCCESS_RATE_FLAT_BONUS
except ImportError:
    SUCCESS_RATE_SCALE = DEFAULT_SUCCESS_RATE_SCALE
    SUCCESS_RATE_FLAT_BONUS = DEFAULT_SUCCESS_RATE_FLAT_BONUS


def calculate_success_probability(accuracy):
    """
    Calcula la probabilidad de éxito de una acción.
    Soporta valores en escala 0-10 (multiplicados por 10) o 0-100 directement.
    Aplica luego un bonus global para reducir la cantidad de fallos (paramétrable via constantes).
    """
    if accuracy is None:
        return 0.0
    try:
        accuracy_value = float(accuracy)
    except (TypeError, ValueError):
        return 0.0

    if accuracy_value <= 10:
        probability = accuracy_value * 10.0
    else:
        probability = accuracy_value

    # Ajuste aprobado para reducir fallos: se aplica un multiplicador y un bonus fijo
    probability = (probability * SUCCESS_RATE_SCALE) + SUCCESS_RATE_FLAT_BONUS

    return max(0.0, min(probability, 100.0))


def roll_action_success(accuracy):
    """
    Genera un valor aleatorio y verifica si la acción es exitosa.
    
    Args:
        accuracy: puntos de réussite (current_accuracy)
    
    Returns:
        bool: True si la acción es exitosa, False en caso contrario
    """
    probability = calculate_success_probability(accuracy)
    roll = random.uniform(0, 100)
    return roll < probability


def can_attack(attacker_pos, target_pos):
    """
    Verifica si un morpion puede atacar a otro (deben ser adyacentes).
    
    Args:
        attacker_pos: tupla (row, col) de la posición del atacante
        target_pos: tupla (row, col) de la posición del objetivo
    
    Returns:
        bool: True si son adyacentes (horizontal o vertical), False en caso contrario
    """
    if not isinstance(attacker_pos, tuple) or not isinstance(target_pos, tuple):
        return False
    
    if len(attacker_pos) != 2 or len(target_pos) != 2:
        return False
    
    row_diff = abs(attacker_pos[0] - target_pos[0])
    col_diff = abs(attacker_pos[1] - target_pos[1])
    
    # Adyacente significa diferencia de 1 en una dirección y 0 en la otra
    return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)


def execute_attack(attacker_morpion_state, target_morpion_state):
    """
    Ejecuta un ataque entre dos morpions.
    
    Args:
        attacker_morpion_state: dict con {'hp': ..., 'attack': ..., 'current_accuracy': ...}
        target_morpion_state: dict con {'hp': ..., ...}
    
    Returns:
        dict con estructura:
        {
            'success': bool,
            'attacker_accuracy_updated': float,  # accuracy incrementado si éxito
            'target_hp_updated': int,  # HP del objetivo después del ataque
            'damage_dealt': int  # daño infligido (0 si falló)
        }
    """
    attacker_accuracy = attacker_morpion_state.get('current_accuracy', attacker_morpion_state.get('accuracy', 1))
    success = roll_action_success(attacker_accuracy)
    
    result = {
        'success': success,
        'attacker_accuracy_updated': attacker_accuracy,
        'target_hp_updated': target_morpion_state.get('hp', 0),
        'damage_dealt': 0
    }
    
    if success:
        # Ataque exitoso: inflige daño igual a attack del atacante
        attack_power = attacker_morpion_state.get('attack', 1)
        current_hp = target_morpion_state.get('hp', 0)
        new_hp = max(0, current_hp - attack_power)  # HP no puede ser negativo
        
        result['target_hp_updated'] = new_hp
        result['damage_dealt'] = attack_power
        result['attacker_accuracy_updated'] = attacker_accuracy + 0.5  # Incremento por acción exitosa
    
    return result


def can_cast_spell(morpion_state, spell_type, cost):
    """
    Verifica si un morpion tiene suficiente mana para lanzar un sort.
    
    Args:
        morpion_state: dict con {'mana': ..., ...}
        spell_type: str ('boule_de_feu', 'soin', 'armageddon')
        cost: int, costo de mana del sort
    
    Returns:
        bool: True si tiene suficiente mana, False en caso contrario
    """
    current_mana = morpion_state.get('mana', 0)
    return current_mana >= cost


def execute_boule_de_feu(target_morpion_state):
    """
    Ejecuta el sort Boule de feu: ataque mágico directo.

    Características:
    - Daño: 3 HP (garantizado si el sort tiene éxito)
    - Costo: 2 mana
    - Rango: Ilimitado (cualquier celda con morpion enemigo)
    - Ventaja: No falla si tienes el mana (el roll de éxito es antes de llamar)

    Args:
        target_morpion_state: dict con {'hp': int, ...}

    Returns:
        dict: {
            'target_hp_updated': int,  # HP después del daño (mínimo 0)
            'mana_cost': 2,
            'damage_dealt': 3
        }
    """
    current_hp = target_morpion_state.get('hp', 0)
    new_hp = max(0, current_hp - 3)  # HP no puede ser negativo

    return {
        'target_hp_updated': new_hp,
        'mana_cost': 2,
        'damage_dealt': 3
    }


def execute_soin(target_morpion_state):
    """
    Ejecuta el sort de soin: curación a aliado o uno mismo.

    Características:
    - Curación: +2 HP (sin límite máximo, puede exceder HP inicial)
    - Costo: 1 mana (el más barato)
    - Objetivo: Solo morpions de tu equipo
    - Estrategia: Útil para prolongar partidas y proteger morpions clave

    Args:
        target_morpion_state: dict con {'hp': int, ...}

    Returns:
        dict: {
            'target_hp_updated': int,  # HP después de curación (ilimitado)
            'mana_cost': 1,
            'healing_done': 2
        }

    Nota: No hay cap de HP máximo. Un morpion que empieza con 10 HP
    puede llegar a 15 HP si recibe múltiples curaciones.
    """
    current_hp = target_morpion_state.get('hp', 0)
    new_hp = current_hp + 2

    return {
        'target_hp_updated': new_hp,
        'mana_cost': 1,
        'healing_done': 2
    }


def execute_armageddon(grid, position, destroyed_cells):
    """
    Ejecuta el sort Armageddon: destrucción permanente de una casilla.

    El hechizo más poderoso y costoso del juego. Destruye completamente
    una casilla del tablero, eliminando cualquier morpion que esté ahí
    y haciendo que la casilla sea inutilizable para el resto de la partida.

    Características:
    - Costo: 5 mana (el más caro, requiere planificación)
    - Efecto: Destruye la casilla permanentemente
    - Daño colateral: Elimina morpion enemigo si hay uno (muerte instantánea)
    - Restricción: No puedes destruir tu propia casilla
    - Estrategia: Bloquea líneas enemigas o elimina morpions poderosos

    Args:
        grid: dict {(row, col): {'team_id': X, 'morpion_id': Y}}
        position: tupla (row, col) de la casilla a destruir
        destroyed_cells: lista de tuplas [(row, col), ...] ya destruidas

    Returns:
        dict: {
            'grid_updated': dict,        # Grid sin el morpion eliminado
            'destroyed_cells_updated': list,  # Lista con nueva casilla añadida
            'mana_cost': 5,
            'morpion_killed': bool,      # True si había un morpion enemigo
            'morpion_id_killed': int | None  # ID del morpion eliminado
        }

    Ejemplo de uso táctico:
    - Bloquear la casilla central en 3x3 (posición más valiosa)
    - Destruir último morpion enemigo para victoria por eliminación
    - Romper una línea casi completa del oponente
    """
    grid_copy = dict(grid)
    destroyed_cells_copy = list(destroyed_cells)

    morpion_killed = False
    morpion_id_killed = None

    # Eliminar morpion si existe en la posición objetivo
    if position in grid_copy:
        morpion_killed = True
        morpion_id_killed = grid_copy[position].get('morpion_id')
        del grid_copy[position]

    # Marcar casilla como destruida permanentemente
    if position not in destroyed_cells_copy:
        destroyed_cells_copy.append(position)

    return {
        'grid_updated': grid_copy,
        'destroyed_cells_updated': destroyed_cells_copy,
        'mana_cost': 5,
        'morpion_killed': morpion_killed,
        'morpion_id_killed': morpion_id_killed
    }


def validate_attack_action(grid, attacker_pos, target_pos, current_player, team1_id, team2_id):
    """
    Valida que un ataque sea válido (lealtad: no atacar propio equipo).
    
    Args:
        grid: dict con estructura {(row, col): {'team_id': X, 'morpion_id': Y}}
        attacker_pos: tupla (row, col) de la posición del atacante
        target_pos: tupla (row, col) de la posición del objetivo
        current_player: int (1 o 2)
        team1_id: int, ID del equipo 1
        team2_id: int, ID del equipo 2
    
    Returns:
        tuple: (bool, str) - (True, "") si válido, (False, mensaje_error) si inválido
    """
    # Verificar que las posiciones existen en el grid
    if attacker_pos not in grid:
        return False, "Position de l'attaquant invalide"
    
    if target_pos not in grid:
        return False, "Position de la cible invalide"
    
    # Obtener team_id del atacante y objetivo
    attacker_team_id = grid[attacker_pos].get('team_id')
    target_team_id = grid[target_pos].get('team_id')
    
    # Verificar lealtad: no atacar propio equipo
    if attacker_team_id == target_team_id:
        return False, "Vous ne pouvez pas attaquer votre propre équipe"
    
    # Verificar que son adyacentes
    if not can_attack(attacker_pos, target_pos):
        return False, "Les positions doivent être adjacentes (horizontal ou vertical)"
    
    return True, ""


def validate_spell_action(grid, caster_pos, target_pos, spell_type, current_player, team1_id, team2_id, destroyed_cells=None):
    """
    Valida que un sort sea válido (lealtad y no kamikaze para armageddon).
    
    Args:
        grid: dict con estructura {(row, col): {'team_id': X, 'morpion_id': Y}}
        caster_pos: tupla (row, col) de la posición del lanzador (puede ser None para armageddon)
        target_pos: tupla (row, col) de la posición objetivo
        spell_type: str ('boule_de_feu', 'soin', 'armageddon')
        current_player: int (1 o 2)
        team1_id: int, ID del equipo 1
        team2_id: int, ID del equipo 2
        destroyed_cells: lista de casillas destruidas (opcional)
    
    Returns:
        tuple: (bool, str) - (True, "") si válido, (False, mensaje_error) si inválido
    """
    current_team_id = team1_id if current_player == 1 else team2_id
    destroyed_cells = destroyed_cells or []
    
    if spell_type == 'armageddon':
        if caster_pos is None or caster_pos not in grid:
            return False, "Sélectionnez un morpion de votre équipe pour lancer Armageddon"
        caster_team_id = grid[caster_pos].get('team_id')
        if caster_team_id != current_team_id:
            return False, "Armageddon doit être lancé par un morpion de votre équipe"
        if caster_pos == target_pos:
            return False, "Vous ne pouvez pas utiliser Armageddon sur votre propre case"
        if target_pos in destroyed_cells:
            return False, "Cette case est déjà détruite"
    
    elif spell_type == 'boule_de_feu':
        if caster_pos is None or caster_pos not in grid:
            return False, "Sélectionnez un morpion de votre équipe pour lancer Boule de feu"
        caster_team_id = grid[caster_pos].get('team_id')
        if caster_team_id != current_team_id:
            return False, "Boule de feu doit être lancé par un morpion de votre équipe"
        if target_pos not in grid:
            return False, "Il doit y avoir un morpion ennemi sur la case cible"
        
        target_team_id = grid[target_pos].get('team_id')
        if target_team_id == current_team_id:
            return False, "Vous ne pouvez pas attaquer votre propre équipe"
    
    elif spell_type == 'soin':
        if target_pos not in grid:
            return False, "Il doit y avoir un morpion sur la case cible"
        
        target_team_id = grid[target_pos].get('team_id')
        if target_team_id != current_team_id:
            return False, "Vous ne pouvez soigner que vos propres morpions"
    
    return True, ""


def check_all_morpions_dead(grid, morpions_state, team_id, team_morpion_ids=None, used_morpions=None):
    """
    Verifica si todos los morpions de un equipo están muertos (HP <= 0).
    
    Args:
        grid: dict con estructura {(row, col): {'team_id': X, 'morpion_id': Y}}
        morpions_state: dict con {morpion_id: {'hp': ..., ...}}
        team_id: int, ID del equipo a verificar
        team_morpion_ids: set de IDs de morpions que pertenecen al equipo (opcional)
    
    Returns:
        bool: True si todos los morpions del equipo están muertos, False en caso contrario
    """
    # Obtener todos los morpions del equipo en el grid
    team_morpion_ids_in_grid = set()
    for cell_data in grid.values():
        if cell_data.get('team_id') == team_id:
            morpion_id = cell_data.get('morpion_id')
            if morpion_id:
                team_morpion_ids_in_grid.add(morpion_id)
    
    # Si no hay morpions del equipo en el grid:
    # - Si no se han colocado morpions aún (grid vacío), la partida acaba de empezar -> False
    # - Si hay morpions en morpions_state pero no en el grid, todos están muertos -> True
    if len(team_morpion_ids_in_grid) == 0:
        team_set = set(team_morpion_ids) if team_morpion_ids is not None else None
        if team_set is not None:
            used_set = {mid for mid in (used_morpions or []) if mid in team_set}
        else:
            used_set = set(used_morpions) if used_morpions is not None else None

        # Si conocemos el roster completo del equipo y no todos se han usado, no está eliminado
        if team_set is not None:
            if used_set is None or len(used_set) < len(team_set):
                return False

        # Construir la lista completa de morpions a verificar (idealmente todos los del roster)
        candidates = team_set if team_set is not None else set(morpions_state.keys())
        if not candidates:
            return False

        for morpion_id in candidates:
            morpion_state = morpions_state.get(morpion_id)
            if morpion_state is None:
                # Falta info => prudencia, considerarlo vivo
                return False
            hp = morpion_state.get('hp', 0)
            if hp > 0:
                return False  # Hay al menos uno vivo
        return True  # Todos los morpions del roster conocidos están muertos
    
    # Verificar que todos los morpions del equipo en el grid tienen HP <= 0
    for morpion_id in team_morpion_ids_in_grid:
        morpion_state = morpions_state.get(morpion_id)
        if morpion_state:
            hp = morpion_state.get('hp', 0)
            if hp > 0:
                return False  # Hay al menos uno vivo
    
    return True  # Todos los morpions en el grid están muertos


def check_game_end_conditions_avancee(grid, grid_size, current_turn, max_turns, team1_id, team2_id,
                                      morpions_state, destroyed_cells, team1_morpions=None, team2_morpions=None, used_morpions=None):
    """
    Verifica todas las condiciones de fin de partie para partie avancée.
    Extiende check_game_end_conditions de normale agregando verificación de eliminación completa.
    
    Args:
        grid: dict con estructura {(row, col): {'team_id': X, 'morpion_id': Y}}
        grid_size: tamaño de la grille (3 o 4)
        current_turn: turno actual
        max_turns: número máximo de turnos configurado
        team1_id: ID del equipo 1
        team2_id: ID del equipo 2
        morpions_state: dict con {morpion_id: {'hp': ..., ...}}
        destroyed_cells: lista de tuplas [(row, col), ...]
        team1_morpions: lista de morpions del equipo 1 (opcional)
        team2_morpions: lista de morpions del equipo 2 (opcional)
        used_morpions: lista de IDs de morpions usados (opcional)
    
    Returns:
        dict con estructura:
        {
            'game_over': bool,
            'winner_team_id': int | None,  # None si empate o partida no terminada
            'reason': str  # 'victory', 'max_turns', 'all_morpions_dead', 'stalemate', None
        }
    """
    # Importar funciones de normale para reutilizar
    from models.game_logic_normale import check_victory_normale
    
    # Verificar victoria por línea completa (reutilizar de normale)
    if check_victory_normale(grid, grid_size, team1_id):
        return {
            'game_over': True,
            'winner_team_id': team1_id,
            'reason': 'victory'
        }
    
    if check_victory_normale(grid, grid_size, team2_id):
        return {
            'game_over': True,
            'winner_team_id': team2_id,
            'reason': 'victory'
        }
    
    # Verificar eliminación completa de morpions (incluso si la grille está vacía)
    team1_morpion_ids = {m['id_morpion'] for m in team1_morpions} if team1_morpions else None
    team2_morpion_ids = {m['id_morpion'] for m in team2_morpions} if team2_morpions else None
    
    team1_all_dead = check_all_morpions_dead(
        grid,
        morpions_state,
        team1_id,
        team1_morpion_ids,
        used_morpions=used_morpions,
    )
    team2_all_dead = check_all_morpions_dead(
        grid,
        morpions_state,
        team2_id,
        team2_morpion_ids,
        used_morpions=used_morpions,
    )
    
    if team1_all_dead and team2_all_dead:
        return {
            'game_over': True,
            'winner_team_id': None,
            'reason': 'all_morpions_dead'
        }
    elif team1_all_dead:
        return {
            'game_over': True,
            'winner_team_id': team2_id,
            'reason': 'all_morpions_dead'
        }
    elif team2_all_dead:
        return {
            'game_over': True,
            'winner_team_id': team1_id,
            'reason': 'all_morpions_dead'
        }
    
    # Verificar máximo de turnos
    if current_turn > max_turns:
        return {
            'game_over': True,
            'winner_team_id': None,
            'reason': 'max_turns'
        }
    
    # Verificar si ambos equipos están bloqués (sin morpions disponibles, sin mana, sin ataques posibles)
    if team1_morpions is not None and team2_morpions is not None and used_morpions is not None:
        team1_ids = {m['id_morpion'] for m in team1_morpions}
        team2_ids = {m['id_morpion'] for m in team2_morpions}
        used_set = set(used_morpions)

        team1_used = used_set & team1_ids
        team2_used = used_set & team2_ids

        team1_available = team1_ids - team1_used
        team2_available = team2_ids - team2_used

        def team_has_spell_option(team_id, team_ids):
            # necesita un morpion en la grille
            morpions_on_grid = [cell['morpion_id'] for cell in grid.values() if cell.get('team_id') == team_id]
            if not morpions_on_grid:
                return False
            for mid in morpions_on_grid:
                state = morpions_state.get(mid, {})
                if state.get('mana', 0) >= 1:
                    return True
            return False

        def teams_adjacent():
            # ¿Existe al menos una paire adyacente?
            positions = list(grid.items())
            for (pos_a, cell_a) in positions:
                team_a = cell_a.get('team_id')
                if team_a not in (team1_id, team2_id):
                    continue
                for (pos_b, cell_b) in positions:
                    if cell_b.get('team_id') == team_a:
                        continue
                    if can_attack(pos_a, pos_b):
                        return True
            return False

        no_placeable = len(team1_available) == 0 and len(team2_available) == 0
        no_spell = (not team_has_spell_option(team1_id, team1_ids)) and (not team_has_spell_option(team2_id, team2_ids))
        no_attack = not teams_adjacent()

        if no_placeable and no_spell and no_attack:
            return {
                'game_over': True,
                'winner_team_id': None,
                'reason': 'stalemate'
            }
    
    # Partida continúa
    return {
        'game_over': False,
        'winner_team_id': None,
        'reason': None
    }
