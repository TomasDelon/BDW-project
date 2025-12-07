-- Script de mise à jour pour ajouter l'équipe d'IA
-- Exécuter ce script sur les bases de données existantes

-- Créer l'équipe d'IA si elle n'existe pas
INSERT INTO team (name, color) 
VALUES ('🤖 IA Opponent', 'gray')
ON CONFLICT (name, color) DO NOTHING;

-- Assigner des morpions à l'IA (6 morpions équilibrés)
-- Uniquement si elle n'a pas de morpions assignés
DO $$
DECLARE
    ai_team_id INTEGER;
    morpion_count INTEGER;
BEGIN
    -- Obtenir l'ID de l'équipe IA
    SELECT id_team INTO ai_team_id 
    FROM team 
    WHERE name = '🤖 IA Opponent' 
    LIMIT 1;
    
    -- Si l'équipe existe, vérifier et assigner des morpions
    IF ai_team_id IS NOT NULL THEN
        -- Compter les morpions assignés
        SELECT COUNT(*) INTO morpion_count
        FROM team_morpion
        WHERE team_id = ai_team_id;
        
        -- Si elle n'a pas de morpions, les assigner
        IF morpion_count = 0 THEN
            INSERT INTO team_morpion (team_id, morpion_id)
            SELECT ai_team_id, id_morpion
            FROM morpion
            WHERE id_morpion IN (1, 2, 3, 5, 8, 10);
            
            RAISE NOTICE 'Équipe IA créée avec 6 morpions (ID: %)', ai_team_id;
        ELSE
            RAISE NOTICE 'L''équipe IA a déjà % morpions assignés', morpion_count;
        END IF;
    ELSE
        RAISE NOTICE 'Impossible de créer l''équipe IA';
    END IF;
END $$;

-- Vérifier le résultat
SELECT 
    t.id_team AS "ID Équipe",
    t.name AS "Nom",
    t.color AS "Couleur",
    COUNT(tm.morpion_id) AS "Quantité Morpions"
FROM team t
LEFT JOIN team_morpion tm ON t.id_team = tm.team_id
WHERE t.name LIKE '%IA Opponent%'
GROUP BY t.id_team, t.name, t.color;

