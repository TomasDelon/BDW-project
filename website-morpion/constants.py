"""
Constantes globales pour le projet Morpion Masters.
Centraliser ici les règles métier pour éviter les valeurs magiques.
"""

MIN_MORPIONS_PER_TEAM = 6
MAX_MORPIONS_PER_TEAM = 8

ALLOWED_GRID_SIZES = (3, 4)
MIN_TURNS = 5
MAX_TURNS = 50

# Ajustes autorisés por el professeur para que los jets fallen menos
SUCCESS_RATE_SCALE = 1.6  # multiplica la probabilidad base (10 × réussite)
SUCCESS_RATE_FLAT_BONUS = 10.0  # bonus plano tras el escalado, antes de hacer clamp

TEAM_GAMES_HISTORY_LIMIT = 5

ERROR_MESSAGES = {
    "team_name_required": "Erreur : le nom de l'équipe est obligatoire.",
    "team_color_required": "Erreur : la couleur de l'équipe est obligatoire.",
    "morpions_required": "Erreur : vous devez sélectionner au moins un morpion.",
    "team_exists": "Erreur : une équipe avec le nom '{name}' et la couleur '{color}' existe déjà.",
    "color_exists": "Erreur : une équipe avec la couleur '{color}' existe déjà (la couleur doit être unique).",
}
