"""
Motor de IA para el juego clásico de Morpion Masters.
Implementa Minimax con poda Alpha-Beta para decisiones óptimas.
"""

import random
from typing import Dict, Tuple, List
from logzero import logger

from .game_logic_normale import check_victory_normale


class MorpionAI:
    """
    Motor de IA para jugar contra el usuario usando el algoritmo Minimax.

    Implementa tres niveles de dificultad balanceados para ofrecer una
    experiencia de juego progresiva sin ser frustrante.
    """

    def __init__(self, difficulty='medium'):
        """
        Inicializa el motor de IA con un nivel de dificultad específico.

        Args:
            difficulty: 'easy', 'medium', 'hard'
                - easy: Minimax profundidad 2 + 60% movimientos aleatorios
                  (permite ganar al jugador, bueno para aprendizaje)
                - medium: Minimax profundidad 4 sin aleatoriedad
                  (equilibrado, tácticamente competente pero no perfecto)
                - hard: Minimax profundidad 9 (grilla completa 3x3)
                  (prácticamente imbatible, juego óptimo)

        Profundidades elegidas según análisis de complejidad:
        - Grilla 3x3: 9 posiciones → profundidad 9 explora todo el árbol
        - Profundidad 4: Equilibrio entre tiempo de respuesta (<100ms) y calidad
        - Profundidad 2: Solo 2 turnos adelante, muchos errores tácticos
        """
        self.difficulty = difficulty
        self.max_depth = {
            'easy': 2,     # ~100 nodos evaluados
            'medium': 4,   # ~10,000 nodos evaluados
            'hard': 9      # ~362,880 nodos (peor caso), pero poda reduce a ~5000
        }[difficulty]
    
    def choose_move(self, grid: Dict[Tuple[int, int], dict], 
                    grid_size: int,
                    ai_team_id: int,
                    player_team_id: int,
                    available_morpions: List[dict]) -> Tuple[int, Tuple[int, int]]:
        """
        Elige el mejor movimiento para la IA.
        
        Args:
            grid: Estado actual de la grilla
            grid_size: Tamaño de la grilla (3 o 4)
            ai_team_id: ID del equipo de la IA
            player_team_id: ID del equipo del jugador
            available_morpions: Lista de morpions disponibles para la IA
        
        Returns:
            Tuple (morpion_id, (row, col))
        """
        if not available_morpions:
            raise ValueError("No hay morpions disponibles para la IA")
        
        # Obtener todas las posiciones vacías
        empty_positions = self._get_empty_positions(grid, grid_size)
        
        if not empty_positions:
            raise ValueError("No hay posiciones vacías en la grilla")
        
        # Para dificultad fácil, a veces hacer movimientos aleatorios
        if self.difficulty == 'easy' and random.random() < 0.6:
            return self._random_move(available_morpions, empty_positions)
        
        # Usar Minimax para encontrar el mejor movimiento
        best_position = self._find_best_position(
            grid, grid_size, ai_team_id, player_team_id, empty_positions
        )
        
        # Elegir un morpion (preferir los más equilibrados para medium/hard)
        morpion_id = self._choose_morpion(available_morpions)
        
        return morpion_id, best_position
    
    def _get_empty_positions(self, grid: Dict, grid_size: int) -> List[Tuple[int, int]]:
        """Obtiene todas las posiciones vacías en la grilla."""
        empty = []
        for row in range(grid_size):
            for col in range(grid_size):
                if (row, col) not in grid:
                    empty.append((row, col))
        return empty
    
    def _random_move(self, available_morpions: List[dict], 
                     empty_positions: List[Tuple[int, int]]) -> Tuple[int, Tuple[int, int]]:
        """Realiza un movimiento aleatorio."""
        morpion = random.choice(available_morpions)
        position = random.choice(empty_positions)
        return morpion['id_morpion'], position
    
    def _choose_morpion(self, available_morpions: List[dict]) -> int:
        """
        Elige qué morpion colocar en la posición seleccionada.

        Estrategia actual: selección aleatoria (todos los morpions son equivalentes
        en modo normal, solo se diferencian en modo avanzé donde tienen stats).

        Args:
            available_morpions: Lista de morpions disponibles para colocar

        Returns:
            int: ID del morpion seleccionado

        Nota: En una versión futura, esto podría usar estadísticas de partidas
        anteriores para elegir morpions que históricamente llevan a victorias.
        """
        morpion = random.choice(available_morpions)
        return morpion['id_morpion']
    
    def _find_best_position(self, grid: Dict, grid_size: int, 
                           ai_team_id: int, player_team_id: int,
                           empty_positions: List[Tuple[int, int]]) -> Tuple[int, int]:
        """
        Encuentra la mejor posición usando Minimax con poda Alpha-Beta.
        """
        best_score = float('-inf')
        best_position = empty_positions[0]  # Fallback
        
        # Evaluar cada posición posible
        for position in empty_positions:
            # Simular el movimiento
            test_grid = grid.copy()
            test_grid[position] = {'team_id': ai_team_id, 'morpion_id': -1}
            
            # Calcular score con minimax
            score = self._minimax(
                test_grid, grid_size, 0, False, 
                ai_team_id, player_team_id,
                float('-inf'), float('inf')
            )
            
            # Actualizar mejor posición
            if score > best_score:
                best_score = score
                best_position = position
        
        return best_position
    
    def _minimax(self, grid: Dict, grid_size: int, depth: int,
                 is_maximizing: bool, ai_team_id: int, player_team_id: int,
                 alpha: float, beta: float) -> float:
        """
        Algoritmo Minimax con poda Alpha-Beta para búsqueda óptima de jugadas.

        Minimax: Algoritmo recursivo que asume juego óptimo de ambos jugadores.
        - Maximiza el score para la IA (peor caso: jugador juega perfecto)
        - Minimiza el score cuando juega el oponente

        Poda Alpha-Beta: Optimización que elimina ramas del árbol que no pueden
        afectar la decisión final, reduciendo complejidad de O(b^d) a O(b^(d/2)).

        Args:
            grid: Estado actual de la grilla {(row,col): {'team_id': X}}
            grid_size: Tamaño de la grilla (3 o 4)
            depth: Profundidad actual (0 = raíz, incrementa con recursión)
            is_maximizing: True = turno IA (maximizar), False = turno jugador (minimizar)
            ai_team_id: ID del equipo de la IA
            player_team_id: ID del equipo del jugador
            alpha: Mejor score garantizado para maximizador (inicialmente -∞)
            beta: Mejor score garantizado para minimizador (inicialmente +∞)

        Returns:
            float: Score de la posición evaluada
                   +10 a -10: Victoria/Derrota (ajustado por profundidad)
                   -10 a +10: Evaluación heurística de posiciones intermedias

        Scoring strategy:
            - Victoria IA: +10 - depth (victorias rápidas valen más)
            - Victoria jugador: depth - 10 (derrotas lentas son menos malas)
            - Empate/profundidad máxima: heurística basada en líneas parciales
        """
        # Condiciones de término: Victoria detectada
        if check_victory_normale(grid, grid_size, ai_team_id):
            return 10 - depth  # Preferir victorias en menos turnos
        if check_victory_normale(grid, grid_size, player_team_id):
            return depth - 10  # Derrotas tardías son menos críticas
        
        # Condición de término: Profundidad máxima o grilla llena
        empty_positions = self._get_empty_positions(grid, grid_size)
        if not empty_positions or depth >= self.max_depth:
            return self._evaluate_position(grid, grid_size, ai_team_id, player_team_id)

        # Turno IA: Maximizar el score (buscar mejor movimiento para IA)
        if is_maximizing:
            max_score = float('-inf')
            for position in empty_positions:
                # Simular jugada de la IA
                test_grid = grid.copy()
                test_grid[position] = {'team_id': ai_team_id, 'morpion_id': -1}

                # Recursión: evaluar respuesta del jugador
                score = self._minimax(
                    test_grid, grid_size, depth + 1, False,
                    ai_team_id, player_team_id, alpha, beta
                )
                max_score = max(max_score, score)
                alpha = max(alpha, score)  # Actualizar límite inferior

                # Poda Beta: Si beta ≤ alpha, el minimizador nunca elegirá esta rama
                # (ya tiene una mejor opción en otro nodo)
                if beta <= alpha:
                    break
            return max_score

        # Turno Jugador: Minimizar el score (peor caso para IA)
        else:
            min_score = float('inf')
            for position in empty_positions:
                # Simular jugada del jugador
                test_grid = grid.copy()
                test_grid[position] = {'team_id': player_team_id, 'morpion_id': -1}

                # Recursión: evaluar respuesta de la IA
                score = self._minimax(
                    test_grid, grid_size, depth + 1, True,
                    ai_team_id, player_team_id, alpha, beta
                )
                min_score = min(min_score, score)
                beta = min(beta, score)  # Actualizar límite superior

                # Poda Alpha: Si beta ≤ alpha, el maximizador nunca elegirá esta rama
                # (ya tiene una mejor opción garantizada)
                if beta <= alpha:
                    break
            return min_score
    
    def _evaluate_position(self, grid: Dict, grid_size: int, 
                          ai_team_id: int, player_team_id: int) -> float:
        """
        Evalúa una posición sin victoria clara.
        Retorna un score basado en líneas potenciales.
        """
        ai_score = self._count_potential_lines(grid, grid_size, ai_team_id)
        player_score = self._count_potential_lines(grid, grid_size, player_team_id)
        return ai_score - player_score
    
    def _count_potential_lines(self, grid: Dict, grid_size: int, team_id: int) -> float:
        """
        Cuenta líneas potenciales (parcialmente completadas) para un equipo.
        """
        score = 0.0
        
        # Obtener posiciones del equipo
        team_positions = {pos for pos, cell in grid.items() if cell['team_id'] == team_id}
        
        # Verificar líneas horizontales
        for row in range(grid_size):
            count = sum(1 for col in range(grid_size) if (row, col) in team_positions)
            if count > 0:
                score += count ** 2
        
        # Verificar líneas verticales
        for col in range(grid_size):
            count = sum(1 for row in range(grid_size) if (row, col) in team_positions)
            if count > 0:
                score += count ** 2
        
        # Verificar diagonal principal
        count = sum(1 for i in range(grid_size) if (i, i) in team_positions)
        if count > 0:
            score += count ** 2
        
        # Verificar diagonal secundaria
        count = sum(1 for i in range(grid_size) if (i, grid_size - 1 - i) in team_positions)
        if count > 0:
            score += count ** 2
        
        return score


def get_ai_team_id(connexion):
    """
    Obtiene el ID del equipo de IA desde la base de datos.
    
    Returns:
        int | None: ID del equipo de IA o None si no existe
    """
    from .db_utils import execute_select_query_dict
    
    query = "SELECT id_team FROM team WHERE name = %s"
    result = execute_select_query_dict(connexion, query, ['🤖 IA Opponent'])
    
    if result and len(result) > 0:
        return result[0]['id_team']
    
    logger.warning("El equipo de IA no existe. Ejecuta init.py para crearlo.")
    return None


def is_ai_team(team_name):
    """
    Verifica si un nombre de equipo corresponde al equipo de IA.
    
    Args:
        team_name: Nombre del equipo
        
    Returns:
        bool: True si es el equipo de IA
    """
    return team_name == '🤖 IA Opponent' if team_name else False

