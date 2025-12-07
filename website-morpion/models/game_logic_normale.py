"""
Fonctions de logique de jeu pour partie normale (Fonctionnalité 3).
Fonctions pures sans accès à la BD.
"""


def check_victory_normale(grid, grid_size, team_id):
    """
    Vérifie si une équipe a une ligne complète (victoire).
    
    Args:
        grid: dict avec structure {(row, col): {'team_id': X, 'morpion_id': Y}}
        grid_size: taille de la grille (3 ou 4)
        team_id: ID de l'équipe à vérifier
    
    Returns:
        bool: True si l'équipe a une ligne complète, False sinon
    """
    required_length = grid_size  # 3 pour grille 3x3, 4 pour grille 4x4
    
    # Obtenir toutes les positions occupées par cette équipe
    team_positions = set()
    for (row, col), cell_data in grid.items():
        if cell_data.get('team_id') == team_id:
            team_positions.add((row, col))
    
    if len(team_positions) < required_length:
        return False
    
    # Vérifier les lignes horizontales
    for row in range(grid_size):
        count = 0
        for col in range(grid_size):
            if (row, col) in team_positions:
                count += 1
            else:
                count = 0
            if count == required_length:
                return True
    
    # Vérifier les lignes verticales
    for col in range(grid_size):
        count = 0
        for row in range(grid_size):
            if (row, col) in team_positions:
                count += 1
            else:
                count = 0
            if count == required_length:
                return True
    
    # Vérifier la diagonale principale (de haut-gauche à bas-droite)
    count = 0
    for i in range(grid_size):
        if (i, i) in team_positions:
            count += 1
        else:
            count = 0
        if count == required_length:
            return True
    
    # Vérifier la diagonale secondaire (de haut-droite à bas-gauche)
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
    Vérifie si la grille est complètement remplie.
    
    Args:
        grid: dict avec structure {(row, col): {'team_id': X, 'morpion_id': Y}}
        grid_size: taille de la grille (3 ou 4)
    
    Returns:
        bool: True si la grille est pleine, False sinon
    """
    total_cells = grid_size * grid_size
    return len(grid) >= total_cells


def check_game_end_conditions(grid, grid_size, current_turn, max_turns, team1_id, team2_id, 
                              team1_morpions=None, team2_morpions=None, used_morpions=None):
    """
    Vérifie toutes les conditions de fin de partie.
    
    Args:
        grid: dict avec structure {(row, col): {'team_id': X, 'morpion_id': Y}}
        grid_size: taille de la grille (3 ou 4)
        current_turn: tour actuel
        max_turns: nombre maximum de tours configuré
        team1_id: ID de l'équipe 1
        team2_id: ID de l'équipe 2
        team1_morpions: liste de morpions de l'équipe 1 (optionnel, pour vérifier si ils n'ont plus de morpions)
        team2_morpions: liste de morpions de l'équipe 2 (optionnel, pour vérifier si ils n'ont plus de morpions)
        used_morpions: liste d'IDs de morpions utilisés (optionnel, pour vérifier si ils n'ont plus de morpions)
    
    Returns:
        dict avec structure :
        {
            'game_over': bool,
            'winner_team_id': int | None,  # None si égalité ou partie non terminée
            'reason': str  # 'victory', 'grid_full', 'max_turns', 'no_morpions', None
        }
    """
    # Vérifier la victoire de l'équipe 1
    if check_victory_normale(grid, grid_size, team1_id):
        return {
            'game_over': True,
            'winner_team_id': team1_id,
            'reason': 'victory'
        }
    
    # Vérifier la victoire de l'équipe 2
    if check_victory_normale(grid, grid_size, team2_id):
        return {
            'game_over': True,
            'winner_team_id': team2_id,
            'reason': 'victory'
        }
    
    # Vérifier la grille pleine
    if is_grid_full_normale(grid, grid_size):
        return {
            'game_over': True,
            'winner_team_id': None,
            'reason': 'grid_full'
        }
    
    # Vérifier le nombre maximum de tours
    if current_turn > max_turns:
        return {
            'game_over': True,
            'winner_team_id': None,
            'reason': 'max_turns'
        }
    
    # Vérifier si les deux équipes se sont retrouvées sans morpions disponibles
    if team1_morpions is not None and team2_morpions is not None and used_morpions is not None:
        # Obtenir les IDs de morpions disponibles pour chaque équipe
        team1_morpion_ids = {m['id_morpion'] for m in team1_morpions}
        team2_morpion_ids = {m['id_morpion'] for m in team2_morpions}
        used_morpion_set = set(used_morpions)
        
        # Vérifier les morpions disponibles pour chaque équipe
        team1_available = team1_morpion_ids - used_morpion_set
        team2_available = team2_morpion_ids - used_morpion_set
        
        # Si les deux équipes se sont retrouvées sans morpions, c'est égalité
        if len(team1_available) == 0 and len(team2_available) == 0:
            return {
                'game_over': True,
                'winner_team_id': None,
                'reason': 'no_morpions'
            }
    
    # La partie continue
    return {
        'game_over': False,
        'winner_team_id': None,
        'reason': None
    }

