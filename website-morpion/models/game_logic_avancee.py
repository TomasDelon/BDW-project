"""
Fonctions de logique de jeu pour partie avancée (Fonctionnalité 4).
Implémente un système de combat avec probabilités, sorts et élimination.

Toutes les fonctions sont pures (sans effets secondaires ni accès à la BD),
ce qui facilite les tests et le raisonnement sur le comportement du jeu.
"""

import random

# Constantes de balance de probabilités de succès
# Ces valeurs ont été ajustées pour réduire la frustration du joueur
# tout en maintenant un élément de hasard intéressant.
DEFAULT_SUCCESS_RATE_SCALE = 1.6  # Multiplie l'accuracy pour amplifier les différences
DEFAULT_SUCCESS_RATE_FLAT_BONUS = 10.0  # Bonus de base pour éviter trop d'échecs

# Contexte de balance :
# - Sans bonus : accuracy=5 → 50% de succès (trop d'échecs)
# - Avec ces valeurs : accuracy=5 → (5*1.6)+10 = 18% → min(18, 100) = 18% de succès
# - Morpion fort (accuracy=8) : (8*1.6)+10 = 22.8% de succès
# Le système favorise légèrement les morpions avec une haute accuracy

try:
    from constants import SUCCESS_RATE_SCALE, SUCCESS_RATE_FLAT_BONUS
except ImportError:
    SUCCESS_RATE_SCALE = DEFAULT_SUCCESS_RATE_SCALE
    SUCCESS_RATE_FLAT_BONUS = DEFAULT_SUCCESS_RATE_FLAT_BONUS


