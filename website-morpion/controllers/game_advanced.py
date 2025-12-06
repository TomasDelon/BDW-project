"""
Contrôleur pour gérer une partie avancée de morpion (Fonctionnalité 4).
Gère les combats et sorts en plus du placement de morpions.
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
    check_game_end_conditions_avancee,
    validate_attack_action,
    validate_spell_action,
    execute_attack,
    execute_boule_de_feu,
    execute_soin,
    execute_armageddon,
    can_cast_spell,
    roll_action_success,
)
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

def setup_request_defaults():
    """Initialise les clés attendues par le template (wrapper para función compartida)."""
    setup_defaults_shared(REQUEST_VARS, ALLOWED_GRID_SIZES, advanced_mode=True)

ADVANCED_GAME_DEFAULTS = {
    'cells': dict,
    'morpions_state': dict,
    'destroyed_cells': list,
    'turn': lambda: 1,
    'current_player': lambda: 1,
    'used_morpions': list,
    'used_morpions_set': set,
    'used_morpions_by_team': dict,  # {team_id: set of morpion_ids}
    'team1_morpions': list,
    'team2_morpions': list,
    'selected_action': lambda: 'place',
    'selected_attacker_pos': lambda: None,
    'selected_spell_type': lambda: None,
    'selected_spell_caster_pos': lambda: None,
    'game_details': lambda: None,
    'state_dirty': lambda: True,
    'logs_cache': list,
    'logs_dirty': lambda: True,
}


def parse_position(value):
    """Convertit une chaîne 'row,col' en tuple, retourne None si invalide."""
    try:
        if isinstance(value, (list, tuple)):
            value = value[0]
        row, col = map(int, str(value).split(','))
        return row, col
    except (ValueError, AttributeError, TypeError):
        return None


def reset_attack_selection(request_vars, game_state):
    """Réinitialise la sélection d'attaquant côté UI."""
    request_vars['selected_attacker_pos'] = None
    game_state['selected_attacker_pos'] = None


def reset_spell_state(request_vars, game_state):
    """Réinitialise la sélection de sort/casteur côté UI."""
    request_vars['selected_spell_type'] = None
    request_vars['selected_spell_caster_pos'] = None
    game_state['selected_spell_type'] = None
    game_state['selected_spell_caster_pos'] = None


def clear_spell_caster(request_vars, game_state):
    """Supprime uniquement la sélection du casteur."""
    request_vars['selected_spell_caster_pos'] = None
    game_state['selected_spell_caster_pos'] = None


def persist_ui_state(game_state, request_vars):
    """Sauvegarde l'état UI courant dans la session."""
    game_state['selected_action'] = request_vars.get('selected_action', 'place')
    game_state['selected_attacker_pos'] = request_vars.get('selected_attacker_pos')
    game_state['selected_spell_type'] = request_vars.get('selected_spell_type')
    game_state['selected_spell_caster_pos'] = request_vars.get('selected_spell_caster_pos')


def mark_morpion_dead(grid, morpions_state, position, morpion_id):
    """Retire le morpion de la grille et conserve son état (hp=0, is_dead=True)."""
    if position is not None:
        grid.pop(position, None)
    if morpion_id is None:
        return
    state = morpions_state.get(morpion_id)
    if state:
        state['hp'] = 0
        state['is_dead'] = True


def get_or_init_game_session(game_id, connexion):
    """Charge ou initialise l'état de jeu avancé depuis SESSION."""
    session_key = f'game_adv_{game_id}'

    def loader():
        game = get_game_with_details(connexion, game_id)
        if not game:
            return None

        team1_morpions = get_team_morpions_for_game(connexion, game['team1_id'])
        team2_morpions = get_team_morpions_for_game(connexion, game['team2_id'])

        return {
            'cells': {},
            'morpions_state': {},
            'destroyed_cells': [],
            'turn': 1,
            'current_player': 1,
            'used_morpions': [],
            'used_morpions_by_team': {
                game['team1_id']: set(),
                game['team2_id']: set()
            },
            'team1_morpions': team1_morpions,
            'team2_morpions': team2_morpions,
            'game_id': game_id,
            'team1_id': game['team1_id'],
            'team2_id': game['team2_id'],
            'grid_size': game['grid_size'],
            'max_turns': game['max_turns'],
            'selected_action': 'place',
            'selected_attacker_pos': None,
            'selected_spell_type': None,
            'selected_spell_caster_pos': None,
            'game_details': game,
            'state_dirty': True,
            'logs_cache': [],
            'logs_dirty': True
        }

    game_state = get_or_init_game_state(SESSION, session_key, loader, ADVANCED_GAME_DEFAULTS)
    if game_state:
        used_set = game_state.get('used_morpions_set')
        if not isinstance(used_set, set):
            game_state['used_morpions_set'] = set(used_set or game_state.get('used_morpions', []))
        # Inicializar used_morpions_by_team si no existe (para compatibilidad con partidas antiguas)
        if 'used_morpions_by_team' not in game_state:
            team1_id = game_state.get('team1_id')
            team2_id = game_state.get('team2_id')
            if team1_id and team2_id:
                # Migrar datos antiguos: construir por equipo desde used_morpions y grid
                used_by_team = {
                    team1_id: set(),
                    team2_id: set()
                }
                # Reconstruir desde el grid si existe
                grid = game_state.get('cells', {})
                for cell_data in grid.values():
                    team_id = cell_data.get('team_id')
                    morpion_id = cell_data.get('morpion_id')
                    if team_id and morpion_id and team_id in used_by_team:
                        used_by_team[team_id].add(morpion_id)
                game_state['used_morpions_by_team'] = used_by_team
            else:
                game_state['used_morpions_by_team'] = {}
        SESSION[session_key] = game_state
    return game_state


