"""
Utilidades para gestionar el caché y datos de sesión.
"""

__all__ = ['clear_morpions_cache']


def clear_morpions_cache(session):
    """
    Invalide le cache des morpions pour forcer un rechargement depuis la BD.
    À appeler après la création, modification ou suppression d'un morpion.

    Args:
        session: Dictionnaire de session contenant les données en cache
    """
    cache = session.get('TEAM_CREATE', {})
    if 'morpions' in cache:
        del cache['morpions']
