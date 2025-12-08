"""
Contrôleur pour la création de morpions personnalisés.
Permet aux utilisateurs de créer leurs propres morpions avec stats et image.
"""

from models.model_pg import check_morpion_name_exists, create_custom_morpion, get_next_morpion_id
from logzero import logger
import os
import base64
from pathlib import Path
from session_utils import clear_morpions_cache

connexion = SESSION['CONNEXION']

# Dossier où sauvegarder les images
IMAGES_DIR = Path(__file__).parent.parent / 'static' / 'img' / 'morpions'
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Valeurs par défaut pour les messages
REQUEST_VARS.setdefault('message', None)
REQUEST_VARS.setdefault('message_class', None)

def validate_stats(hp, attack, mana, accuracy):
    """Valide que les stats respectent les contraintes."""
    try:
        hp = int(hp)
        attack = int(attack)
        mana = int(mana)
        accuracy = int(accuracy)

        # Vérifier que chaque stat est entre 1 et 100
        if not all(1 <= stat <= 100 for stat in [hp, attack, mana, accuracy]):
            return False, "Chaque statistique doit être entre 1 et 100", None

        # Vérifier la somme
        if hp + attack + mana + accuracy != 15:
            return False, f"La somme des statistiques doit être 15 (actuellement: {hp + attack + mana + accuracy})", None

        return True, None, (hp, attack, mana, accuracy)
    except (ValueError, TypeError):
        return False, "Les statistiques doivent être des nombres entiers", None


def process_image(image_data, morpion_id):
    """
    Traite l'image (redimensionnement à 400x400 et compression).

    Args:
        image_data: Données base64 de l'image
        morpion_id: ID du morpion pour nommer le fichier

    Returns:
        str: Nom du fichier sauvegardé ou None si erreur
    """
    try:
        from PIL import Image
        import io

        if not image_data or not image_data.startswith('data:image'):
            return None

        # Extraire les données base64
        header, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(image_bytes))

        # Redimensionner à 400x400 (même taille que t1.png, t2.png, etc.)
        img = img.convert('RGB')  # Convertir en RGB si nécessaire
        img = img.resize((400, 400), Image.Resampling.LANCZOS)

        # Nom du fichier: custom_<id>.png
        output_filename = f"custom_{morpion_id}.png"
        output_path = IMAGES_DIR / output_filename

        # Sauvegarder avec compression optimisée
        img.save(output_path, 'PNG', optimize=True, quality=85)

        logger.info(f"Image sauvegardée: {output_filename}")
        return output_filename

    except Exception as e:
        logger.error(f"Erreur traitement image: {e}")
        return None


# === TRAITEMENT GET/POST ===

if 'morpion_name' in POST:
    # Récupération des données du formulaire
    name = POST.get('morpion_name', [''])[0].strip()
    hp = POST.get('hp', [''])[0]
    attack = POST.get('attack', [''])[0]
    mana = POST.get('mana', [''])[0]
    accuracy = POST.get('accuracy', [''])[0]
    image_data = POST.get('image_data', [''])[0]  # Base64 depuis webcam

    # Validation du nom
    if not name:
        REQUEST_VARS['message'] = "Le nom du morpion est obligatoire"
        REQUEST_VARS['message_class'] = "alert-error"
    elif len(name) > 50:
        REQUEST_VARS['message'] = "Le nom ne peut pas dépasser 50 caractères"
        REQUEST_VARS['message_class'] = "alert-error"
    elif check_morpion_name_exists(connexion, name):
        REQUEST_VARS['message'] = f"Un morpion nommé '{name}' existe déjà"
        REQUEST_VARS['message_class'] = "alert-error"
    else:
        # Validation des stats
        valid, error_msg, stats = validate_stats(hp, attack, mana, accuracy)

        if not valid:
            REQUEST_VARS['message'] = error_msg
            REQUEST_VARS['message_class'] = "alert-error"
        else:
            hp, attack, mana, accuracy = stats

            # Obtenir le prochain ID
            next_id = get_next_morpion_id(connexion)

            # Traiter l'image
            image_filename = process_image(image_data, next_id)

            if not image_filename:
                REQUEST_VARS['message'] = "Une image est obligatoire"
                REQUEST_VARS['message_class'] = "alert-error"
            else:
                # Créer le morpion
                morpion_id = create_custom_morpion(
                    connexion,
                    name,
                    hp,
                    attack,
                    mana,
                    accuracy,
                    image_filename
                )

                if morpion_id:
                    REQUEST_VARS['message'] = f"Morpion '{name}' créé avec succès (ID: {morpion_id})"
                    REQUEST_VARS['message_class'] = "alert-success"
                    # Invalider le cache pour que le nouveau morpion apparaisse dans la liste
                    clear_morpions_cache(SESSION)
                    # Réinitialiser le formulaire après succès
                    name = ''
                    hp = attack = mana = accuracy = ''
                else:
                    REQUEST_VARS['message'] = "Erreur lors de la création du morpion"
                    REQUEST_VARS['message_class'] = "alert-error"

    # Conserver les valeurs du formulaire
    REQUEST_VARS['form_data'] = {
        'name': name,
        'hp': hp,
        'attack': attack,
        'mana': mana,
        'accuracy': accuracy
    }

else:
    # GET - Affichage du formulaire vide
    REQUEST_VARS['form_data'] = {
        'name': '',
        'hp': '',
        'attack': '',
        'mana': '',
        'accuracy': ''
    }

# Instructions pour l'utilisateur
REQUEST_VARS['instructions'] = {
    'stats': "La somme de HP + Attaque + Mana + Précision doit être exactement 15.",
    'image': "L'image est centrée et redimensionnée en 400x400 pixels pour correspondre aux autres morpions.",
    'upload': "Vous pouvez utiliser la webcam ou importer un fichier PNG/JPG depuis votre ordinateur."
}
