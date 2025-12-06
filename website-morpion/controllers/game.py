"""
Contrôleur pour gérer une partie normale de morpion (Fonctionnalité 3).
Version minimaliste : uniquement le placement de morpions.
"""

from models.model_pg import (
    get_teams_for_game_selection,
    create_config,
    create_game,
    get_game_with_details,
    get_team_morpions_for_game,
    add_log_entry,
    get_game_logs,
    update_game_end,
    check_game_end_conditions,
)
from models.ai_engine import MorpionAI, get_ai_team_id, is_ai_team
from constants import ALLOWED_GRID_SIZES, MIN_TURNS, MAX_TURNS
from controllers.game_session_utils import (
    get_or_init_game_state,
    mark_logs_dirty,
    get_logs_with_cache,
    get_requested_game_id as get_game_id_from_params,
    setup_request_defaults as setup_defaults_shared,
    sync_game_state,
    display_game_end_message,
)
from logzero import logger

# Ces variables sont injectées par server.py, mais on définit des valeurs
# par défaut pour éviter les erreurs lors des analyses statiques/linters.
try:
    SESSION  # type: ignore  # noqa: F821
    REQUEST_VARS  # type: ignore  # noqa: F821
    GET  # type: ignore  # noqa: F821
    POST  # type: ignore  # noqa: F821
except NameError:
    SESSION = {}
    REQUEST_VARS = {}
    GET = {}
    POST = {}


NORMAL_GAME_DEFAULTS = {
    'cells': dict,
    'morpions_state': dict,
    'turn': lambda: 1,
    'current_player': lambda: 1,
    'used_morpions_by_team': dict,  # {team_id: set(morpion_ids)} - ÚNICO NECESARIO
    'team1_morpions': list,
    'team2_morpions': list,
    'game_details': lambda: None,
    'state_dirty': lambda: True,
    'logs_cache': list,
    'logs_dirty': lambda: True,
    'is_ai_game': lambda: False,
    'ai_difficulty': lambda: 'medium',
}


def get_or_init_game_session(game_id, connexion):
    """Charge ou initialise l'état du jeu depuis SESSION."""
    session_key = f'game_{game_id}'

    def loader():
        game = get_game_with_details(connexion, game_id)
        if not game:
            return None

        team1_morpions = get_team_morpions_for_game(connexion, game['team1_id'])
        team2_morpions = get_team_morpions_for_game(connexion, game['team2_id'])
        
        # Détecter automatiquement si l'adversaire est l'IA
        is_ai_game = is_ai_team(game.get('team2_name', ''))
        ai_difficulty = 'medium'  # Por defecto

        return {
            'cells': {},
            'morpions_state': {},
            'turn': 1,
            'current_player': 1,
            'team1_morpions': team1_morpions,
            'team2_morpions': team2_morpions,
            'game_id': game_id,
            'team1_id': game['team1_id'],
            'team2_id': game['team2_id'],
            'grid_size': game['grid_size'],
            'max_turns': game['max_turns'],
            'game_details': game,
            'state_dirty': True,
            'used_morpions_by_team': {game['team1_id']: set(), game['team2_id']: set()},
            'logs_cache': [],
            'logs_dirty': True,
            'is_ai_game': is_ai_game,
            'ai_difficulty': ai_difficulty,
        }

    game_state = get_or_init_game_state(SESSION, session_key, loader, NORMAL_GAME_DEFAULTS)
    if game_state:
        # Asegurar que used_morpions_by_team existe (backward compatibility)
        if 'used_morpions_by_team' not in game_state:
            game_state['used_morpions_by_team'] = {
                game_state['team1_id']: set(), 
                game_state['team2_id']: set()
            }
        SESSION[session_key] = game_state
    return game_state


