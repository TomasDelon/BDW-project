-- Script de actualización para añadir equipo de IA
-- Ejecutar este script en bases de datos existentes

-- Crear equipo de IA si no existe
INSERT INTO team (name, color) 
VALUES ('🤖 IA Opponent', 'gray')
ON CONFLICT (name, color) DO NOTHING;

-- Asignar morpions a la IA (6 morpions equilibrados)
-- Solo si no tiene morpions asignados
DO $$
DECLARE
    ai_team_id INTEGER;
    morpion_count INTEGER;
BEGIN
    -- Obtener ID del equipo IA
    SELECT id_team INTO ai_team_id 
    FROM team 
    WHERE name = '🤖 IA Opponent' 
    LIMIT 1;
    
    -- Si el equipo existe, verificar y asignar morpions
    IF ai_team_id IS NOT NULL THEN
        -- Contar morpions asignados
        SELECT COUNT(*) INTO morpion_count
        FROM team_morpion
        WHERE team_id = ai_team_id;
        
        -- Si no tiene morpions, asignarlos
        IF morpion_count = 0 THEN
            INSERT INTO team_morpion (team_id, morpion_id)
            SELECT ai_team_id, id_morpion
            FROM morpion
            WHERE id_morpion IN (1, 2, 3, 5, 8, 10);
            
            RAISE NOTICE 'Equipo IA creado con 6 morpions (ID: %)', ai_team_id;
        ELSE
            RAISE NOTICE 'El equipo IA ya tiene % morpions asignados', morpion_count;
        END IF;
    ELSE
        RAISE NOTICE 'No se pudo crear el equipo IA';
    END IF;
END $$;

-- Verificar resultado
SELECT 
    t.id_team AS "ID Equipo",
    t.name AS "Nombre",
    t.color AS "Color",
    COUNT(tm.morpion_id) AS "Cantidad Morpions"
FROM team t
LEFT JOIN team_morpion tm ON t.id_team = tm.team_id
WHERE t.name LIKE '%IA Opponent%'
GROUP BY t.id_team, t.name, t.color;

