"""
Contrôleur pour lister les équipes et permettre leur suppression.
"""

from models.model_pg import (
    get_all_teams_with_morpions,
    delete_team,
    get_games_for_team,
    get_games_for_teams,
)
from constants import TEAM_GAMES_HISTORY_LIMIT

REQUEST_VARS.setdefault('message', None)
REQUEST_VARS.setdefault('message_class', None)
REQUEST_VARS.setdefault('team_to_delete', None)
REQUEST_VARS.setdefault('games_to_delete', None)
REQUEST_VARS.setdefault('teams_index', {})

def load_teams_with_games(connexion):
    """
    Récupère la liste des équipes et enrichit chaque entrée avec ses parties.
    """
    teams_with_morpions = get_all_teams_with_morpions(connexion)
    team_ids = [team['id_team'] for team in teams_with_morpions]
    games_map = get_games_for_teams(connexion, team_ids, limit_per_team=TEAM_GAMES_HISTORY_LIMIT)
    index = {}
    for team in teams_with_morpions:
        games = games_map.get(team['id_team'], [])
        total_games = games[0].get('total_games') if games and 'total_games' in games[0] else len(games)
        for game in games:
            game.pop('total_games', None)
            game.pop('rn', None)
        team['games'] = games
        team['games_displayed'] = len(games)
        team['games_count'] = total_games
        index[team['id_team']] = team
    return teams_with_morpions


def refresh_teams_context(connexion):
    """
    Recharge REQUEST_VARS['teams'] avec les données complètes (morpions + parties).
    """
    teams = load_teams_with_games(connexion)
    REQUEST_VARS["teams"] = teams
    REQUEST_VARS['teams_index'] = {team['id_team']: team for team in teams}
    return REQUEST_VARS["teams"]


def clear_confirmation_context():
    REQUEST_VARS['team_to_delete'] = None
    REQUEST_VARS['games_to_delete'] = None


teams = refresh_teams_context(SESSION["CONNEXION"])

# Traitement de la suppression
# On déclenche la logique de suppression dès qu'un team_id est envoyé en POST
if 'team_id' in POST:
    team_id_str = POST.get('team_id', [''])[0].strip()
    
    if not team_id_str:
        REQUEST_VARS['message'] = "Erreur : aucun identifiant d'équipe fourni."
        REQUEST_VARS['message_class'] = "alert-error"
        clear_confirmation_context()
    else:
        try:
            team_id = int(team_id_str)
            
            # Trouver l'équipe et ses parties via index
            team_to_delete = REQUEST_VARS.get('teams_index', {}).get(team_id)
            
            if team_to_delete is None:
                REQUEST_VARS['message'] = "Erreur : équipe introuvable."
                REQUEST_VARS['message_class'] = "alert-error"
                clear_confirmation_context()
            else:
                # Vérifier si l'équipe est utilisée dans des parties
                games = get_games_for_team(SESSION["CONNEXION"], team_id)
                
                if len(games) > 0:
                    # L'équipe est utilisée dans des parties
                    # Vérifier si l'utilisateur a confirmé la suppression des parties
                    if 'confirm_delete_games' in POST:
                        # L'utilisateur a confirmé : supprimer les parties puis l'équipe
                        delete_games = POST.get('confirm_delete_games', [''])[0].strip().lower() == 'yes'
                        
                        if delete_games:
                            success = delete_team(SESSION["CONNEXION"], team_id, delete_games=True)
                            
                            if success:
                                REQUEST_VARS['message'] = f"L'équipe '{team_to_delete['name']}' et ses {len(games)} partie(s) associée(s) ont été supprimées avec succès !"
                                REQUEST_VARS['message_class'] = "alert-success"
                                teams = refresh_teams_context(SESSION["CONNEXION"])
                                clear_confirmation_context()
                            else:
                                REQUEST_VARS['message'] = "Erreur : impossible de supprimer l'équipe et ses parties."
                                REQUEST_VARS['message_class'] = "alert-error"
                                clear_confirmation_context()
                        else:
                            # L'utilisateur a choisi de conserver les parties
                            REQUEST_VARS['message'] = "Suppression annulée : l'équipe est conservée car elle est utilisée dans des parties."
                            REQUEST_VARS['message_class'] = "alert-info"
                            clear_confirmation_context()
                    else:
                        # Afficher les parties et demander confirmation
                        REQUEST_VARS['team_to_delete'] = team_to_delete
                        REQUEST_VARS['games_to_delete'] = games
                        REQUEST_VARS['message'] = f"L'équipe '{team_to_delete['name']}' est utilisée dans {len(games)} partie(s). Souhaitez-vous supprimer ces parties également ?"
                        REQUEST_VARS['message_class'] = "alert-warning"
                else:
                    # L'équipe n'est pas utilisée dans des parties : demander confirmation via message/component
                    confirm_delete_team = POST.get('confirm_delete_team', [''])[0].strip().lower()

                    if confirm_delete_team == 'yes':
                        success = delete_team(SESSION["CONNEXION"], team_id, delete_games=False)
                        if success:
                            REQUEST_VARS['message'] = f"L'équipe '{team_to_delete['name']}' a été supprimée avec succès !"
                            REQUEST_VARS['message_class'] = "alert-success"
                            teams = refresh_teams_context(SESSION["CONNEXION"])
                            clear_confirmation_context()
                        else:
                            REQUEST_VARS['message'] = "Erreur : impossible de supprimer l'équipe."
                            REQUEST_VARS['message_class'] = "alert-error"
                            clear_confirmation_context()
                    elif confirm_delete_team == 'no':
                        REQUEST_VARS['message'] = "Suppression annulée : l'équipe a été conservée."
                        REQUEST_VARS['message_class'] = "alert-info"
                        clear_confirmation_context()
                    else:
                        REQUEST_VARS['team_to_delete'] = team_to_delete
                        REQUEST_VARS['games_to_delete'] = []
                        REQUEST_VARS['message'] = f"Confirmez la suppression de l'équipe '{team_to_delete['name']}'. Cette action est irréversible."
                        REQUEST_VARS['message_class'] = "alert-warning"
        except ValueError:
            REQUEST_VARS['message'] = "Erreur : identifiant d'équipe invalide."
            REQUEST_VARS['message_class'] = "alert-error"
            clear_confirmation_context()
        except Exception as e:
            REQUEST_VARS['message'] = f"Erreur lors de la suppression : {str(e)}"
            REQUEST_VARS['message_class'] = "alert-error"
            clear_confirmation_context()