def calculate_success_probability(accuracy):
    """
    Calcule la probabilité de succès d'une action.
    Prend en charge les valeurs en échelle 0-10 (multipliées par 10) ou 0-100 directement.
    Applique ensuite un bonus global pour réduire la quantité d'échecs (paramétrable via constantes).
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

    # Ajuste approbado pour réduire les échecs : on applique un multiplicateur et un bonus fixe
    probability = (probability * SUCCESS_RATE_SCALE) + SUCCESS_RATE_FLAT_BONUS

    return max(0.0, min(probability, 100.0))


def roll_action_success(accuracy):
    """
    Génère une valeur aléatoire et vérifie si l'action est réussie.
    
    Args:
        accuracy: points de réussite (current_accuracy)
    
    Returns:
        bool: True si l'action est réussie, False sinon
    """
    probability = calculate_success_probability(accuracy)
    roll = random.uniform(0, 100)
    return roll < probability


def can_attack(attacker_pos, target_pos):
    """
    Vérifie si un morpion peut attaquer un autre (doivent être adjacents).
    
    Args:
        attacker_pos: tuple (row, col) de la position de l'attaquant
        target_pos: tuple (row, col) de la position de la cible
    
    Returns:
        bool: True si ils sont adjacents (horizontal ou vertical), False sinon
    """
    if not isinstance(attacker_pos, tuple) or not isinstance(target_pos, tuple):
        return False
    
    if len(attacker_pos) != 2 or len(target_pos) != 2:
        return False
    
    row_diff = abs(attacker_pos[0] - target_pos[0])
    col_diff = abs(attacker_pos[1] - target_pos[1])
    
    # Adyacente signifie différence de 1 dans une direction et 0 dans l'autre
    return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)


def execute_attack(attacker_morpion_state, target_morpion_state):
    """
    Exécute une attaque entre deux morpions.
    
    Args:
        attacker_morpion_state: dict avec {'hp': ..., 'attack': ..., 'current_accuracy': ...}
        target_morpion_state: dict avec {'hp': ..., ...}
    
    Returns:
        dict avec structure :
        {
            'success': bool,
            'attacker_accuracy_updated': float,  # accuracy incrémenté si succès
            'target_hp_updated': int,  # HP de la cible après l'attaque
            'damage_dealt': int  # dégâts infligés (0 si échec)
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
        # Ataque réussi : inflige des dégâts égaux à l'attaque de l'attaquant
        attack_power = attacker_morpion_state.get('attack', 1)
        current_hp = target_morpion_state.get('hp', 0)
        new_hp = max(0, current_hp - attack_power)  # HP ne peut pas être négatif
        
        result['target_hp_updated'] = new_hp
        result['damage_dealt'] = attack_power
        result['attacker_accuracy_updated'] = attacker_accuracy + 0.5  # Incrémentation pour une action réussie
    
    return result


def can_cast_spell(morpion_state, spell_type, cost):
    """
    Vérifie si un morpion a assez de mana pour lancer un sort.
    
    Args:
        morpion_state: dict avec {'mana': ..., ...}
        spell_type: str ('boule_de_feu', 'soin', 'armageddon')
        cost: int, coût de mana du sort
    
    Returns:
        bool: True s'il a assez de mana, False sinon
    """
    current_mana = morpion_state.get('mana', 0)
    return current_mana >= cost


def execute_boule_de_feu(target_morpion_state):
    """
    Exécute le sort Boule de feu : attaque magique directe.

    Caractéristiques :
    - Dégâts : 3 HP (garantis si le sort réussit)
    - Coût : 2 mana
    - Portée : Illimitée (n'importe quelle case avec un morpion ennemi)
    - Avantage : Ne rate pas si vous avez le mana (le roll de succès est fait avant d'appeler)

    Args:
        target_morpion_state: dict avec {'hp': int, ...}

    Returns:
        dict : {
            'target_hp_updated': int,  # HP après les dégâts (minimum 0)
            'mana_cost': 2,
            'damage_dealt': 3
        }
    """
    current_hp = target_morpion_state.get('hp', 0)
    new_hp = max(0, current_hp - 3)  # HP ne peut pas être négatif

    return {
        'target_hp_updated': new_hp,
        'mana_cost': 2,
        'damage_dealt': 3
    }


def execute_soin(target_morpion_state):
    """
    Exécute le sort de soin : guérison d'un allié ou de soi-même.

    Caractéristiques :
    - Guérison : +2 HP (sans limite maximale, peut dépasser le HP initial)
    - Coût : 1 mana (le plus économique)
    - Cible : Seulement les morpions de votre équipe
    - Stratégie : Utile pour prolonger les parties et protéger les morpions clés

    Args:
        target_morpion_state: dict avec {'hp': int, ...}

    Returns:
        dict : {
            'target_hp_updated': int,  # HP après guérison (illimité)
            'mana_cost': 1,
            'healing_done': 2
        }

    Note : Pas de limite maximale de HP. Un morpion qui commence avec 10 HP
    peut atteindre 15 HP s'il reçoit plusieurs soins.
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
    Exécute le sort Armageddon : destruction permanente d'une case.

    Le sort le plus puissant et coûteux du jeu. Détruit complètement
    une case du plateau, éliminant tout morpion présent dessus
    et rendant la case inutilisable pour le reste de la partie.

    Caractéristiques :
    - Coût : 5 mana (le plus cher, nécessite de la planification)
    - Effet : Détruit la case de manière permanente
    - Dégâts collatéraux : Élimine le morpion ennemi s'il y en a un (mort instantanée)
    - Restriction : Vous ne pouvez pas détruire votre propre case
    - Stratégie : Bloque les lignes ennemies ou élimine les morpions puissants

    Args:
        grid: dict {(row, col): {'team_id': X, 'morpion_id': Y}}
        position: tuple (row, col) de la case à détruire
        destroyed_cells: liste de tuples [(row, col), ...] déjà détruites

    Returns:
        dict : {
            'grid_updated': dict,        # Grille sans le morpion éliminé
            'destroyed_cells_updated': list,  # Liste avec nouvelle case ajoutée
            'mana_cost': 5,
            'morpion_killed': bool,      # True s'il y avait un morpion ennemi
            'morpion_id_killed': int | None  # ID du morpion éliminé
        }

    Exemple d'utilisation tactique :
    - Bloquer la case centrale en 3x3 (position la plus précieuse)
    - Détruire le dernier morpion ennemi pour victoire par élimination
    - Briser une ligne presque complète de l'adversaire
    """
    grid_copy = dict(grid)
    destroyed_cells_copy = list(destroyed_cells)

    morpion_killed = False
    morpion_id_killed = None

    # Eliminer morpion si existe en position cible
    if position in grid_copy:
        morpion_killed = True
        morpion_id_killed = grid_copy[position].get('morpion_id')
        del grid_copy[position]

    # Marquer la case comme détruite de manière permanente
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
    Valide qu'une attaque soit valide (loyauté : ne pas attaquer son propre équipe).
    
    Args:
        grid: dict avec structure {(row, col): {'team_id': X, 'morpion_id': Y}}
        attacker_pos: tuple (row, col) de la position de l'attaquant
        target_pos: tuple (row, col) de la position de la cible
        current_player: int (1 ou 2)
        team1_id: int, ID de l'équipe 1
        team2_id: int, ID de l'équipe 2
    
    Returns:
        tuple: (bool, str) - (True, "") si valide, (False, message_erreur) si invalide
    """
    # Vérifier que les positions existent dans la grille
    if attacker_pos not in grid:
        return False, "Position de l'attaquant invalide"
    
    if target_pos not in grid:
        return False, "Position de la cible invalide"
    
    # Obtenir team_id de l'attaquant et de la cible
    attacker_team_id = grid[attacker_pos].get('team_id')
    target_team_id = grid[target_pos].get('team_id')
    
    # Vérifier la loyauté : ne pas attaquer son propre équipe
    if attacker_team_id == target_team_id:
        return False, "Vous ne pouvez pas attaquer votre propre équipe"
    
    # Vérifier qu'ils sont adjacents
    if not can_attack(attacker_pos, target_pos):
        return False, "Les positions doivent être adjacentes (horizontal ou vertical)"
    
    return True, ""


def validate_spell_action(grid, caster_pos, target_pos, spell_type, current_player, team1_id, team2_id, destroyed_cells=None):
    """
    Valide qu'un sort soit valide (loyauté et pas kamikaze pour armageddon).
    
    Args:
        grid: dict avec structure {(row, col): {'team_id': X, 'morpion_id': Y}}
        caster_pos: tuple (row, col) de la position du lanceur (peut être None pour armageddon)
        target_pos: tuple (row, col) de la position cible
        spell_type: str ('boule_de_feu', 'soin', 'armageddon')
        current_player: int (1 ou 2)
        team1_id: int, ID de l'équipe 1
        team2_id: int, ID de l'équipe 2
        destroyed_cells: liste de cases détruites (optionnel)
    
    Returns:
        tuple: (bool, str) - (True, "") si valide, (False, message_erreur) si invalide
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
    Vérifie si tous les morpions d'une équipe sont morts (HP <= 0).
    
    Args:
        grid: dict avec structure {(row, col): {'team_id': X, 'morpion_id': Y}}
        morpions_state: dict avec {morpion_id: {'hp': ..., ...}}
        team_id: int, ID de l'équipe à vérifier
        team_morpion_ids: set d'IDs de morpions appartenant à l'équipe (optionnel)
    
    Returns:
        bool: True si tous les morpions de l'équipe sont morts, False sinon
    """
    # Obtenir tous les morpions de l'équipe dans la grille
    team_morpion_ids_in_grid = set()
    for cell_data in grid.values():
        if cell_data.get('team_id') == team_id:
            morpion_id = cell_data.get('morpion_id')
            if morpion_id:
                team_morpion_ids_in_grid.add(morpion_id)
    
    # Si aucun morpion de l'équipe dans la grille :
    # - Si aucun morpion n'a encore été placé (grille vide), la partie vient de commencer -> False
    # - Si des morpions sont dans morpions_state mais pas dans la grille, tous sont morts -> True
    if len(team_morpion_ids_in_grid) == 0:
        team_set = set(team_morpion_ids) if team_morpion_ids is not None else None
        if team_set is not None:
            used_set = {mid for mid in (used_morpions or []) if mid in team_set}
        else:
            used_set = set(used_morpions) if used_morpions is not None else None

        # Si on connaît le roster complet de l'équipe et qu'aucun n'a été utilisé, il n'est pas éliminé
        if team_set is not None:
            if used_set is None or len(used_set) < len(team_set):
                return False

        # Construire la liste complète des morpions à vérifier (idéalement tous les du roster)
        candidates = team_set if team_set is not None else set(morpions_state.keys())
        if not candidates:
            return False

        for morpion_id in candidates:
            morpion_state = morpions_state.get(morpion_id)
            if morpion_state is None:
                # Manque d'info => prudence, le considérer vivant
                return False
            hp = morpion_state.get('hp', 0)
            if hp > 0:
                return False  # Au moins un vivant
        return True  # Tous les morpions du roster connu sont morts
    
    # Vérifier que tous les morpions de l'équipe dans la grille ont HP <= 0
    for morpion_id in team_morpion_ids_in_grid:
        morpion_state = morpions_state.get(morpion_id)
        if morpion_state:
            hp = morpion_state.get('hp', 0)
            if hp > 0:
                return False  # Au moins un vivant
    
    return True  # Tous les morpions dans la grille sont morts


def check_game_end_conditions_avancee(grid, grid_size, current_turn, max_turns, team1_id, team2_id,
                                      morpions_state, destroyed_cells, team1_morpions=None, team2_morpions=None, used_morpions=None):
    """
    Vérifie toutes les conditions de fin de partie pour partie avancée.
    Étend check_game_end_conditions de normale en ajoutant la vérification d'élimination complète.
    
    Args:
        grid: dict avec structure {(row, col): {'team_id': X, 'morpion_id': Y}}
        grid_size: taille de la grille (3 ou 4)
        current_turn: tour actuel
        max_turns: nombre maximum de tours configuré
        team1_id: ID de l'équipe 1
        team2_id: ID de l'équipe 2
        morpions_state: dict avec {morpion_id: {'hp': ..., ...}}
        destroyed_cells: liste de tuples [(row, col), ...]
        team1_morpions: liste de morpions de l'équipe 1 (optionnel)
        team2_morpions: liste de morpions de l'équipe 2 (optionnel)
        used_morpions: liste d'IDs de morpions utilisés (optionnel)
    
    Returns:
        dict avec structure :
        {
            'game_over': bool,
            'winner_team_id': int | None,  # None si égalité ou partie non terminée
            'reason': str  # 'victory', 'max_turns', 'all_morpions_dead', 'stalemate', None
        }
    """
    # Importer les fonctions de normale pour réutiliser
    from models.game_logic_normale import check_victory_normale
    
    # Vérifier la victoire par ligne complète (réutiliser de normale)
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
    
    # Vérifier l'élimination complète des morpions (même si la grille est vide)
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
    
    # Vérifier le maximum de tours
    if current_turn > max_turns:
        return {
            'game_over': True,
            'winner_team_id': None,
            'reason': 'max_turns'
        }
    
    # Vérifier si les deux équipes sont bloquées (aucun morpion disponible, aucun mana, aucune attaque possible)
    if team1_morpions is not None and team2_morpions is not None and used_morpions is not None:
        team1_ids = {m['id_morpion'] for m in team1_morpions}
        team2_ids = {m['id_morpion'] for m in team2_morpions}
        used_set = set(used_morpions)

        team1_used = used_set & team1_ids
        team2_used = used_set & team2_ids

        team1_available = team1_ids - team1_used
        team2_available = team2_ids - team2_used

        def team_has_spell_option(team_id, team_ids):
            # a besoin d'un morpion sur la grille
            morpions_on_grid = [cell['morpion_id'] for cell in grid.values() if cell.get('team_id') == team_id]
            if not morpions_on_grid:
                return False
            for mid in morpions_on_grid:
                state = morpions_state.get(mid, {})
                if state.get('mana', 0) >= 1:
                    return True
            return False

        def teams_adjacent():
            # Existe-t-il au moins une paire adjacente ?
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
    
    # La partie continue
    return {
        'game_over': False,
        'winner_team_id': None,
        'reason': None
    }