def place_morpion(game_state, REQUEST_VARS, team_id, morpion_id, position, morpion_template):
    """
    Helper pour placer un morpion (joueur humain ou IA) sans dupliquer la logique.
    """
    row, col = position
    
    # Crear estado inicial del morpion
    REQUEST_VARS['morpions_state'][morpion_id] = {
        'hp': morpion_template['hp'],
        'attack': morpion_template['attack'],
        'mana': morpion_template['mana'],
        'accuracy': morpion_template['accuracy']
    }
    
    # Colocar en la grille
    REQUEST_VARS['grid'][position] = {
        'team_id': team_id,
        'morpion_id': morpion_id
    }
    
    # Marcar morpion como usado por este equipo
    game_state['used_morpions_by_team'][team_id].add(morpion_id)
    game_state['state_dirty'] = True


def get_available_morpions(game_state, team_morpions, team_id):
    """
    Retourne les morpions encore disponibles pour une équipe.
    """
    used_by_team = game_state.get('used_morpions_by_team', {}).get(team_id, set())
    return [m for m in team_morpions if m['id_morpion'] not in used_by_team]


def get_all_used_morpions(game_state):
    """
    Retorna una lista de todos los morpions usados (por ambos equipos).
    Helper function para mantener compatibilidad con check_game_end_conditions.
    """
    used_by_team = game_state.get('used_morpions_by_team', {})
    all_used = set()
    for team_id, morpions in used_by_team.items():
        all_used.update(morpions)
    return list(all_used)


def setup_request_defaults():
    """Initialise les clés attendues par le template (wrapper para función compartida)."""
    setup_defaults_shared(REQUEST_VARS, ALLOWED_GRID_SIZES, advanced_mode=False)


def finalize_end_conditions(end_conditions, game_state, game, game_id, session_key, connexion, add_log=True):
    """
    Applique la clôture de partie (wrapper para función compartida).
    """
    return display_game_end_message(
        end_conditions, game_state, game, REQUEST_VARS, connexion,
        game_id, session_key, SESSION, add_log_entry, update_game_end,
        get_game_with_details, add_log
    )


def refresh_logs_cache(game_state, session_key, connexion, game_id):
    """Recharge les logs à partir du cache SESSION et des données BD."""
    REQUEST_VARS['logs'] = get_logs_with_cache(
        game_state,
        SESSION,
        session_key,
        get_game_logs,
        connexion,
        game_id,
        limit=50,
    )


def populate_request_vars_from_state(game_state, game):
    """Met à jour REQUEST_VARS à partir de l'état SESSION."""
    REQUEST_VARS['page_mode'] = 'play'
    REQUEST_VARS['game'] = game
    REQUEST_VARS['game_over'] = False
    REQUEST_VARS['ai_just_played'] = False
    REQUEST_VARS['grid'] = game_state.get('cells', {})
    REQUEST_VARS['morpions_state'] = game_state.get('morpions_state', {})
    REQUEST_VARS['current_turn'] = game_state.get('turn', 1)
    REQUEST_VARS['current_player'] = game_state.get('current_player', 1)
    # Eliminar used_morpions (legacy) - ahora usamos used_morpions_by_team
    REQUEST_VARS['team1_morpions'] = game_state.get('team1_morpions', [])
    REQUEST_VARS['team2_morpions'] = game_state.get('team2_morpions', [])
    game_state.setdefault('state_dirty', True)
    game_state.setdefault('logs_cache', [])
    game_state.setdefault('logs_dirty', True)


def ensure_game_details_loaded(game_state, game_id, session_key, connexion):
    """Garantit que game_details est disponible dans SESSION."""
    game = game_state.get('game_details')
    if not game:
        game = get_game_with_details(connexion, game_id)
        if game:
            game_state['game_details'] = game
            SESSION[session_key] = game_state
    return game


