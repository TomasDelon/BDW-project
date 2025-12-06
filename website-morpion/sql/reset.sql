-- Réinitialisation complète du schéma morpion (⚠️ destructif)
-- Exécuter avec psql depuis le dossier sql/ pour recharger toutes les données de test.
\set ON_ERROR_STOP on

DROP SCHEMA IF EXISTS morpion CASCADE;
CREATE SCHEMA IF NOT EXISTS morpion;
SET search_path TO morpion;

-- Recharge la structure + données initiales sans devoir copier-coller.
\ir schema.sql