def handle_setup_mode(connexion):
    """Gère la configuration d'une partie avancée (choix des équipes/paramètres)."""
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
        team2_id = int(POST.get('team2_id', [''])[0])
        grid_size = int(POST.get('grid_size', [''])[0])
        max_turns = int(POST.get('max_turns', [''])[0])

        if team1_id == team2_id:
            REQUEST_VARS['message'] = "❌ Les équipes sélectionnées doivent être différentes."
            REQUEST_VARS['message_class'] = "alert-warning"
        else:
            validation_errors = []
            if grid_size not in ALLOWED_GRID_SIZES:
                validation_errors.append(f"Taille de grille invalide. Choisissez parmi {ALLOWED_GRID_SIZES}.")
            if max_turns < MIN_TURNS or max_turns > MAX_TURNS:
                validation_errors.append(f"Le nombre de tours doit être compris entre {MIN_TURNS} et {MAX_TURNS}.")

            if validation_errors:
                REQUEST_VARS['message'] = "❌ " + " ".join(validation_errors)
                REQUEST_VARS['message_class'] = "alert-error"
            else:
                config_id = create_config(connexion, grid_size, max_turns)
                game_id = create_game(connexion, team1_id, team2_id, config_id)

        if game_id:
            session_key = f'game_adv_{game_id}'
            game = get_game_with_details(connexion, game_id)
            team1_morpions = get_team_morpions_for_game(connexion, game['team1_id'])
            team2_morpions = get_team_morpions_for_game(connexion, game['team2_id'])

            SESSION[session_key] = {
                'cells': {},
                'morpions_state': {},
                'destroyed_cells': [],
                'turn': 1,
                'current_player': 1,
                'used_morpions': [],
                'used_morpions_by_team': {
                    game['team1_id']: set(),
                    game['team2_id']: set()
                },
                'team1_morpions': team1_morpions,
                'team2_morpions': team2_morpions,
                'game_id': game_id,
                'team1_id': game['team1_id'],
                'team2_id': game['team2_id'],
                'grid_size': game['grid_size'],
                'max_turns': game['max_turns'],
                'selected_action': 'place',
                'selected_attacker_pos': None,
                'selected_spell_type': None,
                'selected_spell_caster_pos': None,
                'game_details': game,
                'state_dirty': True,
                'used_morpions_set': set(),
                'logs_cache': [],
                'logs_dirty': True
            }

            REQUEST_VARS['message'] = f"✅ Partie avancée créée ! (#{game_id})"
            REQUEST_VARS['message_class'] = "alert-success"
            REQUEST_VARS['game_created_id'] = game_id
    except Exception as exc:  # pragma: no cover - erreurs saisie utilisateur
        REQUEST_VARS['message'] = f"❌ Erreur: {str(exc)}"
        REQUEST_VARS['message_class'] = "alert-error"

# Initialisation des variables pour chaque requête
setup_request_defaults()
connexion = SESSION["CONNEXION"]

# Extraire eventuel game_id depuis l'URL (/partie-avancee/<id>)
url_components = REQUEST_VARS.get('url_components', [])
game_id_from_path = url_components[1] if len(url_components) > 1 else None
game_id_str = get_game_id_from_params(game_id_from_path, GET, POST)

# ============================================================
# MODE SETUP: Créer une nouvelle partie avancée
# ============================================================
if not game_id_str:
    REQUEST_VARS['page_mode'] = 'setup'
    REQUEST_VARS['teams'] = get_teams_for_game_selection(connexion)
    
    if len(REQUEST_VARS['teams']) < 2:
        REQUEST_VARS['message'] = "Il faut au moins 2 équipes avec 6 morpions ou plus pour jouer."
        REQUEST_VARS['message_class'] = "alert-warning"
    
    # Création de partie
    if 'team1_id' in POST:
        game_id = None
        try:
            team1_id = int(POST.get('team1_id', [''])[0])
            team2_id = int(POST.get('team2_id', [''])[0])
            grid_size = int(POST.get('grid_size', [''])[0])
            max_turns = int(POST.get('max_turns', [''])[0])
            
            if team1_id == team2_id:
                REQUEST_VARS['message'] = "❌ Les équipes sélectionnées doivent être différentes."
                REQUEST_VARS['message_class'] = "alert-warning"
            else:
                validation_errors = []
                if grid_size not in ALLOWED_GRID_SIZES:
                    validation_errors.append(f"Taille de grille invalide. Choisissez parmi {ALLOWED_GRID_SIZES}.")
                if max_turns < MIN_TURNS or max_turns > MAX_TURNS:
                    validation_errors.append(f"Le nombre de tours doit être compris entre {MIN_TURNS} et {MAX_TURNS}.")

                if validation_errors:
                    REQUEST_VARS['message'] = "❌ " + " ".join(validation_errors)
                    REQUEST_VARS['message_class'] = "alert-error"
                else:
                    # Créer config et partie
                    config_id = create_config(connexion, grid_size, max_turns)
                    game_id = create_game(connexion, team1_id, team2_id, config_id)
                
                if game_id:
                    # Initialiser l'état de la partie avancée dans SESSION
                    session_key = f'game_adv_{game_id}'
                    game = get_game_with_details(connexion, game_id)
                    team1_morpions = get_team_morpions_for_game(connexion, game['team1_id'])
                    team2_morpions = get_team_morpions_for_game(connexion, game['team2_id'])

                    SESSION[session_key] = {
                        'cells': {},
                        'morpions_state': {},
                        'destroyed_cells': [],
                        'turn': 1,
                        'current_player': 1,
                        'used_morpions': [],
                        'used_morpions_by_team': {
                            game['team1_id']: set(),
                            game['team2_id']: set()
                        },
                        'team1_morpions': team1_morpions,
                        'team2_morpions': team2_morpions,
                        'game_id': game_id,
                        'team1_id': game['team1_id'],
                        'team2_id': game['team2_id'],
                        'grid_size': game['grid_size'],
                        'max_turns': game['max_turns'],
                        'selected_action': 'place',
                        'selected_attacker_pos': None,
                        'selected_spell_type': None,
                        'selected_spell_caster_pos': None,
                        'game_details': game,
                        'state_dirty': True,
                        'used_morpions_set': set(),
                        'logs_cache': [],
                        'logs_dirty': True
                    }

                    REQUEST_VARS['message'] = f"✅ Partie avancée créée ! (#{game_id})"
                    REQUEST_VARS['message_class'] = "alert-success"
                    REQUEST_VARS['game_created_id'] = game_id
        except Exception as e:
            REQUEST_VARS['message'] = f"❌ Erreur: {str(e)}"
            REQUEST_VARS['message_class'] = "alert-error"

