"""
Fichier d'initialisation (constantes chargées au démarrage dans la session)
"""

from datetime import datetime
import os
from logzero import logger

SESSION['APP'] = "Morpion Masters"
SESSION['BASELINE'] = "Composez, combattez, triomphez."
SESSION['DIR_HISTORIQUE'] = os.path.join(SESSION['DIRECTORY'], "historiques")
SESSION['HISTORIQUE'] = dict()
SESSION['CURRENT_YEAR'] = datetime.now().year

# ============================================
# Vérification du bundle CSS
# ============================================
def remind_css_bundle():
    """Alerte si main.css manque ou semble plus ancien que les sources."""
    css_root = os.path.join(SESSION['DIRECTORY'], "static", "styles")
    main_css = os.path.join(css_root, "main.css")

    if not os.path.exists(main_css):
        logger.warning("main.css est absent. Exécutez `python scripts/build_css.py` après toute modification des styles.")
        return

    latest_source_mtime = 0
    for dirpath, _, filenames in os.walk(css_root):
        for filename in filenames:
            if not filename.endswith(".css") or filename == "main.css":
                continue
            latest_source_mtime = max(latest_source_mtime, os.path.getmtime(os.path.join(dirpath, filename)))

    if latest_source_mtime and os.path.getmtime(main_css) < latest_source_mtime:
        logger.warning("main.css semble obsolète. Lancez `python scripts/build_css.py` pour régénérer les styles concaténés.")

# ============================================
# Initialisation automatique du equipo de IA
# ============================================
def init_ai_team():
    """Crée l'équipe IA automatiquement si elle n'existe pas déjà."""
    try:
        connexion = SESSION.get("CONNEXION")
        if not connexion:
            logger.warning("Connexion BD indisponible : impossible de vérifier l'équipe IA.")
            return
        
        # Verificar si el equipo IA ya existe
        cursor = connexion.cursor()
        cursor.execute("SELECT id_team FROM team WHERE name = %s", ('🤖 IA Opponent',))
        result = cursor.fetchone()
        
        if result:
            logger.info(f"Équipe IA déjà présente (ID: {result[0]}).")
            return
        
        # Crear equipo IA
        logger.info("Création de l'équipe IA…")
        cursor.execute(
            "INSERT INTO team (name, color) VALUES (%s, %s) RETURNING id_team",
            ('🤖 IA Opponent', 'gray')
        )
        ai_team_id = cursor.fetchone()[0]
        logger.info(f"Équipe IA créée (ID: {ai_team_id}).")
        
        # Asignar 6 morpions al equipo IA
        morpion_ids = [1, 2, 3, 5, 8, 10]
        for morpion_id in morpion_ids:
            cursor.execute(
                "INSERT INTO team_morpion (team_id, morpion_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (ai_team_id, morpion_id)
            )
        
        logger.info(f"{len(morpion_ids)} morpions assignés à l'équipe IA.")
        logger.info("Initialisation de l'équipe IA terminée.")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de l'équipe IA: {e}")

remind_css_bundle()
# Ejecutar inicialización del equipo IA
init_ai_team()
