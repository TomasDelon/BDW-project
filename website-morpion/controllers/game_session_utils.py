"""
Helpers shared by controllers/game.py et controllers/game_advanced.py
pour factoriser la gestion de SESSION et des logs.
"""
from typing import Any, Callable, Dict, Optional, Tuple, List


DefaultFactory = Callable[[], Any]


def build_session_key(prefix: str, game_id: int) -> str:
    """Construit la clé de session standardisée."""
    return f"{prefix}_{game_id}"


def _resolve_default(value: Any) -> Any:
    """Évalue une fabrique si nécessaire pour éviter les références partagées."""
    return value() if callable(value) else value


def _apply_defaults(target: Dict[str, Any], defaults: Dict[str, Any]) -> None:
    """Complète target avec les valeurs par défaut manquantes."""
    for key, factory in defaults.items():
        if key not in target:
            target[key] = _resolve_default(factory)


def get_or_init_game_state(
    session_store: Dict[str, Any],
    session_key: str,
    loader_fn: Callable[[], Optional[Dict[str, Any]]],
    defaults: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Récupère l'état en SESSION ou exécute loader_fn pour l'initialiser.
    Applique les valeurs par défaut fournies.
    """
    if session_key in session_store:
        state = session_store[session_key]
        _apply_defaults(state, defaults)
        return state

    state = loader_fn()
    if state is None:
        return None

    _apply_defaults(state, defaults)
    session_store[session_key] = state
    return state


def mark_logs_dirty(
    game_state: Dict[str, Any],
    session_store: Dict[str, Any],
    session_key: str,
) -> None:
    """Indique que les logs doivent être rafraîchis."""
    game_state['logs_dirty'] = True
    session_store[session_key] = game_state


def get_logs_with_cache(
    game_state: Dict[str, Any],
    session_store: Dict[str, Any],
    session_key: str,
    fetch_logs_fn: Callable[..., Any],
    *fetch_args: Any,
    **fetch_kwargs: Any,
) -> Any:
    """Retourne les logs en utilisant le cache stocké en SESSION."""
    logs_cache = game_state.get('logs_cache', [])
    if game_state.get('logs_dirty', True) or logs_cache is None:
        logs_cache = fetch_logs_fn(*fetch_args, **fetch_kwargs)
        game_state['logs_cache'] = logs_cache
        game_state['logs_dirty'] = False
        session_store[session_key] = game_state
    return logs_cache


def get_requested_game_id(game_id_from_path: Optional[str], GET: Dict, POST: Dict) -> str:
    """
    Récupère l'identifiant de partie depuis GET/POST ou l'URL.

    Args:
        game_id_from_path: ID extrait de l'URL (ex: /partie/<id>)
        GET: Dictionnaire des paramètres GET
        POST: Dictionnaire des paramètres POST

    Returns:
        str: L'ID de la partie ou chaîne vide si non trouvé
    """
    if 'game_id' in GET:
        return GET.get('game_id', [''])[0]
    if 'game_id' in POST:
        return POST.get('game_id', [''])[0]
    if game_id_from_path:
        return game_id_from_path
    return ''


def setup_request_defaults(REQUEST_VARS: Dict[str, Any],
                           allowed_grid_sizes: List[int],
                           advanced_mode: bool = False) -> None:
    """
    Initialise les clés attendues par le template pour éviter les KeyError.

    Args:
        REQUEST_VARS: Dictionnaire des variables de requête à initialiser
        allowed_grid_sizes: Liste des tailles de grille autorisées
        advanced_mode: Si True, ajoute les clés spécifiques au mode avancé
    """
    # Clés communes aux deux modes
    REQUEST_VARS.setdefault('message', None)
    REQUEST_VARS.setdefault('message_class', None)
    REQUEST_VARS.setdefault('page_mode', 'setup')
    REQUEST_VARS.setdefault('teams', [])
    REQUEST_VARS.setdefault('allowed_grid_sizes', allowed_grid_sizes)
    REQUEST_VARS.setdefault('game_created_id', None)
    REQUEST_VARS.setdefault('game', None)
    REQUEST_VARS.setdefault('grid', {})
    REQUEST_VARS.setdefault('morpions_state', {})
    REQUEST_VARS.setdefault('current_turn', 1)
    REQUEST_VARS.setdefault('current_player', 1)
    REQUEST_VARS.setdefault('team1_morpions', [])
    REQUEST_VARS.setdefault('team2_morpions', [])
    REQUEST_VARS.setdefault('available_morpions', [])
    REQUEST_VARS.setdefault('game_over', False)
    REQUEST_VARS.setdefault('logs', [])

    # Clés spécifiques au mode avancé
    if advanced_mode:
        REQUEST_VARS.setdefault('destroyed_cells', [])
        REQUEST_VARS.setdefault('used_morpions', [])
        REQUEST_VARS.setdefault('used_morpions_set', set())
        REQUEST_VARS.setdefault('selected_action', 'place')
        REQUEST_VARS.setdefault('selected_attacker_pos', None)
        REQUEST_VARS.setdefault('selected_spell_type', None)
        REQUEST_VARS.setdefault('selected_spell_caster_pos', None)
        REQUEST_VARS.setdefault('action_processed', False)
    else:
        # Clés específicas al modo normal (para AI)
        REQUEST_VARS.setdefault('ai_just_played', False)


def sync_game_state(game_state: Dict[str, Any],
                   REQUEST_VARS: Dict[str, Any],
                   session_store: Dict[str, Any],
                   session_key: str,
                   advanced_mode: bool = False) -> None:
    """
    Sincroniza el estado del juego desde REQUEST_VARS hacia SESSION.
    Evita duplicación de las ~8 líneas de asignación repetidas.

    Args:
        game_state: Estado del juego a actualizar
        REQUEST_VARS: Variables de la petición con datos actuales
        session_store: Almacén de sesión (SESSION)
        session_key: Clave de sesión (ej: 'game_123')
        advanced_mode: Si True, sincroniza campos adicionales del modo avanzado
    """
    game_state['cells'] = REQUEST_VARS['grid']
    game_state['morpions_state'] = REQUEST_VARS['morpions_state']
    game_state['turn'] = REQUEST_VARS['current_turn']
    game_state['current_player'] = REQUEST_VARS['current_player']

    if advanced_mode:
        game_state['used_morpions'] = REQUEST_VARS.get('used_morpions', [])
        game_state['used_morpions_set'] = REQUEST_VARS.get('used_morpions_set', set())
        game_state['used_morpions_by_team'] = REQUEST_VARS.get('used_morpions_by_team', {})
        game_state['destroyed_cells'] = REQUEST_VARS.get('destroyed_cells', [])

    session_store[session_key] = game_state


def display_game_end_message(
    end_conditions: Dict[str, Any],
    game_state: Dict[str, Any],
    game: Dict[str, Any],
    REQUEST_VARS: Dict[str, Any],
    connexion: Any,
    game_id: int,
    session_key: str,
    session_store: Dict[str, Any],
    add_log_entry_fn: Callable,
    update_game_end_fn: Callable,
    get_game_with_details_fn: Callable,
    add_log: bool = True
) -> Dict[str, Any]:
    """
    Gestiona el final del juego: actualiza BD, muestra mensajes y logs.
    Consolida la lógica duplicada 4 veces en game_advanced.py.

    Args:
        end_conditions: Diccionario con 'game_over', 'winner_team_id', 'reason'
        game_state: Estado actual del juego
        game: Detalles del juego desde BD
        REQUEST_VARS: Variables de petición (para setear mensajes)
        connexion: Conexión a BD
        game_id: ID de la partida
        session_key: Clave de sesión
        session_store: Almacén de sesión (SESSION)
        add_log_entry_fn: Función para agregar logs
        update_game_end_fn: Función para marcar partida como terminada
        get_game_with_details_fn: Función para recargar datos de partida
        add_log: Si True, agrega entrada al log

    Returns:
        Dict: Datos actualizados del juego
    """
    if not end_conditions['game_over']:
        return game

    REQUEST_VARS['game_over'] = True
    REQUEST_VARS['available_morpions'] = []
    winner_id = end_conditions['winner_team_id']

    # Actualizar BD
    update_game_end_fn(connexion, game_id, winner_id)

    # Recargar datos actualizados
    refreshed_game = get_game_with_details_fn(connexion, game_id) or game
    REQUEST_VARS['game'] = refreshed_game
    game_state['game_details'] = refreshed_game
    session_store[session_key] = game_state

    reason = end_conditions.get('reason')

    # Determinar nombre del ganador si existe
    winner_name = None
    if winner_id:
        winner_name = (
            refreshed_game['team1_name']
            if winner_id == game_state.get('team1_id')
            else refreshed_game['team2_name']
        )

    # Generar mensajes según la razón de fin
    if reason == 'victory' and winner_name:
        end_log = f"🎉 Partie terminée ! {winner_name} a gagné par victoire (ligne complète) !"
        REQUEST_VARS['message'] = f"🎉 {winner_name} a gagné ! Ligne complète réalisée."
        REQUEST_VARS['message_class'] = "alert-success"
    elif reason == 'all_morpions_dead':
        if winner_name:
            end_log = f"🎉 Partie terminée ! {winner_name} a gagné par élimination complète !"
            REQUEST_VARS['message'] = f"🎉 {winner_name} a gagné ! Tous les morpions adverses ont été éliminés."
            REQUEST_VARS['message_class'] = "alert-success"
        else:
            end_log = "🤝 Partie terminée ! Tous les morpions éliminés - Match nul."
            REQUEST_VARS['message'] = "🤝 Match nul ! Tous les morpions ont été éliminés."
            REQUEST_VARS['message_class'] = "alert-info"
    elif reason == 'grid_full':
        end_log = "🤝 Partie terminée ! Grille pleine - Match nul."
        REQUEST_VARS['message'] = "🤝 Match nul ! La grille est pleine."
        REQUEST_VARS['message_class'] = "alert-info"
    elif reason == 'max_turns':
        max_turns = game_state.get('max_turns', '?')
        end_log = f"⏱️ Partie terminée ! Nombre maximum de tours ({max_turns}) atteint - Match nul."
        REQUEST_VARS['message'] = f"⏱️ Match nul ! Nombre maximum de tours ({max_turns}) atteint."
        REQUEST_VARS['message_class'] = "alert-info"
    elif reason == 'no_morpions':
        end_log = "🤝 Partie terminée ! Les deux équipes ont épuisé tous leurs morpions - Match nul."
        REQUEST_VARS['message'] = "🤝 Match nul ! Les deux équipes ont épuisé tous leurs morpions."
        REQUEST_VARS['message_class'] = "alert-info"
    elif reason == 'stalemate':
        end_log = "🤝 Partie terminée ! Aucune action possible - Match nul."
        REQUEST_VARS['message'] = "🤝 Match nul ! Plus aucun déplacement, attaque ou sort n'est possible."
        REQUEST_VARS['message_class'] = "alert-info"
    elif refreshed_game and refreshed_game.get('ended_at') and winner_name:
        # Fallback genérico si hay ganador
        REQUEST_VARS['message'] = f"🎉 Partie terminée ! {winner_name} a gagné."
        REQUEST_VARS['message_class'] = "alert-success"
        end_log = f"🎉 Partie terminée ! {winner_name} a gagné."
    else:
        # Fallback genérico sin ganador
        REQUEST_VARS['message'] = "🤝 Partie terminée."
        REQUEST_VARS['message_class'] = "alert-info"
        end_log = "🤝 Partie terminée."

    # Agregar log si se solicita
    if add_log:
        add_log_entry_fn(connexion, game_id, end_log)
        mark_logs_dirty(game_state, session_store, session_key)

    return refreshed_game

