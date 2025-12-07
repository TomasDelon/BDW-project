"""
Moteur d'IA pour le jeu classique de Morpion Masters.
Implémente Minimax avec élagage Alpha-Beta pour des décisions optimales.
"""

import random
from typing import Dict, Tuple, List
from logzero import logger

from .game_logic_normale import check_victory_normale


class MorpionAI:
    """
    Moteur d'IA pour jouer contre l'utilisateur en utilisant l'algorithme Minimax.

    Implémente trois niveaux de difficulté équilibrés pour offrir une
    expérience de jeu progressive sans être frustrante.
    """

    def __init__(self, difficulty='medium'):
        """
        Initialise le moteur d'IA avec un niveau de difficulté spécifique.

        Args:
            difficulty: 'easy', 'medium', 'hard'
                - easy: Minimax profondeur 2 + 60% mouvements aléatoires
                  (permet au joueur de gagner, bon pour l'apprentissage)
                - medium: Minimax profondeur 4 sans aléatoire
                  (équilibré, tactiquement compétent mais pas parfait)
                - hard: Minimax profondeur 9 (grille complète 3x3)
                  (pratiquement imbattable, jeu optimal)

        Profondeurs choisies selon l'analyse de complexité:
        - Grille 3x3: 9 positions → profondeur 9 explore tout l'arbre
        - Grille 4x4: Réduit à 3/4/5 selon difficulté (16 positions = complexité énorme)
        - Profondeur 4: Équilibre entre temps de réponse (<100ms) et qualité
        - Profondeur 2: Seulement 2 tours à l'avance, nombreuses erreurs tactiques
        """
        self.difficulty = difficulty
        # Profondeurs pour grille 3x3
        self.max_depth_3x3 = {
            'easy': 2,     # ~100 Nœuds
            'medium': 4,   # ~10,000 Nœuds
            'hard': 9      # ~362,880 Nœuds (pire cas), mais élagage réduit à ~5000
        }[difficulty]

        # Profondeurs réduites pour grille 4x4 (complexité beaucoup plus élevée)
        self.max_depth_4x4 = {
            'easy': 2,     # ~256 Nœuds
            'medium': 3,   # ~4,096 Nœuds
            'hard': 4      # ~65,536 Nœuds (acceptable avec élagage et optimisations)
        }[difficulty]

        # Cache pour mémoriser les positions déjà évaluées
        self.transposition_table = {}
    
    def choose_move(self, grid: Dict[Tuple[int, int], dict],
                    grid_size: int,
                    ai_team_id: int,
                    player_team_id: int,
                    available_morpions: List[dict]) -> Tuple[int, Tuple[int, int]]:
        """
        Choisit le meilleur mouvement pour l'IA.

        Args:
            grid: État actuel de la grille
            grid_size: Taille de la grille (3 ou 4)
            ai_team_id: ID de l'équipe de l'IA
            player_team_id: ID de l'équipe du joueur
            available_morpions: Liste des morpions disponibles pour l'IA

        Returns:
            Tuple (morpion_id, (row, col))
        """
        if not available_morpions:
            raise ValueError("Aucun morpion disponible pour l'IA")

        # Obtenir toutes les positions vides
        empty_positions = self._get_empty_positions(grid, grid_size)

        if not empty_positions:
            raise ValueError("Aucune position vide dans la grille")

        # Pour grille 4x4, jouer aléatoirement aux 2-3 premiers coups pour éviter les longs calculs
        if grid_size == 4 and len(empty_positions) >= 14:
            # Préférer les positions centrales pour un meilleur jeu
            return self._smart_random_move(available_morpions, empty_positions, grid_size)

        # Pour difficulté facile, parfois faire des mouvements aléatoires
        if self.difficulty == 'easy' and random.random() < 0.6:
            return self._random_move(available_morpions, empty_positions)

        # Réinitialiser le cache de transposition au début de chaque tour
        self.transposition_table.clear()

        # Utiliser Minimax pour trouver le meilleur mouvement
        best_position = self._find_best_position(
            grid, grid_size, ai_team_id, player_team_id, empty_positions
        )

        # Choisir un morpion (préférer les plus équilibrés pour medium/hard)
        morpion_id = self._choose_morpion(available_morpions)

        return morpion_id, best_position
    
    def _get_empty_positions(self, grid: Dict, grid_size: int) -> List[Tuple[int, int]]:
        """Obtient toutes les positions vides dans la grille."""
        empty = []
        for row in range(grid_size):
            for col in range(grid_size):
                if (row, col) not in grid:
                    empty.append((row, col))
        return empty
    
    def _random_move(self, available_morpions: List[dict],
                     empty_positions: List[Tuple[int, int]]) -> Tuple[int, Tuple[int, int]]:
        """Effectue un mouvement aléatoire."""
        morpion = random.choice(available_morpions)
        position = random.choice(empty_positions)
        return morpion['id_morpion'], position

    def _smart_random_move(self, available_morpions: List[dict],
                          empty_positions: List[Tuple[int, int]],
                          grid_size: int) -> Tuple[int, Tuple[int, int]]:
        """
        Effectue un mouvement aléatoire intelligent en privilégiant les positions centrales.
        Pour grille 4x4, les positions centrales (1,1), (1,2), (2,1), (2,2) sont stratégiques.
        """
        # Positions centrales selon la taille de grille
        if grid_size == 4:
            center_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        else:  # 3x3
            center_positions = [(1, 1)]

        # Filtrer les positions centrales disponibles
        preferred_positions = [pos for pos in empty_positions if pos in center_positions]

        # Choisir parmi les positions centrales si disponibles, sinon toutes positions
        if preferred_positions:
            position = random.choice(preferred_positions)
        else:
            position = random.choice(empty_positions)

        morpion = random.choice(available_morpions)
        return morpion['id_morpion'], position
    
    def _choose_morpion(self, available_morpions: List[dict]) -> int:
        """
        Choisit quel morpion placer à la position sélectionnée.

        Stratégie actuelle: sélection aléatoire (tous les morpions sont équivalents
        en mode normal, ils se différencient uniquement en mode avancé où ils ont des stats).

        Args:
            available_morpions: Liste des morpions disponibles à placer

        Returns:
            int: ID du morpion sélectionné

        Note: Dans une version future, cela pourrait utiliser des statistiques de parties
        précédentes pour choisir des morpions qui mènent historiquement à des victoires.
        """
        morpion = random.choice(available_morpions)
        return morpion['id_morpion']
    
    def _find_best_position(self, grid: Dict, grid_size: int,
                           ai_team_id: int, player_team_id: int,
                           empty_positions: List[Tuple[int, int]]) -> Tuple[int, int]:
        """
        Trouve la meilleure position en utilisant Minimax avec élagage Alpha-Beta.
        Optimisé avec:
        - Détection de victoires/bloquages immédiats
        - Ordonnancement des mouvements par priorité
        - Cache de transposition
        """
        # 1. VÉRIFICATION RAPIDE: Chercher victoire immédiate
        for position in empty_positions:
            test_grid = grid.copy()
            test_grid[position] = {'team_id': ai_team_id, 'morpion_id': -1}
            if check_victory_normale(test_grid, grid_size, ai_team_id):
                return position  # Gagner immédiatement!

        # 2. VÉRIFICATION RAPIDE: Bloquer victoire immédiate du joueur
        for position in empty_positions:
            test_grid = grid.copy()
            test_grid[position] = {'team_id': player_team_id, 'morpion_id': -1}
            if check_victory_normale(test_grid, grid_size, player_team_id):
                return position  # Bloquer la victoire!

        # 3. Ordonner les positions par priorité (centre > reste)
        ordered_positions = self._order_moves(empty_positions, grid_size)

        best_score = float('-inf')
        best_position = ordered_positions[0]  # Solution de repli

        # 4. Évaluer chaque position possible avec Minimax
        for position in ordered_positions:
            # Simuler le mouvement
            test_grid = grid.copy()
            test_grid[position] = {'team_id': ai_team_id, 'morpion_id': -1}

            # Calculer le score avec minimax
            score = self._minimax(
                test_grid, grid_size, 0, False,
                ai_team_id, player_team_id,
                float('-inf'), float('inf')
            )

            # Mettre à jour la meilleure position
            if score > best_score:
                best_score = score
                best_position = position

        return best_position

    def _order_moves(self, positions: List[Tuple[int, int]], grid_size: int) -> List[Tuple[int, int]]:
        """
        Ordonne les mouvements par priorité pour améliorer l'élagage alpha-beta.
        Positions centrales d'abord, puis le reste.
        """
        # Définir le centre selon la taille
        if grid_size == 4:
            center = [(1, 1), (1, 2), (2, 1), (2, 2)]
        else:  # 3x3
            center = [(1, 1)]

        # Séparer positions centrales et périphériques
        center_positions = [pos for pos in positions if pos in center]
        other_positions = [pos for pos in positions if pos not in center]

        # Retourner centre d'abord
        return center_positions + other_positions
    
    def _minimax(self, grid: Dict, grid_size: int, depth: int,
                 is_maximizing: bool, ai_team_id: int, player_team_id: int,
                 alpha: float, beta: float) -> float:
        """
        Algorithme Minimax avec élagage Alpha-Beta pour la recherche optimale de coups.

        Minimax: Algorithme récursif qui suppose un jeu optimal des deux joueurs.
        - Maximise le score pour l'IA (pire cas: le joueur joue parfaitement)
        - Minimise le score quand l'adversaire joue

        Élagage Alpha-Beta: Optimisation qui élimine les branches de l'arbre qui ne peuvent
        affecter la décision finale, réduisant la complexité de O(b^d) à O(b^(d/2)).

        Optimisations supplémentaires:
        - Cache de transposition: mémorise les positions déjà évaluées
        - Profondeur adaptative: réduite pour grilles 4x4

        Args:
            grid: État actuel de la grille {(row,col): {'team_id': X}}
            grid_size: Taille de la grille (3 ou 4)
            depth: Profondeur actuelle (0 = racine, s'incrémente avec la récursion)
            is_maximizing: True = tour IA (maximiser), False = tour joueur (minimiser)
            ai_team_id: ID de l'équipe de l'IA
            player_team_id: ID de l'équipe du joueur
            alpha: Meilleur score garanti pour le maximiseur (initialement -∞)
            beta: Meilleur score garanti pour le minimiseur (initialement +∞)

        Returns:
            float: Score de la position évaluée
                   +10 à -10: Victoire/Défaite (ajusté par la profondeur)
                   -10 à +10: Évaluation heuristique des positions intermédiaires

        Stratégie de scoring:
            - Victoire IA: +10 - depth (les victoires rapides valent plus)
            - Victoire joueur: depth - 10 (les défaites lentes sont moins graves)
            - Égalité/profondeur maximale: heuristique basée sur les lignes partielles
        """
        # Vérifier le cache de transposition
        grid_hash = self._hash_grid(grid)
        if grid_hash in self.transposition_table:
            return self.transposition_table[grid_hash]

        # Conditions de terminaison: Victoire détectée
        if check_victory_normale(grid, grid_size, ai_team_id):
            return 10 - depth  # Préférer les victoires en moins de tours
        if check_victory_normale(grid, grid_size, player_team_id):
            return depth - 10  # Les défaites tardives sont moins critiques

        # Sélectionner la profondeur maximale selon la taille de grille
        max_depth = self.max_depth_4x4 if grid_size == 4 else self.max_depth_3x3

        # Condition de terminaison: Profondeur maximale ou grille pleine
        empty_positions = self._get_empty_positions(grid, grid_size)
        if not empty_positions or depth >= max_depth:
            result = self._evaluate_position(grid, grid_size, ai_team_id, player_team_id)
            self.transposition_table[grid_hash] = result
            return result

        # Ordonner les mouvements pour améliorer l'élagage
        ordered_positions = self._order_moves(empty_positions, grid_size)

        # Tour IA: Maximiser le score (chercher le meilleur mouvement pour l'IA)
        if is_maximizing:
            max_score = float('-inf')
            for position in ordered_positions:
                # Simuler le coup de l'IA
                test_grid = grid.copy()
                test_grid[position] = {'team_id': ai_team_id, 'morpion_id': -1}

                # Récursion: évaluer la réponse du joueur
                score = self._minimax(
                    test_grid, grid_size, depth + 1, False,
                    ai_team_id, player_team_id, alpha, beta
                )
                max_score = max(max_score, score)
                alpha = max(alpha, score)  # Mettre à jour la limite inférieure

                # Élagage Beta: Si beta ≤ alpha, le minimiseur ne choisira jamais cette branche
                # (il a déjà une meilleure option dans un autre nœud)
                if beta <= alpha:
                    break

            self.transposition_table[grid_hash] = max_score
            return max_score

        # Tour Joueur: Minimiser le score (pire cas pour l'IA)
        else:
            min_score = float('inf')
            for position in ordered_positions:
                # Simuler le coup du joueur
                test_grid = grid.copy()
                test_grid[position] = {'team_id': player_team_id, 'morpion_id': -1}

                # Récursion: évaluer la réponse de l'IA
                score = self._minimax(
                    test_grid, grid_size, depth + 1, True,
                    ai_team_id, player_team_id, alpha, beta
                )
                min_score = min(min_score, score)
                beta = min(beta, score)  # Mettre à jour la limite supérieure

                # Élagage Alpha: Si beta ≤ alpha, le maximiseur ne choisira jamais cette branche
                # (il a déjà une meilleure option garantie)
                if beta <= alpha:
                    break

            self.transposition_table[grid_hash] = min_score
            return min_score

    def _hash_grid(self, grid: Dict) -> int:
        """
        Génère un hash de la grille pour le cache de transposition.
        Utilise les positions et team_ids pour créer une signature unique.
        """
        # Créer une représentation triable de la grille
        grid_tuple = tuple(sorted((pos, cell['team_id']) for pos, cell in grid.items()))
        return hash(grid_tuple)
    
    def _evaluate_position(self, grid: Dict, grid_size: int,
                          ai_team_id: int, player_team_id: int) -> float:
        """
        Évalue une position sans victoire claire.
        Retourne un score basé sur les lignes potentielles.
        """
        ai_score = self._count_potential_lines(grid, grid_size, ai_team_id)
        player_score = self._count_potential_lines(grid, grid_size, player_team_id)
        return ai_score - player_score
    
    def _count_potential_lines(self, grid: Dict, grid_size: int, team_id: int) -> float:
        """
        Compte les lignes potentielles (partiellement complétées) pour une équipe.
        """
        score = 0.0

        # Obtenir les positions de l'équipe
        team_positions = {pos for pos, cell in grid.items() if cell['team_id'] == team_id}

        # Vérifier les lignes horizontales
        for row in range(grid_size):
            count = sum(1 for col in range(grid_size) if (row, col) in team_positions)
            if count > 0:
                score += count ** 2

        # Vérifier les lignes verticales
        for col in range(grid_size):
            count = sum(1 for row in range(grid_size) if (row, col) in team_positions)
            if count > 0:
                score += count ** 2

        # Vérifier la diagonale principale
        count = sum(1 for i in range(grid_size) if (i, i) in team_positions)
        if count > 0:
            score += count ** 2

        # Vérifier la diagonale secondaire
        count = sum(1 for i in range(grid_size) if (i, grid_size - 1 - i) in team_positions)
        if count > 0:
            score += count ** 2

        return score


def get_ai_team_id(connexion):
    """
    Obtient l'ID de l'équipe IA depuis la base de données.

    Returns:
        int | None: ID de l'équipe IA ou None si elle n'existe pas
    """
    from .db_utils import execute_select_query_dict

    query = "SELECT id_team FROM team WHERE name = %s"
    result = execute_select_query_dict(connexion, query, ['🤖 IA Opponent'])

    if result and len(result) > 0:
        return result[0]['id_team']

    logger.warning("L'équipe IA n'existe pas. Exécutez init.py pour la créer.")
    return None


def is_ai_team(team_name):
    """
    Vérifie si un nom d'équipe correspond à l'équipe IA.

    Args:
        team_name: Nom de l'équipe

    Returns:
        bool: True si c'est l'équipe IA
    """
    return team_name == '🤖 IA Opponent' if team_name else False

