-- Schema SQL pour Morpion Masters (script non destructif)
-- Base de données: PostgreSQL
-- Utiliser reset.sql pour tout effacer/recréer, ce fichier ne fait que créer/remplir.

CREATE SCHEMA IF NOT EXISTS morpion;
SET search_path TO morpion;

/* ============================================
   TABLES
   ============================================ */

-- Table MORPION: Les différents morpions disponibles
CREATE TABLE morpion (
  id_morpion SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  hp INTEGER NOT NULL CHECK (hp >= 1 AND hp <= 100),
  attack INTEGER NOT NULL CHECK (attack >= 1 AND attack <= 100),
  mana INTEGER NOT NULL CHECK (mana >= 1 AND mana <= 100),
  accuracy INTEGER NOT NULL CHECK (accuracy >= 1 AND accuracy <= 100),
  image_url VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (hp + attack + mana + accuracy = 15)
);

-- Table TEAM: Les équipes créées par les joueurs
CREATE TABLE team (
  id_team SERIAL PRIMARY KEY,
  name VARCHAR(80) NOT NULL,
  color VARCHAR(40) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(name, color)
);

-- Table TEAM_MORPION: Relation many-to-many entre équipes et morpions
CREATE TABLE team_morpion (
  team_id INTEGER REFERENCES team(id_team) ON DELETE CASCADE,
  morpion_id INTEGER REFERENCES morpion(id_morpion) ON DELETE CASCADE,
  PRIMARY KEY (team_id, morpion_id)
);