# ============================================================
# MODE PLAY: Jouer une partie avancée
# ============================================================
else:
    try:
        game_id = int(game_id_str)
        game_state = get_or_init_game_session(game_id, connexion)
        
        if not game_state:
            REQUEST_VARS['message'] = "❌ Partie introuvable."
            REQUEST_VARS['message_class'] = "alert-error"
            REQUEST_VARS['page_mode'] = 'setup'
        else:
            session_key = f'game_adv_{game_id}'
            game = game_state.get('game_details')
            if not game:
                game = get_game_with_details(connexion, game_id)
                if not game:
                    REQUEST_VARS['message'] = "❌ Partie introuvable."
                    REQUEST_VARS['message_class'] = "alert-error"
                    REQUEST_VARS['page_mode'] = 'setup'
                else:
                    game_state['game_details'] = game
                    SESSION[session_key] = game_state
            if game:
                REQUEST_VARS['page_mode'] = 'play'
                REQUEST_VARS['game'] = game

                REQUEST_VARS['grid'] = game_state.get('cells', {})
                REQUEST_VARS['morpions_state'] = game_state.get('morpions_state', {})
                REQUEST_VARS['destroyed_cells'] = game_state.get('destroyed_cells', [])
                REQUEST_VARS['current_turn'] = game_state.get('turn', 1)
                REQUEST_VARS['current_player'] = game_state.get('current_player', 1)
                REQUEST_VARS['used_morpions'] = game_state.get('used_morpions', [])
                game_state.setdefault('used_morpions_set', set(game_state.get('used_morpions', [])))
                REQUEST_VARS['used_morpions_set'] = game_state['used_morpions_set']
                # Inicializar used_morpions_by_team si no existe
                if 'used_morpions_by_team' not in game_state:
                    team1_id = game_state.get('team1_id')
                    team2_id = game_state.get('team2_id')
                    if team1_id and team2_id:
                        used_by_team = {
                            team1_id: set(),
                            team2_id: set()
                        }
                        # Reconstruir desde el grid
                        grid = game_state.get('cells', {})
                        for cell_data in grid.values():
                            cell_team_id = cell_data.get('team_id')
                            morpion_id = cell_data.get('morpion_id')
                            if cell_team_id and morpion_id and cell_team_id in used_by_team:
                                used_by_team[cell_team_id].add(morpion_id)
                        game_state['used_morpions_by_team'] = used_by_team
                    else:
                        game_state['used_morpions_by_team'] = {}
                REQUEST_VARS['used_morpions_by_team'] = game_state.get('used_morpions_by_team', {})
                REQUEST_VARS['team1_morpions'] = game_state.get('team1_morpions', [])
                REQUEST_VARS['team2_morpions'] = game_state.get('team2_morpions', [])
                # UI state defaults
                game_state.setdefault('selected_action', 'place')
                game_state.setdefault('selected_attacker_pos', None)
                game_state.setdefault('selected_spell_type', None)
                game_state.setdefault('selected_spell_caster_pos', None)
                game_state.setdefault('state_dirty', True)
                game_state.setdefault('logs_cache', [])
                game_state.setdefault('logs_dirty', True)
                REQUEST_VARS['selected_action'] = game_state.get('selected_action', 'place')
                REQUEST_VARS['selected_attacker_pos'] = game_state.get('selected_attacker_pos')
                REQUEST_VARS['selected_spell_type'] = game_state.get('selected_spell_type')
                REQUEST_VARS['selected_spell_caster_pos'] = game_state.get('selected_spell_caster_pos')

            # Reset action_processed at the start of the request to allow switching modes
            REQUEST_VARS['action_processed'] = False

            state_dirty = game_state.get('state_dirty', True)
            session_key = f'game_adv_{game_id}'

            # Vérifier si la partie est déjà terminée en base
            REQUEST_VARS['game_over'] = False
            if game.get('ended_at'):
                REQUEST_VARS['game_over'] = True
                if game.get('id_winner'):
                    winner_name = game['team1_name'] if game['id_winner'] == game['team1_id'] else game['team2_name']
                    REQUEST_VARS['message'] = f"🎉 Partie terminée ! {winner_name} a gagné."
                    REQUEST_VARS['message_class'] = "alert-success"
                else:
                    REQUEST_VARS['message'] = "🤝 Partie terminée ! Match nul."
                    REQUEST_VARS['message_class'] = "alert-info"
            elif state_dirty:
                # Vérifier les conditions de fin
                end_conditions = check_game_end_conditions_avancee(
                    REQUEST_VARS['grid'],
                    game_state['grid_size'],
                    REQUEST_VARS['current_turn'],
                    game_state['max_turns'],
                    game_state['team1_id'],
                    game_state['team2_id'],
                    REQUEST_VARS['morpions_state'],
                    REQUEST_VARS['destroyed_cells'],
                    team1_morpions=REQUEST_VARS['team1_morpions'],
                    team2_morpions=REQUEST_VARS['team2_morpions'],
                    used_morpions=REQUEST_VARS['used_morpions']
                                    )

                if end_conditions['game_over']:
                    REQUEST_VARS['game_over'] = True
                    winner_id = end_conditions['winner_team_id']
                    
                    # Actualizar BD si no estaba marcada como terminada
                    update_game_end(connexion, game_id, winner_id)
                    
                    # Actualizar game para reflejar el cambio
                    game = get_game_with_details(connexion, game_id)
                    REQUEST_VARS['game'] = game
                    game_state['game_details'] = game
                    SESSION[session_key] = game_state
                    
                    # Mostrar mensaje apropiado
                    if end_conditions['reason'] == 'victory':
                        winner_name = game['team1_name'] if winner_id == game_state['team1_id'] else game['team2_name']
                        REQUEST_VARS['message'] = f"🎉 {winner_name} a gagné ! Ligne complète réalisée."
                        REQUEST_VARS['message_class'] = "alert-success"
                    elif end_conditions['reason'] == 'all_morpions_dead':
                        if winner_id:
                            winner_name = game['team1_name'] if winner_id == game_state['team1_id'] else game['team2_name']
                            REQUEST_VARS['message'] = f"🎉 {winner_name} a gagné ! Tous les morpions adverses ont été éliminés."
                            REQUEST_VARS['message_class'] = "alert-success"
                        else:
                            REQUEST_VARS['message'] = "🤝 Match nul ! Tous les morpions ont été éliminés."
                            REQUEST_VARS['message_class'] = "alert-info"
                    elif end_conditions['reason'] == 'max_turns':
                        REQUEST_VARS['message'] = f"⏱️ Match nul ! Nombre maximum de tours ({game_state['max_turns']}) atteint."
                        REQUEST_VARS['message_class'] = "alert-info"
                    elif end_conditions['reason'] == 'stalemate':
                        REQUEST_VARS['message'] = "🤝 Match nul ! Plus aucun déplacement, attaque ou sort n'est possible."
                        REQUEST_VARS['message_class'] = "alert-info"
                else:
                    game_state['state_dirty'] = False
                    SESSION[session_key] = game_state
            
            # Calculer morpions disponibles (solo si la partie no ha terminado)
            if not REQUEST_VARS['game_over']:
                current_team_morpions = REQUEST_VARS['team1_morpions'] if REQUEST_VARS['current_player'] == 1 else REQUEST_VARS['team2_morpions']
                current_team_id = game_state['team1_id'] if REQUEST_VARS['current_player'] == 1 else game_state['team2_id']
                # Usar used_morpions_by_team para filtrar solo los morpiones usados por este equipo
                used_by_team = REQUEST_VARS.get('used_morpions_by_team', {})
                used_set_for_team = used_by_team.get(current_team_id, set())
                REQUEST_VARS['available_morpions'] = [m for m in current_team_morpions if m['id_morpion'] not in used_set_for_team]
            else:
                REQUEST_VARS['available_morpions'] = []
            
            # Cargar logs desde cache (y actualizarlos si necesario)
            REQUEST_VARS['logs'] = get_logs_with_cache(
                game_state,
                SESSION,
                session_key,
                get_game_logs,
                connexion,
                game_id,
                limit=50,
            )
            
            previous_action = REQUEST_VARS.get('selected_action', 'place')
            # Récupérer l'action demandée (POST/GET)
            # On évite d'écraser la valeur si une action vient d'être traitée (ex: conserver "place" après attaque/sort)
            if 'action' in POST and not REQUEST_VARS.get('action_processed', False):
                REQUEST_VARS['selected_action'] = POST.get('action', ['place'])[0]
                REQUEST_VARS['action_processed'] = True
            elif 'action' in GET:
                REQUEST_VARS['selected_action'] = GET.get('action', ['place'])[0]
            elif REQUEST_VARS.get('selected_action') is None:
                REQUEST_VARS['selected_action'] = 'place'

            if REQUEST_VARS['selected_action'] not in {'place', 'attack', 'spell'}:
                REQUEST_VARS['selected_action'] = 'place'

            if REQUEST_VARS['selected_action'] != previous_action:
                reset_attack_selection(REQUEST_VARS, game_state)
                reset_spell_state(REQUEST_VARS, game_state)

            # Gestion des sélections UI supplémentaires via GET
            current_team_id = game_state['team1_id'] if REQUEST_VARS['current_player'] == 1 else game_state['team2_id']

            if 'select_attacker' in GET and REQUEST_VARS['selected_action'] == 'attack':
                attacker_pos = parse_position(GET.get('select_attacker'))
                if attacker_pos and attacker_pos in REQUEST_VARS['grid']:
                    cell_team = REQUEST_VARS['grid'][attacker_pos].get('team_id')
                    if cell_team == current_team_id:
                        REQUEST_VARS['selected_attacker_pos'] = attacker_pos
                        game_state['selected_attacker_pos'] = attacker_pos

            if 'reset_attacker' in GET:
                reset_attack_selection(REQUEST_VARS, game_state)

            if REQUEST_VARS['selected_action'] == 'spell':
                if 'select_spell' in GET:
                    selected_spell = GET.get('select_spell', [''])[0]
                    if selected_spell in {'boule_de_feu', 'soin', 'armageddon'}:
                        if selected_spell != REQUEST_VARS.get('selected_spell_type'):
                            clear_spell_caster(REQUEST_VARS, game_state)
                        REQUEST_VARS['selected_spell_type'] = selected_spell
                        game_state['selected_spell_type'] = selected_spell
                    else:
                        reset_spell_state(REQUEST_VARS, game_state)
                if 'reset_spell' in GET:
                    reset_spell_state(REQUEST_VARS, game_state)

                if 'select_spell_caster' in GET and REQUEST_VARS.get('selected_spell_type') in {'boule_de_feu', 'armageddon'}:
                    caster_pos = parse_position(GET.get('select_spell_caster'))
                    if caster_pos and caster_pos in REQUEST_VARS['grid']:
                        caster_team = REQUEST_VARS['grid'][caster_pos].get('team_id')
                        if caster_team == current_team_id:
                            REQUEST_VARS['selected_spell_caster_pos'] = caster_pos
                            game_state['selected_spell_caster_pos'] = caster_pos
                if 'reset_spell_caster' in GET:
                    clear_spell_caster(REQUEST_VARS, game_state)
            else:
                reset_spell_state(REQUEST_VARS, game_state)

            # Persist UI state dans la session
            session_key = f'game_adv_{game_id}'
            persist_ui_state(game_state, REQUEST_VARS)
            SESSION[session_key] = game_state

            # Pré-calculer les cibles valides pour l'attaque (affichage des boutons dans le template)
            REQUEST_VARS['attack_valid_targets'] = set()
            if REQUEST_VARS['selected_action'] == 'attack' and REQUEST_VARS.get('selected_attacker_pos'):
                attacker_pos = REQUEST_VARS['selected_attacker_pos']
                row, col = attacker_pos
                potential_targets = [
                    (row + 1, col),
                    (row - 1, col),
                    (row, col + 1),
                    (row, col - 1),
                ]
                for pos in potential_targets:
                    cell_data = REQUEST_VARS['grid'].get(pos)
                    if cell_data and cell_data.get('team_id') != current_team_id:
                        REQUEST_VARS['attack_valid_targets'].add(pos)
            
            # ============================================================
            # TRAITEMENT DES ACTIONS (POST)
            # ============================================================
            if not REQUEST_VARS['game_over']:
                # On s'apprête à traiter une action
                REQUEST_VARS['action_processed'] = False
                
                # Action demandée (POST prioritaire, sinon sélection actuelle)
                post_action = POST.get('action', [''])[0] if 'action' in POST else REQUEST_VARS['selected_action']
                
                # ACTION 1: PLACER MORPION
                if post_action == 'place' and 'morpion_id' in POST and 'position' in POST:
                    try:
                        morpion_id = int(POST.get('morpion_id', [''])[0])
                        position_str = POST.get('position', [''])[0]
                        row, col = map(int, position_str.split(','))
                        position = (row, col)
                        grid_size = game_state['grid_size']
                        current_player = REQUEST_VARS['current_player']
                        team_id = game_state['team1_id'] if current_player == 1 else game_state['team2_id']
                        
                        # Validations de base
                        errors = []
                        
                        # Valider la position dans la grille
                        if row < 0 or row >= grid_size or col < 0 or col >= grid_size:
                            errors.append(f"Position invalide: ({row}, {col})")
                        
                        # Valider case libre et non détruite
                        if position in REQUEST_VARS['destroyed_cells']:
                            errors.append(f"La position ({row+1}, {col+1}) est détruite et ne peut pas être utilisée")
                        elif position in REQUEST_VARS['grid']:
                            errors.append(f"La position ({row+1}, {col+1}) est déjà occupée")
                        
                        # Valider que le morpion n'a pas déjà été utilisé par cette équipe
                        used_by_team = REQUEST_VARS.get('used_morpions_by_team', {})
                        used_set_for_team = used_by_team.get(team_id, set())
                        if morpion_id in used_set_for_team:
                            errors.append(f"Ce morpion (ID: {morpion_id}) a déjà été utilisé par votre équipe")
                        
                        # Valider que le morpion appartient bien à l'équipe courante
                        morpion_template = None
                        if current_player == 1:
                            morpion_template = next((m for m in REQUEST_VARS['team1_morpions'] if m['id_morpion'] == morpion_id), None)
                        else:
                            morpion_template = next((m for m in REQUEST_VARS['team2_morpions'] if m['id_morpion'] == morpion_id), None)
                        
                        if not morpion_template:
                            errors.append(f"Ce morpion (ID: {morpion_id}) n'appartient pas à votre équipe")
                        
                        if errors:
                            REQUEST_VARS['message'] = "❌ " + " | ".join(errors)
                            REQUEST_VARS['message_class'] = "alert-error"
                        else:
                            # Placer le morpion sur la grille
                            REQUEST_VARS['morpions_state'][morpion_id] = {
                                'hp': morpion_template['hp'],
                                'attack': morpion_template['attack'],
                                'mana': morpion_template['mana'],
                                'accuracy': morpion_template['accuracy'],
                                'current_accuracy': morpion_template['accuracy']  # Valeur initiale de précision
                            }
                            
                            REQUEST_VARS['grid'][position] = {
                                'team_id': team_id,
                                'morpion_id': morpion_id
                            }
                            
                            # Mémoriser côté session (compatibilité anciens formats)
                            REQUEST_VARS['used_morpions'].append(morpion_id)
                            REQUEST_VARS['used_morpions_set'].add(morpion_id)
                            # Ranger le morpion dans le set de l'équipe courante
                            used_by_team = REQUEST_VARS.get('used_morpions_by_team', {})
                            if team_id not in used_by_team:
                                used_by_team[team_id] = set()
                            used_by_team[team_id].add(morpion_id)
                            REQUEST_VARS['used_morpions_by_team'] = used_by_team
                            game_state['state_dirty'] = True
                            
                            # Actualizar turno
                            next_player = 2 if current_player == 1 else 1
                            REQUEST_VARS['current_player'] = next_player
                            REQUEST_VARS['current_turn'] += 1
                            
                            session_key = f'game_adv_{game_id}'
                            game_state['cells'] = REQUEST_VARS['grid']
                            game_state['morpions_state'] = REQUEST_VARS['morpions_state']
                            game_state['turn'] = REQUEST_VARS['current_turn']
                            game_state['current_player'] = REQUEST_VARS['current_player']
                            game_state['used_morpions'] = REQUEST_VARS['used_morpions']
                            game_state['used_morpions_set'] = REQUEST_VARS['used_morpions_set']
                            game_state['destroyed_cells'] = REQUEST_VARS['destroyed_cells']
                            SESSION[session_key] = game_state
                            persist_ui_state(game_state, REQUEST_VARS)
                            SESSION[session_key] = game_state

                            # Log
                            team_name = game['team1_name'] if current_player == 1 else game['team2_name']
                            log_message = f"Joueur {current_player} ({team_name}) a placé le morpion '{morpion_template['name']}' (ID: {morpion_id}) en position ({row+1}, {col+1})"
                            add_log_entry(connexion, game_id, log_message)
                            mark_logs_dirty(game_state, SESSION, session_key)
                            
                            # Vérifier les conditions de fin
                            end_conditions = check_game_end_conditions_avancee(
                                REQUEST_VARS['grid'],
                                grid_size,
                                REQUEST_VARS['current_turn'],
                                game_state['max_turns'],
                                game_state['team1_id'],
                                game_state['team2_id'],
                                REQUEST_VARS['morpions_state'],
                                REQUEST_VARS['destroyed_cells'],
                                team1_morpions=REQUEST_VARS['team1_morpions'],
                                team2_morpions=REQUEST_VARS['team2_morpions'],
                                used_morpions=REQUEST_VARS['used_morpions']
                            )
                            
                            if end_conditions['game_over']:
                                game = display_game_end_message(
                                    end_conditions, game_state, game, REQUEST_VARS, connexion,
                                    game_id, session_key, SESSION, add_log_entry, update_game_end,
                                    get_game_with_details, add_log=True
                                )
                            else:
                                REQUEST_VARS['message'] = f"✅ Morpion '{morpion_template['name']}' placé avec succès en ({row+1}, {col+1})"
                                REQUEST_VARS['message_class'] = "alert-success"
                                
                                # Recalculer les morpions disponibles pour le joueur suivant
                                next_team_morpions = REQUEST_VARS['team1_morpions'] if next_player == 1 else REQUEST_VARS['team2_morpions']
                                used_set = REQUEST_VARS.get('used_morpions_set', set())
                                REQUEST_VARS['available_morpions'] = [m for m in next_team_morpions if m['id_morpion'] not in used_set]
                                
                                # Revenir automatiquement au mode "place" après un placement
                                REQUEST_VARS['selected_action'] = 'place'
                                REQUEST_VARS['action_processed'] = True
                                game_state['state_dirty'] = False
                                SESSION[session_key] = game_state
                                reset_attack_selection(REQUEST_VARS, game_state)
                                reset_spell_state(REQUEST_VARS, game_state)
                                persist_ui_state(game_state, REQUEST_VARS)
                                SESSION[session_key] = game_state
                    
                    except (ValueError, KeyError, TypeError) as e:
                        REQUEST_VARS['message'] = f"❌ Erreur lors du traitement du coup: {str(e)}"
                        REQUEST_VARS['message_class'] = "alert-error"
                
                # ACTION 2: ATTAQUER
                elif post_action == 'attack' and 'attacker_pos' in POST and 'target_pos' in POST:
                    try:
                        attacker_pos_str = POST.get('attacker_pos', [''])[0]
                        target_pos_str = POST.get('target_pos', [''])[0]
                        attacker_pos = tuple(map(int, attacker_pos_str.split(',')))
                        target_pos = tuple(map(int, target_pos_str.split(',')))
                        current_player = REQUEST_VARS['current_player']
                        team_id = game_state['team1_id'] if current_player == 1 else game_state['team2_id']
                        
                        # Valider l'action d'attaque
                        is_valid, error_msg = validate_attack_action(
                            REQUEST_VARS['grid'],
                            attacker_pos,
                            target_pos,
                            current_player,
                            game_state['team1_id'],
                            game_state['team2_id']
                        )
                        
                        if not is_valid:
                            REQUEST_VARS['message'] = f"❌ {error_msg}"
                            REQUEST_VARS['message_class'] = "alert-error"
                        else:
                            # Récupérer les états des morpions impliqués
                            attacker_morpion_id = REQUEST_VARS['grid'][attacker_pos]['morpion_id']
                            target_morpion_id = REQUEST_VARS['grid'][target_pos]['morpion_id']
                            attacker_state = REQUEST_VARS['morpions_state'][attacker_morpion_id]
                            target_state = REQUEST_VARS['morpions_state'][target_morpion_id]
                            
                            # Ejecutar ataque
                            attack_result = execute_attack(attacker_state, target_state)
                            
                            # Actualizar estados
                            attacker_state['current_accuracy'] = attack_result['attacker_accuracy_updated']
                            target_state['hp'] = attack_result['target_hp_updated']
                            
                            # Si el objetivo murió, remover del grid y morpions_state
                            if target_state['hp'] <= 0:
                                mark_morpion_dead(REQUEST_VARS['grid'], REQUEST_VARS['morpions_state'], target_pos, target_morpion_id)
                                target_dead_msg = " Le morpion ennemi a été éliminé !"
                            else:
                                target_dead_msg = ""
                            
                            game_state['state_dirty'] = True
                            
                            # Actualizar turno
                            next_player = 2 if current_player == 1 else 1
                            REQUEST_VARS['current_player'] = next_player
                            REQUEST_VARS['current_turn'] += 1
                            
                            session_key = f'game_adv_{game_id}'
                            game_state['cells'] = REQUEST_VARS['grid']
                            game_state['morpions_state'] = REQUEST_VARS['morpions_state']
                            game_state['turn'] = REQUEST_VARS['current_turn']
                            game_state['current_player'] = REQUEST_VARS['current_player']
                            game_state['used_morpions'] = REQUEST_VARS['used_morpions']
                            game_state['used_morpions_set'] = REQUEST_VARS['used_morpions_set']
                            game_state['used_morpions_by_team'] = REQUEST_VARS.get('used_morpions_by_team', {})
                            game_state['destroyed_cells'] = REQUEST_VARS['destroyed_cells']
                            SESSION[session_key] = game_state
                            persist_ui_state(game_state, REQUEST_VARS)
                            SESSION[session_key] = game_state

                            # Log
                            team_name = game['team1_name'] if current_player == 1 else game['team2_name']
                            attacker_name = next((m['name'] for m in (REQUEST_VARS['team1_morpions'] if current_player == 1 else REQUEST_VARS['team2_morpions']) if m['id_morpion'] == attacker_morpion_id), f"Morpion {attacker_morpion_id}")
                            
                            if attack_result['success']:
                                log_message = f"Joueur {current_player} ({team_name}) - {attacker_name} a attaqué avec succès ! {attack_result['damage_dealt']} dégâts infligés.{target_dead_msg}"
                            else:
                                log_message = f"Joueur {current_player} ({team_name}) - {attacker_name} a raté son attaque."
                            
                            add_log_entry(connexion, game_id, log_message)
                            mark_logs_dirty(game_state, SESSION, session_key)
                            
                            # Vérifier les conditions de fin
                            end_conditions = check_game_end_conditions_avancee(
                                REQUEST_VARS['grid'],
                                game_state['grid_size'],
                                REQUEST_VARS['current_turn'],
                                game_state['max_turns'],
                                game_state['team1_id'],
                                game_state['team2_id'],
                                REQUEST_VARS['morpions_state'],
                                REQUEST_VARS['destroyed_cells'],
                                team1_morpions=REQUEST_VARS['team1_morpions'],
                                team2_morpions=REQUEST_VARS['team2_morpions'],
                                used_morpions=REQUEST_VARS['used_morpions']
                            )
                            
                            if end_conditions['game_over']:
                                game = display_game_end_message(
                                    end_conditions, game_state, game, REQUEST_VARS, connexion,
                                    game_id, session_key, SESSION, add_log_entry, update_game_end,
                                    get_game_with_details, add_log=True
                                )
                            else:
                                if attack_result['success']:
                                    REQUEST_VARS['message'] = f"✅ Attaque réussie ! {attack_result['damage_dealt']} dégâts infligés.{target_dead_msg}"
                                else:
                                    REQUEST_VARS['message'] = "❌ Attaque ratée !"
                                REQUEST_VARS['message_class'] = "alert-success" if attack_result['success'] else "alert-warning"
                                
                                # Recalculer les morpions disponibles pour le joueur suivant
                                next_team_morpions = REQUEST_VARS['team1_morpions'] if next_player == 1 else REQUEST_VARS['team2_morpions']
                                next_team_id = game_state['team1_id'] if next_player == 1 else game_state['team2_id']
                                used_by_team = REQUEST_VARS.get('used_morpions_by_team', {})
                                used_set_for_team = used_by_team.get(next_team_id, set())
                                REQUEST_VARS['available_morpions'] = [m for m in next_team_morpions if m['id_morpion'] not in used_set_for_team]
                                
                                # Volver a modo "place" por defecto después del ataque
                                REQUEST_VARS['selected_action'] = 'place'
                                REQUEST_VARS['action_processed'] = True
                                game_state['state_dirty'] = False
                                SESSION[session_key] = game_state
                                reset_attack_selection(REQUEST_VARS, game_state)
                                reset_spell_state(REQUEST_VARS, game_state)
                                persist_ui_state(game_state, REQUEST_VARS)
                                SESSION[session_key] = game_state
                    
                    except (ValueError, KeyError, TypeError) as e:
                        REQUEST_VARS['message'] = f"❌ Erreur lors du traitement de l'attaque: {str(e)}"
                        REQUEST_VARS['message_class'] = "alert-error"
                
                # ACTION 3: LANCER SORT
                elif post_action == 'spell' and 'spell_type' in POST and 'target_pos' in POST:
                    try:
                        session_key = f'game_adv_{game_id}'
                        spell_type = POST.get('spell_type', [''])[0]
                        target_pos_str = POST.get('target_pos', [''])[0]
                        target_pos = tuple(map(int, target_pos_str.split(',')))
                        current_player = REQUEST_VARS['current_player']
                        team_id = game_state['team1_id'] if current_player == 1 else game_state['team2_id']
                        
                        # Récupérer la position du lanceur si elle est fournie (Armageddon)
                        caster_pos = None
                        if 'caster_pos' in POST:
                            caster_pos_str = POST.get('caster_pos', [''])[0]
                            if caster_pos_str:
                                caster_pos = tuple(map(int, caster_pos_str.split(',')))
                        
                        # Valider le sort demandé
                        is_valid, error_msg = validate_spell_action(
                            REQUEST_VARS['grid'],
                            caster_pos,
                            target_pos,
                            spell_type,
                            current_player,
                            game_state['team1_id'],
                            game_state['team2_id'],
                            REQUEST_VARS['destroyed_cells']
                        )
                        
                        if not is_valid:
                            REQUEST_VARS['message'] = f"❌ {error_msg}"
                            REQUEST_VARS['message_class'] = "alert-error"
                        else:
                            # Identifier le morpion lanceur (selon le sort choisi)
                            caster_morpion_id = None
                            caster_state = None
                            
                            if spell_type in {'boule_de_feu', 'armageddon'}:
                                if caster_pos in REQUEST_VARS['grid']:
                                    caster_morpion_id = REQUEST_VARS['grid'][caster_pos]['morpion_id']
                                    caster_state = REQUEST_VARS['morpions_state'].get(caster_morpion_id)
                            elif spell_type == 'soin':
                                if target_pos in REQUEST_VARS['grid']:
                                    caster_morpion_id = REQUEST_VARS['grid'][target_pos]['morpion_id']
                                    caster_state = REQUEST_VARS['morpions_state'].get(caster_morpion_id)
                            
                            if not caster_state:
                                REQUEST_VARS['message'] = "❌ Aucun morpion disponible pour lancer ce sort"
                                REQUEST_VARS['message_class'] = "alert-error"
                            else:
                                # Vérifier le coût en mana
                                spell_costs = {
                                    'boule_de_feu': 2,
                                    'soin': 1,
                                    'armageddon': 5
                                }
                                spell_cost = spell_costs.get(spell_type, 0)
                                
                                if not can_cast_spell(caster_state, spell_type, spell_cost):
                                    REQUEST_VARS['message'] = f"❌ Mana insuffisant pour lancer ce sort (nécessite {spell_cost} mana)"
                                    REQUEST_VARS['message_class'] = "alert-error"
                                else:
                                    # Jet de réussite commun
                                    caster_accuracy = caster_state.get('current_accuracy', caster_state.get('accuracy', 1))
                                    spell_success = roll_action_success(caster_accuracy)
                                    
                                    if not spell_success:
                                        REQUEST_VARS['message'] = "❌ Sort raté !"
                                        REQUEST_VARS['message_class'] = "alert-warning"
                                        team_name = game['team1_name'] if current_player == 1 else game['team2_name']
                                        caster_name = next((m['name'] for m in (REQUEST_VARS['team1_morpions'] if current_player == 1 else REQUEST_VARS['team2_morpions']) if m['id_morpion'] == caster_morpion_id), f"Morpion {caster_morpion_id}")
                                        miss_log = f"Joueur {current_player} ({team_name}) - {caster_name}: Sort '{spell_type}' a échoué."
                                        add_log_entry(connexion, game_id, miss_log)
                                        mark_logs_dirty(game_state, SESSION, session_key)

                                        # Consommer le tour malgré l'échec
                                        next_player = 2 if current_player == 1 else 1
                                        REQUEST_VARS['current_player'] = next_player
                                        REQUEST_VARS['current_turn'] += 1
                                        game_state['state_dirty'] = False
                                        
                                        game_state['cells'] = REQUEST_VARS['grid']
                                        game_state['morpions_state'] = REQUEST_VARS['morpions_state']
                                        game_state['turn'] = REQUEST_VARS['current_turn']
                                        game_state['current_player'] = REQUEST_VARS['current_player']
                                        game_state['used_morpions'] = REQUEST_VARS['used_morpions']
                                        game_state['used_morpions_set'] = REQUEST_VARS['used_morpions_set']
                                        game_state['used_morpions_by_team'] = REQUEST_VARS.get('used_morpions_by_team', {})
                                        game_state['destroyed_cells'] = REQUEST_VARS['destroyed_cells']
                                        SESSION[session_key] = game_state
                                        
                                        # Recalculer les morpions disponibles
                                        next_team_morpions = REQUEST_VARS['team1_morpions'] if next_player == 1 else REQUEST_VARS['team2_morpions']
                                        next_team_id = game_state['team1_id'] if next_player == 1 else game_state['team2_id']
                                        used_by_team = REQUEST_VARS.get('used_morpions_by_team', {})
                                        used_set_for_team = used_by_team.get(next_team_id, set())
                                        REQUEST_VARS['available_morpions'] = [m for m in next_team_morpions if m['id_morpion'] not in used_set_for_team]
                                        
                                        REQUEST_VARS['selected_action'] = 'place'
                                        REQUEST_VARS['action_processed'] = True
                                        reset_attack_selection(REQUEST_VARS, game_state)
                                        reset_spell_state(REQUEST_VARS, game_state)
                                        persist_ui_state(game_state, REQUEST_VARS)
                                        SESSION[session_key] = game_state
                                    else:
                                        # Ejecutar sort
                                        if spell_type == 'boule_de_feu':
                                            spell_result = execute_boule_de_feu(REQUEST_VARS['morpions_state'][REQUEST_VARS['grid'][target_pos]['morpion_id']])
                                            target_morpion_id = REQUEST_VARS['grid'][target_pos]['morpion_id']
                                            target_state = REQUEST_VARS['morpions_state'][target_morpion_id]
                                            target_state['hp'] = spell_result['target_hp_updated']
                                            caster_state['mana'] -= spell_result['mana_cost']
                                            
                                            # Si el objetivo murió, remover del grid
                                            if target_state['hp'] <= 0:
                                                mark_morpion_dead(REQUEST_VARS['grid'], REQUEST_VARS['morpions_state'], target_pos, target_morpion_id)
                                                target_dead_msg = " Le morpion ennemi a été éliminé !"
                                            else:
                                                target_dead_msg = ""
                                            
                                            spell_log = f"Boule de feu lancée ! {spell_result['damage_dealt']} dégâts infligés.{target_dead_msg}"
                                        
                                        elif spell_type == 'soin':
                                            spell_result = execute_soin(REQUEST_VARS['morpions_state'][REQUEST_VARS['grid'][target_pos]['morpion_id']])
                                            target_morpion_id = REQUEST_VARS['grid'][target_pos]['morpion_id']
                                            target_state = REQUEST_VARS['morpions_state'][target_morpion_id]
                                            target_state['hp'] = spell_result['target_hp_updated']
                                            caster_state['mana'] -= spell_result['mana_cost']
                                            
                                            spell_log = f"Sort de soin lancé ! +{spell_result['healing_done']} HP restaurés."
                                        
                                        elif spell_type == 'armageddon':
                                            spell_result = execute_armageddon(REQUEST_VARS['grid'], target_pos, REQUEST_VARS['destroyed_cells'])
                                            REQUEST_VARS['grid'] = spell_result['grid_updated']
                                            REQUEST_VARS['destroyed_cells'] = spell_result['destroyed_cells_updated']
                                            caster_state['mana'] -= spell_result['mana_cost']
                                            
                                            if spell_result['morpion_killed']:
                                                mark_morpion_dead(
                                                    REQUEST_VARS['grid'],
                                                    REQUEST_VARS['morpions_state'],
                                                    target_pos,
                                                    spell_result['morpion_id_killed']
                                                )
                                                spell_log = f"Armageddon lancé ! La case ({target_pos[0]+1}, {target_pos[1]+1}) a été détruite. Le morpion sur cette case a été éliminé."
                                            else:
                                                spell_log = f"Armageddon lancé ! La case ({target_pos[0]+1}, {target_pos[1]+1}) a été détruite."
                                        
                                        # Incrementar accuracy si sort exitoso (todos los sorts son exitosos si se lanzan)
                                        caster_state['current_accuracy'] = caster_state.get('current_accuracy', caster_state.get('accuracy', 1)) + 0.5
                                        game_state['state_dirty'] = True
                                        
                                        # Actualizar turno
                                        next_player = 2 if current_player == 1 else 1
                                        REQUEST_VARS['current_player'] = next_player
                                        REQUEST_VARS['current_turn'] += 1
                                        
                                        game_state['cells'] = REQUEST_VARS['grid']
                                        game_state['morpions_state'] = REQUEST_VARS['morpions_state']
                                        game_state['turn'] = REQUEST_VARS['current_turn']
                                        game_state['current_player'] = REQUEST_VARS['current_player']
                                        game_state['used_morpions'] = REQUEST_VARS['used_morpions']
                                        game_state['used_morpions_set'] = REQUEST_VARS['used_morpions_set']
                                        game_state['used_morpions_by_team'] = REQUEST_VARS.get('used_morpions_by_team', {})
                                        game_state['destroyed_cells'] = REQUEST_VARS['destroyed_cells']
                                        SESSION[session_key] = game_state
                                        persist_ui_state(game_state, REQUEST_VARS)
                                        SESSION[session_key] = game_state

                                        # Log
                                        team_name = game['team1_name'] if current_player == 1 else game['team2_name']
                                        caster_name = next((m['name'] for m in (REQUEST_VARS['team1_morpions'] if current_player == 1 else REQUEST_VARS['team2_morpions']) if m['id_morpion'] == caster_morpion_id), f"Morpion {caster_morpion_id}")
                                        log_message = f"Joueur {current_player} ({team_name}) - {caster_name}: {spell_log}"
                                        add_log_entry(connexion, game_id, log_message)
                                        mark_logs_dirty(game_state, SESSION, session_key)
                                        
                                        # Vérifier les conditions de fin
                                        end_conditions = check_game_end_conditions_avancee(
                                            REQUEST_VARS['grid'],
                                            game_state['grid_size'],
                                            REQUEST_VARS['current_turn'],
                                            game_state['max_turns'],
                                            game_state['team1_id'],
                                            game_state['team2_id'],
                                            REQUEST_VARS['morpions_state'],
                                            REQUEST_VARS['destroyed_cells'],
                                            team1_morpions=REQUEST_VARS['team1_morpions'],
                                            team2_morpions=REQUEST_VARS['team2_morpions'],
                                            used_morpions=REQUEST_VARS['used_morpions']
                                        )
                                        
                                        if end_conditions['game_over']:
                                            game = display_game_end_message(
                                                end_conditions, game_state, game, REQUEST_VARS, connexion,
                                                game_id, session_key, SESSION, add_log_entry, update_game_end,
                                                get_game_with_details, add_log=True
                                            )
                                        else:
                                            REQUEST_VARS['message'] = f"✅ {spell_log}"
                                            REQUEST_VARS['message_class'] = "alert-success"
                                    
                                # Recalculer les morpions disponibles pour le joueur suivant
                                    next_team_morpions = REQUEST_VARS['team1_morpions'] if next_player == 1 else REQUEST_VARS['team2_morpions']
                                    next_team_id = game_state['team1_id'] if next_player == 1 else game_state['team2_id']
                                    used_by_team = REQUEST_VARS.get('used_morpions_by_team', {})
                                    used_set_for_team = used_by_team.get(next_team_id, set())
                                    REQUEST_VARS['available_morpions'] = [m for m in next_team_morpions if m['id_morpion'] not in used_set_for_team]
                                    
                                    # Volver a modo "place" por defecto después del sort
                                    REQUEST_VARS['selected_action'] = 'place'
                                    REQUEST_VARS['action_processed'] = True
                                    reset_attack_selection(REQUEST_VARS, game_state)
                                    reset_spell_state(REQUEST_VARS, game_state)
                                    persist_ui_state(game_state, REQUEST_VARS)
                                    game_state['state_dirty'] = False
                                    SESSION[session_key] = game_state
                    
                    except (ValueError, KeyError, TypeError) as e:
                        REQUEST_VARS['message'] = f"❌ Erreur lors du traitement du sort: {str(e)}"
                        REQUEST_VARS['message_class'] = "alert-error"
            
            # Recalculer les morpions disponibles après traitement des actions POST
            if not REQUEST_VARS['game_over']:
                current_team_morpions = REQUEST_VARS['team1_morpions'] if REQUEST_VARS['current_player'] == 1 else REQUEST_VARS['team2_morpions']
                current_team_id = game_state['team1_id'] if REQUEST_VARS['current_player'] == 1 else game_state['team2_id']
                used_by_team = REQUEST_VARS.get('used_morpions_by_team', {})
                used_set_for_team = used_by_team.get(current_team_id, set())
                REQUEST_VARS['available_morpions'] = [m for m in current_team_morpions if m['id_morpion'] not in used_set_for_team]
            
            # Charger les logs de la partie (cache + limit pour éviter relectures complètes)
            logs_cache = game_state.get('logs_cache', [])
            if game_state.get('logs_dirty', True):
                logs_cache = get_game_logs(connexion, game_id, limit=50)
                game_state['logs_cache'] = logs_cache
                game_state['logs_dirty'] = False
                SESSION[session_key] = game_state
            REQUEST_VARS['logs'] = logs_cache
    
    except ValueError:
        REQUEST_VARS['message'] = "❌ ID invalide."
        REQUEST_VARS['message_class'] = "alert-error"
        REQUEST_VARS['page_mode'] = 'setup'
