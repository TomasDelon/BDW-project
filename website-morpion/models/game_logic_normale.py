"""
Funciones de lógica de juego para partie normale (Fonctionnalité 3).
Funciones puras sin acceso a BD.
"""


def check_victory_normale(grid, grid_size, team_id):
    """
    Verifica si un equipo tiene una línea completa (victoria).
    
    Args:
        grid: dict con estructura {(row, col): {'team_id': X, 'morpion_id': Y}}
        grid_size: tamaño de la grille (3 o 4)
        team_id: ID del equipo a verificar
    
    Returns:
        bool: True si el equipo tiene una línea completa, False en caso contrario
    """
    required_length = grid_size  # 3 para grille 3x3, 4 para grille 4x4
    
    # Obtener todas las posiciones ocupadas por este equipo
    team_positions = set()
    for (row, col), cell_data in grid.items():
        if cell_data.get('team_id') == team_id:
            team_positions.add((row, col))
    
    if len(team_positions) < required_length:
        return False
    
    # Verificar líneas horizontales
    for row in range(grid_size):
        count = 0
        for col in range(grid_size):
            if (row, col) in team_positions:
                count += 1
            else:
                count = 0
            if count == required_length:
                return True
    
    # Verificar líneas verticales
    for col in range(grid_size):
        count = 0
        for row in range(grid_size):
            if (row, col) in team_positions:
                count += 1
            else:
                count = 0
            if count == required_length:
                return True
    
    # Verificar diagonal principal (de arriba-izquierda a abajo-derecha)
    count = 0
    for i in range(grid_size):
        if (i, i) in team_positions:
            count += 1
        else:
            count = 0
        if count == required_length:
            return True
    
    # Verificar diagonal secundaria (de arriba-derecha a abajo-izquierda)
    count = 0
    for i in range(grid_size):
        if (i, grid_size - 1 - i) in team_positions:
            count += 1
        else:
            count = 0
        if count == required_length:
            return True
    
    return False


def is_grid_full_normale(grid, grid_size):
    """
    Verifica si la grille está completamente llena.
    
    Args:
        grid: dict con estructura {(row, col): {'team_id': X, 'morpion_id': Y}}
        grid_size: tamaño de la grille (3 o 4)
    
    Returns:
        bool: True si la grille está llena, False en caso contrario
    """
    total_cells = grid_size * grid_size
    return len(grid) >= total_cells


def check_game_end_conditions(grid, grid_size, current_turn, max_turns, team1_id, team2_id, 
                              team1_morpions=None, team2_morpions=None, used_morpions=None):
    """
    Verifica todas las condiciones de fin de partie.
    
    Args:
        grid: dict con estructura {(row, col): {'team_id': X, 'morpion_id': Y}}
        grid_size: tamaño de la grille (3 o 4)
        current_turn: turno actual
        max_turns: número máximo de turnos configurado
        team1_id: ID del equipo 1
        team2_id: ID del equipo 2
        team1_morpions: lista de morpions del equipo 1 (opcional, para verificar si se quedaron sin morpions)
        team2_morpions: lista de morpions del equipo 2 (opcional, para verificar si se quedaron sin morpions)
        used_morpions: lista de IDs de morpions usados (opcional, para verificar si se quedaron sin morpions)
    
    Returns:
        dict con estructura:
        {
            'game_over': bool,
            'winner_team_id': int | None,  # None si empate o partida no terminada
            'reason': str  # 'victory', 'grid_full', 'max_turns', 'no_morpions', None
        }
    """
    # Verificar victoria del equipo 1
    if check_victory_normale(grid, grid_size, team1_id):
        return {
            'game_over': True,
            'winner_team_id': team1_id,
            'reason': 'victory'
        }
    
    # Verificar victoria del equipo 2
    if check_victory_normale(grid, grid_size, team2_id):
        return {
            'game_over': True,
            'winner_team_id': team2_id,
            'reason': 'victory'
        }
    
    # Verificar grille llena
    if is_grid_full_normale(grid, grid_size):
        return {
            'game_over': True,
            'winner_team_id': None,
            'reason': 'grid_full'
        }
    
    # Verificar máximo de turnos
    if current_turn > max_turns:
        return {
            'game_over': True,
            'winner_team_id': None,
            'reason': 'max_turns'
        }
    
    # Verificar si ambos equipos se quedaron sin morpions disponibles
    if team1_morpions is not None and team2_morpions is not None and used_morpions is not None:
        # Obtener IDs de morpions disponibles para cada equipo
        team1_morpion_ids = {m['id_morpion'] for m in team1_morpions}
        team2_morpion_ids = {m['id_morpion'] for m in team2_morpions}
        used_morpion_set = set(used_morpions)
        
        # Verificar morpions disponibles para cada equipo
        team1_available = team1_morpion_ids - used_morpion_set
        team2_available = team2_morpion_ids - used_morpion_set
        
        # Si ambos equipos se quedaron sin morpions, es empate
        if len(team1_available) == 0 and len(team2_available) == 0:
            return {
                'game_over': True,
                'winner_team_id': None,
                'reason': 'no_morpions'
            }
    
    # Partida continúa
    return {
        'game_over': False,
        'winner_team_id': None,
        'reason': None
    }