def handle_ai_turn(game_state, game, game_id, grid_size, session_key, connexion):
    """Joue automatiquement le tour de l'IA si nécessaire."""
    ai_team_id = game_state['team2_id']
    ai_used = game_state['used_morpions_by_team'].get(ai_team_id, set())
    ai_available = [
        m for m in REQUEST_VARS['team2_morpions']
        if m['id_morpion'] not in ai_used
    ]
    if not ai_available:
        return

    # Si la grille est pleine, ne pas tenter de jouer (évite l'exception de l'IA)
    if len(REQUEST_VARS['grid']) >= grid_size * grid_size:
        logger.warning("Tour IA ignoré : aucune case libre.")
        return

    ai_difficulty = game_state.get('ai_difficulty', 'medium')
    ai = MorpionAI(difficulty=ai_difficulty)

    try:
        ai_morpion_id, ai_position = ai.choose_move(
            REQUEST_VARS['grid'],
            grid_size,
            game_state['team2_id'],
            game_state['team1_id'],
            ai_available,
        )
        ai_morpion = next(
            morpion for morpion in REQUEST_VARS['team2_morpions']
            if morpion['id_morpion'] == ai_morpion_id
        )
        place_morpion(
            game_state,
            REQUEST_VARS,
            game_state['team2_id'],
            ai_morpion_id,
            ai_position,
            ai_morpion,
        )

        REQUEST_VARS['current_player'] = 1
        REQUEST_VARS['current_turn'] += 1
        game_state['cells'] = REQUEST_VARS['grid']
        game_state['morpions_state'] = REQUEST_VARS['morpions_state']
        game_state['turn'] = REQUEST_VARS['current_turn']
        game_state['current_player'] = REQUEST_VARS['current_player']
        SESSION[session_key] = game_state

        ai_log = (
            f"IA ({game['team2_name']}) a placé '{ai_morpion['name']}' "
            f"en position ({ai_position[0]+1}, {ai_position[1]+1})"
        )
        add_log_entry(connexion, game_id, ai_log)
        mark_logs_dirty(game_state, SESSION, session_key)
        REQUEST_VARS['ai_just_played'] = True
    except Exception as exc:  # pragma: no cover - robustesse CLI
        logger.error(f"Erreur lors du tour de l'IA: {exc}")