-- Table GAME_CONFIG: Configuration d'une partie
CREATE TABLE game_config (
  id_config SERIAL PRIMARY KEY,
  grid_size INTEGER NOT NULL CHECK (grid_size IN (3, 4)),
  max_turns INTEGER NOT NULL CHECK (max_turns >= 5 AND max_turns <= 50),
  game_mode VARCHAR(20) DEFAULT 'normale',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE game (
  id_game SERIAL PRIMARY KEY,
  id_config INTEGER NOT NULL REFERENCES game_config(id_config) ON DELETE CASCADE,
  id_team1 INTEGER NOT NULL REFERENCES team(id_team) ON DELETE CASCADE,
  id_team2 INTEGER NOT NULL REFERENCES team(id_team) ON DELETE CASCADE,
  id_winner INTEGER REFERENCES team(id_team) ON DELETE SET NULL,
  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ended_at TIMESTAMP,
  CHECK (id_team1 != id_team2),
  CHECK (id_winner IS NULL OR id_winner IN (id_team1, id_team2))
);

CREATE TABLE game_log (
  id_log SERIAL PRIMARY KEY,
  id_game INTEGER NOT NULL REFERENCES game(id_game) ON DELETE CASCADE,
  log_num INTEGER NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(id_game, log_num)
);

/* ============================================
   INDEX pour améliorer les performances
   ============================================ */

CREATE INDEX idx_team_morpion_team ON team_morpion(team_id);
CREATE INDEX idx_team_morpion_morpion ON team_morpion(morpion_id);
CREATE INDEX idx_game_team1 ON game(id_team1);
CREATE INDEX idx_game_team2 ON game(id_team2);
CREATE INDEX idx_game_winner ON game(id_winner);
CREATE INDEX idx_game_log_game ON game_log(id_game);

/* ============================================
   DONNÉES INITIALES - MORPIONS
   ============================================ */

INSERT INTO morpion (name, hp, attack, mana, accuracy, image_url) VALUES
  ('Guerrier Écarlate', 6, 4, 3, 2, 't1.png'),
  ('Mage Azur', 3, 2, 6, 4, 't2.png'),
  ('Archer Vert', 4, 5, 3, 3, 't3.png'),
  ('Paladin Doré', 6, 3, 2, 4, 't4.png'),
  ('Assassin Noir', 3, 7, 3, 2, 't5.png'),
  ('Druide Naturel', 5, 2, 6, 2, 't6.png'),
  ('Berserker Rouge', 7, 6, 1, 1, 't7.png'),
  ('Invocateur Violet', 2, 2, 7, 4, 't8.png'),
  ('Chevalier Argenté', 6, 5, 2, 2, 't9.png'),
  ('Sorcier Sombre', 3, 3, 6, 3, 't10.png'),
  ('Ranger Forestier', 4, 5, 2, 4, 't11.png'),
  ('Prêtre Lumineux', 5, 1, 6, 3, 't12.png'),
  ('Ninja Furtif', 3, 6, 2, 4, 't13.png'),
  ('Chaman Tribal', 4, 3, 5, 3, 't14.png'),
  ('Gladiateur Bronzé', 6, 5, 1, 3, 't15.png'),
  ('Mystique Éthéré', 2, 3, 6, 4, 't16.png');

/* ============================================
   DONNÉES DE TEST (optionnel)
   ============================================ */

INSERT INTO team (name, color) VALUES
  ('Les Verts Furieux', 'green'),
  ('Les Bleus Mystiques', 'blue'),
  ('Les Rouges Ardents', 'red'),
  ('Les Jaunes Solaires', 'yellow'),
  ('Les Ombres Pourpres', 'purple'),
  ('Les Glaces Azures', 'cyan'),
  ('Les Brumes d''Argent', 'silver'),
  ('Les Dragons Nocturnes', 'black'),
  ('Les Tempêtes Oranges', 'orange'),
  ('Les Gardiens Turquoise', 'turquoise');

-- Morpions par équipe (6 chacun)
INSERT INTO team_morpion (team_id, morpion_id) VALUES
  -- Les Verts Furieux (ID 1)
  (1, 1), (1, 3), (1, 6), (1, 7), (1, 11), (1, 14),
  -- Les Bleus Mystiques (ID 2)
  (2, 2), (2, 8), (2, 10), (2, 12), (2, 16), (2, 4),
  -- Les Rouges Ardents (ID 3)
  (3, 1), (3, 2), (3, 5), (3, 9), (3, 13), (3, 15),
  -- Les Jaunes Solaires (ID 4)
  (4, 4), (4, 6), (4, 8), (4, 10), (4, 12), (4, 14),
  -- Les Ombres Pourpres (ID 5)
  (5, 2), (5, 5), (5, 7), (5, 11), (5, 13), (5, 16),
  -- Les Glaces Azures (ID 6)
  (6, 3), (6, 4), (6, 9), (6, 10), (6, 15), (6, 16),
  -- Les Brumes d'Argent (ID 7)
  (7, 1), (7, 6), (7, 8), (7, 12), (7, 14), (7, 15),
  -- Les Dragons Nocturnes (ID 8)
  (8, 5), (8, 7), (8, 9), (8, 11), (8, 13), (8, 16),
  -- Les Tempêtes Oranges (ID 9)
  (9, 2), (9, 4), (9, 6), (9, 8), (9, 10), (9, 12),
  -- Les Gardiens Turquoise (ID 10)
  (10, 3), (10, 5), (10, 7), (10, 9), (10, 11), (10, 13);

INSERT INTO game_config (grid_size, max_turns, game_mode) VALUES
  (3, 20, 'normale'),
  (4, 30, 'normale'),
  (3, 25, 'avancee'),
  (4, 35, 'avancee'),
  (3, 18, 'normale'),
  (4, 32, 'avancee'),
  (3, 22, 'normale'),
  (4, 28, 'avancee'),
  (3, 24, 'normale'),
  (4, 34, 'avancee');

INSERT INTO game (id_config, id_team1, id_team2, started_at, ended_at, id_winner) VALUES
  (1, 1, 2, CURRENT_TIMESTAMP - INTERVAL '10 days', CURRENT_TIMESTAMP - INTERVAL '10 days', 1),
  (2, 3, 4, CURRENT_TIMESTAMP - INTERVAL '9 days', CURRENT_TIMESTAMP - INTERVAL '9 days', 4),
  (3, 5, 6, CURRENT_TIMESTAMP - INTERVAL '8 days', CURRENT_TIMESTAMP - INTERVAL '8 days', 5),
  (4, 7, 8, CURRENT_TIMESTAMP - INTERVAL '7 days', CURRENT_TIMESTAMP - INTERVAL '7 days', 8),
  (5, 9, 10, CURRENT_TIMESTAMP - INTERVAL '6 days', CURRENT_TIMESTAMP - INTERVAL '6 days', 9),
  (6, 1, 3, CURRENT_TIMESTAMP - INTERVAL '5 days', CURRENT_TIMESTAMP - INTERVAL '5 days', 3),
  (7, 2, 5, CURRENT_TIMESTAMP - INTERVAL '4 days', CURRENT_TIMESTAMP - INTERVAL '4 days', 2),
  (8, 4, 7, CURRENT_TIMESTAMP - INTERVAL '3 days', CURRENT_TIMESTAMP - INTERVAL '3 days', 7),
  (9, 6, 9, CURRENT_TIMESTAMP - INTERVAL '2 days', CURRENT_TIMESTAMP - INTERVAL '2 days', 6),
  (10, 8, 10, CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day', 10);

INSERT INTO game_log (id_game, log_num, message) VALUES
  (1, 1, 'Début de la partie entre Les Verts Furieux et Les Bleus Mystiques.'),
  (1, 2, 'Victoire des Verts par ligne complète.'),
  (2, 1, 'La partie commence entre Les Rouges Ardents et Les Jaunes Solaires.'),
  (2, 2, 'Les Jaunes Solaires remportent la victoire.'),
  (3, 1, 'Ombres Pourpres contre Glaces Azures - Partie avancée.'),
  (3, 2, 'Les Ombres Pourpres éliminent tous les morpions adverses.'),
  (4, 1, 'Brumes d''Argent contre Dragons Nocturnes - duel intense.'),
  (4, 2, 'Les Dragons Nocturnes dominent la grille.'),
  (5, 1, 'Tempêtes Oranges versus Gardiens Turquoise.'),
  (5, 2, 'Tempêtes Oranges prennent l''avantage final.'),
  (6, 1, 'Revanche entre Les Verts Furieux et Les Rouges Ardents.'),
  (6, 2, 'Les Rouges Ardents s''imposent grâce aux sorts.'),
  (7, 1, 'Les Bleus Mystiques défient Les Ombres Pourpres.'),
  (7, 2, 'Triomphe des Bleus après une longue bataille.'),
  (8, 1, 'Jaunes Solaires vs Brumes d''Argent.'),
  (8, 2, 'Brumes d''Argent remportent la victoire au tour 25.'),
  (9, 1, 'Glaces Azures affrontent Tempêtes Oranges.'),
  (9, 2, 'Glaces Azures alignent une diagonale gagnante.'),
  (10, 1, 'Dragons Nocturnes contre Gardiens Turquoise.'),
  (10, 2, 'Gardiens Turquoise gagnent grâce à Armageddon.');

/* ============================================
   EQUIPO DE IA (Oponente controlado por computadora)
   ============================================ */

-- Crear equipo especial para la IA
INSERT INTO team (name, color) VALUES 
  ('🤖 IA Opponent', 'gray');

-- Asignar 6 morpions equilibrados a la IA
INSERT INTO team_morpion (team_id, morpion_id)
SELECT 
  (SELECT id_team FROM team WHERE name = '🤖 IA Opponent'),
  id_morpion
FROM morpion
WHERE id_morpion IN (1, 2, 3, 5, 8, 10);
