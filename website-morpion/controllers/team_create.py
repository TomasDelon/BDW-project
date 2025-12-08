"""
Contrôleur pour créer une nouvelle équipe avec sélection de morpions.
"""

from models.model_pg import (
    get_all_morpions,
    check_team_name_color_exists,
    check_team_color_exists,
    create_team,
    add_morpions_to_team,
)
from constants import (
    MIN_MORPIONS_PER_TEAM,
    MAX_MORPIONS_PER_TEAM,
    ERROR_MESSAGES,
)
from session_utils import clear_morpions_cache

REQUEST_VARS.setdefault('message', None)
REQUEST_VARS.setdefault('message_class', None)
REQUEST_VARS.setdefault('form_team_name', '')
REQUEST_VARS.setdefault('form_team_color', '')
REQUEST_VARS.setdefault('form_selected_morpions', [])


def get_cached_morpions(connexion):
    """
    Récupère la liste des morpions avec un cache persistant en SESSION.
    """
    cache = SESSION.setdefault('TEAM_CREATE', {})
    morpions = cache.get('morpions')
    if not morpions:
        morpions = get_all_morpions(connexion)
        cache['morpions'] = morpions
    return morpions


def refresh_morpions_context(connexion):
    REQUEST_VARS["morpions"] = get_cached_morpions(connexion)


def set_form_state(team_name, team_color, selected_ids):
    REQUEST_VARS['form_team_name'] = team_name
    REQUEST_VARS['form_team_color'] = team_color
    REQUEST_VARS['form_selected_morpions'] = selected_ids


def reset_form_state():
    set_form_state('', '', [])


def parse_selected_morpions(raw_values):
    if not raw_values:
        return []
    try:
        return [int(m_id) for m_id in raw_values]
    except ValueError:
        raise ValueError("Erreur : identifiant de morpion invalide.")


def validate_team_form(connexion, team_name, team_color, morpion_ids):
    if not team_name:
        return False, ERROR_MESSAGES["team_name_required"], "alert-error"
    if not team_color:
        return False, ERROR_MESSAGES["team_color_required"], "alert-error"
    if not morpion_ids:
        return False, ERROR_MESSAGES["morpions_required"], "alert-error"
    if len(morpion_ids) < MIN_MORPIONS_PER_TEAM:
        return False, f"Erreur : vous devez sélectionner au moins {MIN_MORPIONS_PER_TEAM} morpions (actuellement {len(morpion_ids)}).", "alert-error"
    if len(morpion_ids) > MAX_MORPIONS_PER_TEAM:
        return False, f"Erreur : vous ne pouvez pas sélectionner plus de {MAX_MORPIONS_PER_TEAM} morpions (actuellement {len(morpion_ids)}).", "alert-error"
    if check_team_name_color_exists(connexion, team_name, team_color):
        return False, ERROR_MESSAGES["team_exists"].format(name=team_name, color=team_color), "alert-error"
    if check_team_color_exists(connexion, team_color):
        return False, ERROR_MESSAGES["color_exists"].format(color=team_color), "alert-error"
    return True, None, None


refresh_morpions_context(SESSION["CONNEXION"])

# Traitement du formulaire POST
if 'team_name' in POST:
    team_name = POST.get('team_name', [''])[0].strip()
    team_color = POST.get('team_color', [''])[0].strip()
    raw_morpions = POST.get('morpions', [])

    try:
        morpion_ids = parse_selected_morpions(raw_morpions)
    except ValueError as exc:
        REQUEST_VARS['message'] = str(exc)
        REQUEST_VARS['message_class'] = "alert-error"
        set_form_state(team_name, team_color, [])
    else:
        set_form_state(team_name, team_color, morpion_ids)
        is_valid, error_message, error_class = validate_team_form(
            SESSION["CONNEXION"],
            team_name,
            team_color,
            morpion_ids,
        )

        if not is_valid:
            REQUEST_VARS['message'] = error_message
            REQUEST_VARS['message_class'] = error_class
        else:
            team_id = create_team(SESSION["CONNEXION"], team_name, team_color)

            if team_id:
                count = add_morpions_to_team(SESSION["CONNEXION"], team_id, morpion_ids)

                if count is not None:
                    REQUEST_VARS['message'] = f"L'équipe '{team_name}' a été créée avec succès avec {count} morpion(s) !"
                    REQUEST_VARS['message_class'] = "alert-success"
                    reset_form_state()
                else:
                    REQUEST_VARS['message'] = "Erreur : l'équipe a été créée mais les morpions n'ont pas pu être ajoutés."
                    REQUEST_VARS['message_class'] = "alert-error"
            else:
                REQUEST_VARS['message'] = "Erreur : impossible de créer l'équipe."
                REQUEST_VARS['message_class'] = "alert-error"