def process_player_turn(game_state, game, game_id, session_key, connexion):
    """Traite un coup humain (validation + éventuel tour IA)."""
    has_position = 'position' in POST
    has_row_col = 'row' in POST and 'col' in POST
    if 'morpion_id' not in POST or (not has_position and not has_row_col):
        return

    if REQUEST_VARS['game_over']:
        REQUEST_VARS['message'] = "❌ La partie est déjà terminée. Vous ne pouvez plus jouer."
        REQUEST_VARS['message_class'] = "alert-warning"
        return

    try:
        morpion_id = int(POST.get('morpion_id', [''])[0])

        if has_position:
            position_str = POST.get('position', [''])[0]
            try:
                row, col = map(int, position_str.split(','))
            except (ValueError, AttributeError):
                REQUEST_VARS['message'] = "❌ Format de position invalide."
                REQUEST_VARS['message_class'] = "alert-error"
                raise ValueError("Format de position invalide")
        else:
            row = int(POST.get('row', [''])[0])
            col = int(POST.get('col', [''])[0])

        grid_size = game_state['grid_size']
        current_player = REQUEST_VARS['current_player']
        team_id = game_state['team1_id'] if current_player == 1 else game_state['team2_id']

        errors = []
        if row < 0 or row >= grid_size or col < 0 or col >= grid_size:
            errors.append(
                f"Position invalide: ({row}, {col}) doit être entre (0, 0) et ({grid_size-1}, {grid_size-1})"
            )

        position = (row, col)
        if position in REQUEST_VARS['grid']:
            errors.append(f"La position ({row+1}, {col+1}) est déjà occupée")

        game_state.setdefault(
            'used_morpions_by_team',
            {game_state['team1_id']: set(), game_state['team2_id']: set()},
        )
        used_by_current_team = game_state['used_morpions_by_team'].get(team_id, set())
        if morpion_id in used_by_current_team:
            errors.append(f"Ce morpion (ID: {morpion_id}) a déjà été utilisé par votre équipe")

        if current_player == 1:
            morpion_template = next(
                (m for m in REQUEST_VARS['team1_morpions'] if m['id_morpion'] == morpion_id),
                None,
            )
        else:
            morpion_template = next(
                (m for m in REQUEST_VARS['team2_morpions'] if m['id_morpion'] == morpion_id),
                None,
            )

        if not morpion_template:
            errors.append(f"Ce morpion (ID: {morpion_id}) n'appartient pas à votre équipe")

        if errors:
            REQUEST_VARS['message'] = "❌ " + " | ".join(errors)
            REQUEST_VARS['message_class'] = "alert-error"
            return

        place_morpion(game_state, REQUEST_VARS, team_id, morpion_id, position, morpion_template)

        next_player = 2 if current_player == 1 else 1
        REQUEST_VARS['current_player'] = next_player
        REQUEST_VARS['current_turn'] += 1

        game_state['cells'] = REQUEST_VARS['grid']
        game_state['morpions_state'] = REQUEST_VARS['morpions_state']
        game_state['turn'] = REQUEST_VARS['current_turn']
        game_state['current_player'] = REQUEST_VARS['current_player']
        SESSION[session_key] = game_state

        team_name = game['team1_name'] if current_player == 1 else game['team2_name']
        log_message = (
            f"Joueur {current_player} ({team_name}) a placé le morpion "
            f"'{morpion_template['name']}' (ID: {morpion_id}) en position ({row+1}, {col+1})"
        )
        add_log_entry(connexion, game_id, log_message)
        mark_logs_dirty(game_state, SESSION, session_key)

        end_conditions = check_game_end_conditions(
            REQUEST_VARS['grid'],
            grid_size,
            REQUEST_VARS['current_turn'],
            game_state['max_turns'],
            game_state['team1_id'],
            game_state['team2_id'],
            team1_morpions=REQUEST_VARS['team1_morpions'],
            team2_morpions=REQUEST_VARS['team2_morpions'],
            used_morpions=get_all_used_morpions(game_state),
        )

        game = finalize_end_conditions(
            end_conditions,
            game_state,
            game,
            game_id,
            session_key,
            connexion,
            add_log=True,
        )

        if REQUEST_VARS['game_over']:
            return game

        if game_state.get('is_ai_game') and REQUEST_VARS['current_player'] == 2:
            handle_ai_turn(game_state, game, game_id, grid_size, session_key, connexion)

            end_conditions = check_game_end_conditions(
                REQUEST_VARS['grid'],
                grid_size,
                REQUEST_VARS['current_turn'],
                game_state['max_turns'],
                game_state['team1_id'],
                game_state['team2_id'],
                team1_morpions=REQUEST_VARS['team1_morpions'],
                team2_morpions=REQUEST_VARS['team2_morpions'],
                used_morpions=get_all_used_morpions(game_state),
            )

            game = finalize_end_conditions(
                end_conditions,
                game_state,
                game,
                game_id,
                session_key,
                connexion,
                add_log=True,
            )

        if REQUEST_VARS['game_over']:
            return game

        if not REQUEST_VARS['game_over']:
            REQUEST_VARS['message'] = (
                f"✅ Morpion '{morpion_template['name']}' placé avec succès en ({row+1}, {col+1})"
            )
            REQUEST_VARS['message_class'] = "alert-success"

            current_player = REQUEST_VARS['current_player']
            next_team_id = game_state['team1_id'] if current_player == 1 else game_state['team2_id']
            next_team_morpions = (
                REQUEST_VARS['team1_morpions']
                if current_player == 1
                else REQUEST_VARS['team2_morpions']
            )
            REQUEST_VARS['available_morpions'] = get_available_morpions(
                game_state,
                next_team_morpions,
                next_team_id,
            )
            game_state['state_dirty'] = False
            SESSION[session_key] = game_state

        return game
    except (ValueError, KeyError, TypeError) as exc:
        REQUEST_VARS['message'] = f"❌ Erreur lors du traitement du coup: {str(exc)}"
        REQUEST_VARS['message_class'] = "alert-error"
        return game


def handle_available_morpions(game_state, game, game_id, session_key, connexion):
    """Calcule les morpions disponibles et gère le cas où les deux équipes n'ont plus de pièces."""
    current_player = REQUEST_VARS['current_player']
    current_team_id = game_state['team1_id'] if current_player == 1 else game_state['team2_id']
    current_team_morpions = (
        REQUEST_VARS['team1_morpions']
        if current_player == 1
        else REQUEST_VARS['team2_morpions']
    )

    REQUEST_VARS['available_morpions'] = get_available_morpions(
        game_state,
        current_team_morpions,
        current_team_id,
    )

    team1_available = get_available_morpions(
        game_state, REQUEST_VARS['team1_morpions'], game_state['team1_id']
    )
    team2_available = get_available_morpions(
        game_state, REQUEST_VARS['team2_morpions'], game_state['team2_id']
    )

    if len(team1_available) == 0 and len(team2_available) == 0:
        end_conditions = {
            'game_over': True,
            'winner_team_id': None,
            'reason': 'no_morpions',
        }
        game = finalize_end_conditions(
            end_conditions,
            game_state,
            game,
            game_id,
            session_key,
            connexion,
            add_log=True,
        )
        REQUEST_VARS['available_morpions'] = []
        return game

    return game


def handle_setup_mode(connexion):
    """Gère l'écran de configuration d'une nouvelle partie."""
    REQUEST_VARS['page_mode'] = 'setup'
    REQUEST_VARS['teams'] = get_teams_for_game_selection(connexion)

    if len(REQUEST_VARS['teams']) < 2:
        REQUEST_VARS['message'] = "Il faut au moins 2 équipes avec 6 morpions ou plus pour jouer."
        REQUEST_VARS['message_class'] = "alert-warning"

    if 'team1_id' not in POST:
        return

    game_id = None
    try:
        team1_id = int(POST.get('team1_id', [''])[0])
        opponent_type = POST.get('opponent_type', ['human'])[0]

        is_ai_game = opponent_type.startswith('ai_')
        ai_difficulty = None
        team2_id = None

        if is_ai_game:
            ai_team_id = get_ai_team_id(connexion)
            if not ai_team_id:
                REQUEST_VARS['message'] = (
                    "❌ L'équipe IA n'existe pas. "
                    "Veuillez exécuter le script SQL: website-morpion/sql/add_ai_team.sql"
                )
                REQUEST_VARS['message_class'] = "alert-error"
                raise ValueError("Équipe IA manquante")
            team2_id = ai_team_id
            ai_difficulty = opponent_type.replace('ai_', '')
        else:
            team2_id = int(POST.get('team2_id', [''])[0])

        grid_size = int(POST.get('grid_size', [''])[0])
        max_turns = int(POST.get('max_turns', [''])[0])

        if team1_id == team2_id:
            REQUEST_VARS['message'] = "❌ Les équipes sélectionnées doivent être différentes."
            REQUEST_VARS['message_class'] = "alert-warning"
            return

        validation_errors = []
        if grid_size not in ALLOWED_GRID_SIZES:
            validation_errors.append(f"Taille de grille invalide. Choisissez parmi {ALLOWED_GRID_SIZES}.")
        if max_turns < MIN_TURNS or max_turns > MAX_TURNS:
            validation_errors.append(
                f"Le nombre de tours doit être compris entre {MIN_TURNS} et {MAX_TURNS}."
            )

        if validation_errors:
            REQUEST_VARS['message'] = "❌ " + " ".join(validation_errors)
            REQUEST_VARS['message_class'] = "alert-error"
            return

        config_id = create_config(connexion, grid_size, max_turns)
        game_id = create_game(connexion, team1_id, team2_id, config_id)

        if game_id:
            session_key = f'game_{game_id}'
            game = get_game_with_details(connexion, game_id)
            team1_morpions = get_team_morpions_for_game(connexion, game['team1_id'])
            team2_morpions = get_team_morpions_for_game(connexion, game['team2_id'])

            SESSION[session_key] = {
                'cells': {},
                'morpions_state': {},
                'turn': 1,
                'current_player': 1,
                'team1_morpions': team1_morpions,
                'team2_morpions': team2_morpions,
                'game_id': game_id,
                'team1_id': game['team1_id'],
                'team2_id': game['team2_id'],
                'grid_size': game['grid_size'],
                'max_turns': game['max_turns'],
                'game_details': game,
                'state_dirty': True,
                'used_morpions_by_team': {game['team1_id']: set(), game['team2_id']: set()},
                'logs_cache': [],
                'logs_dirty': True,
                'is_ai_game': is_ai_game,
                'ai_difficulty': ai_difficulty or 'medium',
            }

            opponent_text = f"IA ({ai_difficulty})" if is_ai_game else "joueur 2"
            REQUEST_VARS['message'] = f"✅ Partie créée contre {opponent_text}! (#{game_id})"
            REQUEST_VARS['message_class'] = "alert-success"
            REQUEST_VARS['game_created_id'] = game_id
    except Exception as exc:  # pragma: no cover - erreurs pilotées par input utilisateur
        REQUEST_VARS['message'] = f"❌ Erreur: {str(exc)}"
        REQUEST_VARS['message_class'] = "alert-error"


setup_request_defaults()

connexion = SESSION["CONNEXION"]

# Extraire game_id éventuel depuis l'URL (format /partie/<id>)
url_components = REQUEST_VARS.get('url_components', [])
game_id_from_path = url_components[1] if len(url_components) > 1 else None
game_id_str = get_game_id_from_params(game_id_from_path, GET, POST)

if not game_id_str:
    handle_setup_mode(connexion)
else:
    try:
        game_id = int(game_id_str)
        session_key = f'game_{game_id}'
        game_state = get_or_init_game_session(game_id, connexion)

        if not game_state:
            REQUEST_VARS['message'] = "❌ Partie introuvable."
            REQUEST_VARS['message_class'] = "alert-error"
            REQUEST_VARS['page_mode'] = 'setup'
        else:
            game = ensure_game_details_loaded(game_state, game_id, session_key, connexion)
            if not game:
                REQUEST_VARS['message'] = "❌ Partie introuvable."
                REQUEST_VARS['message_class'] = "alert-error"
                REQUEST_VARS['page_mode'] = 'setup'
            else:
                populate_request_vars_from_state(game_state, game)

                if game.get('ended_at'):
                    end_reason = 'victory' if game.get('id_winner') else 'grid_full'
                    finalize_end_conditions(
                        {
                            'game_over': True,
                            'winner_team_id': game.get('id_winner'),
                            'reason': end_reason,
                        },
                        game_state,
                        game,
                        game_id,
                        session_key,
                        connexion,
                        add_log=False,
                    )
                else:
                    if game_state.get('state_dirty', True):
                        end_conditions = check_game_end_conditions(
                            REQUEST_VARS['grid'],
                            game_state['grid_size'],
                            REQUEST_VARS['current_turn'],
                            game_state['max_turns'],
                            game_state['team1_id'],
                            game_state['team2_id'],
                            team1_morpions=REQUEST_VARS['team1_morpions'],
                            team2_morpions=REQUEST_VARS['team2_morpions'],
                            used_morpions=get_all_used_morpions(game_state),
                        )
                        game = finalize_end_conditions(
                            end_conditions,
                            game_state,
                            game,
                            game_id,
                            session_key,
                            connexion,
                            add_log=False,
                        )
                    else:
                        game_state['state_dirty'] = False
                        SESSION[session_key] = game_state

                    if not REQUEST_VARS['game_over']:
                        game = handle_available_morpions(
                            game_state,
                            game,
                            game_id,
                            session_key,
                            connexion,
                        )

                    if not REQUEST_VARS['game_over']:
                        game = process_player_turn(
                            game_state,
                            game,
                            game_id,
                            session_key,
                            connexion,
                        ) or game

                        if not REQUEST_VARS['game_over']:
                            game = handle_available_morpions(
                                game_state,
                                game,
                                game_id,
                                session_key,
                                connexion,
                            )
                            game_state['state_dirty'] = False
                            SESSION[session_key] = game_state

                refresh_logs_cache(game_state, session_key, connexion, game_id)

    except ValueError:
        REQUEST_VARS['message'] = "❌ ID invalide."
        REQUEST_VARS['message_class'] = "alert-error"
        REQUEST_VARS['page_mode'] = 'setup'
    except Exception as exc:  # pragma: no cover - trace utilisateur
        REQUEST_VARS['message'] = f"❌ Erreur inattendue: {str(exc)}"
        REQUEST_VARS['message_class'] = "alert-error"
