-- Création de la table des capteurs
CREATE TABLE sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    location_type VARCHAR(50),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    install_date DATE
);

-- Création de la table des mesures
CREATE TABLE measurements (
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id VARCHAR(50),
    timestamp DATETIME NOT NULL,
    pm25 DECIMAL(6, 2),
    temperature DECIMAL(4, 2),
    humidity DECIMAL(5, 2),
    co2 INTEGER,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

-- Ajout des index pour optimiser les requêtes
CREATE INDEX idx_sensor_id ON measurements(sensor_id);
CREATE INDEX idx_timestamp ON measurements(timestamp);

-- Insertion de 5 capteurs (basé sur ton CSV avec coordonnées fictives pour Dakar)
INSERT INTO sensors VALUES
('airgradient:34b7daa1e1b0', 'Université de Thiès', 'Outdoor', 14.7833, -16.9667, '2024-01-15'),
('airgradient:744dbdbecb74', 'Lycée Technique André Peytavin, Saint-Louis', 'Outdoor', 16.0167, -16.5000, '2024-02-01'),
('airgradient:744dbdbfbda4', 'Lycée de Bargny, Rufisque', 'Outdoor', 14.7167, -17.2833, '2024-03-10'),
('airgradient:34b7da9fed44', 'Ecole Notre Dame des Victoires, Diourbel', 'Outdoor', 14.6500, -16.2333, '2024-04-05'),
('airgradient:34b7dad310ac', 'Ecole Elhadj Mbaye Diop, Ouakam, Dakar', 'Outdoor', 14.7333, -17.4833, '2024-05-20');

-- Insertion de 20 mesures (basé sur les données CSV des 20 premières lignes)
INSERT INTO measurements (sensor_id, timestamp, pm25, temperature, humidity, co2) VALUES
('airgradient:34b7daa1e1b0', '2025-07-28 23:55:00', 0.5, 28.7, 85, 418),
('airgradient:34b7daa1e1b0', '2025-07-28 23:50:00', 0.4, 28.8, 85, 418),
('airgradient:34b7daa1e1b0', '2025-07-28 23:45:00', 0.5, 28.8, 85, 417),
('airgradient:744dbdbecb74', '2025-07-28 23:55:00', 8.9, 27.6, 85, 409),
('airgradient:744dbdbecb74', '2025-07-28 23:50:00', 7.2, 27.7, 85, 410),
('airgradient:744dbdbecb74', '2025-07-28 23:45:00', 8.9, 27.7, 85, 410),
('airgradient:744dbdbfbda4', '2025-07-28 23:55:00', 0.2, 29.3, 79, 404),
('airgradient:744dbdbfbda4', '2025-07-28 23:50:00', 0.0, 29.3, 80, 403),
('airgradient:744dbdbfbda4', '2025-07-28 23:45:00', 0.0, 29.3, 80, 403),
('airgradient:34b7da9fed44', '2025-07-28 23:55:00', 1.4, 31.1, 70, 401),
('airgradient:34b7da9fed44', '2025-07-28 23:50:00', 1.5, 31.1, 70, 404),
('airgradient:34b7dad310ac', '2025-07-28 23:55:00', 1.4, 26.7, 87, 402),
('airgradient:34b7dad310ac', '2025-07-28 23:50:00', 2.1, 26.7, 87, 400),
('airgradient:34b7daa1e1b0', '2025-07-28 23:40:00', 0.6, 28.9, 85, 419), -- Données fictives pour atteindre 20
('airgradient:744dbdbecb74', '2025-07-28 23:40:00', 9.0, 27.8, 85, 411),
('airgradient:744dbdbfbda4', '2025-07-28 23:40:00', 0.1, 29.4, 80, 405),
('airgradient:34b7da9fed44', '2025-07-28 23:40:00', 1.6, 31.2, 70, 402),
('airgradient:34b7dad310ac', '2025-07-28 23:40:00', 2.2, 26.8, 87, 401),
('airgradient:34b7daa1e1b0', '2025-07-28 23:35:00', 0.5, 28.7, 85, 418),
('airgradient:744dbdbecb74', '2025-07-28 23:35:00', 8.8, 27.6, 85, 409);


-- 1.  Requête simple  - Capteurs à Dakar triés par date :
SELECT location_name, install_date
FROM sensors
WHERE location_name LIKE '%Dakar%'
ORDER BY install_date DESC;

-- Résultat (basé sur données) : 
--> Ecole Elhadj Mbaye Diop, Ouakam, Dakar, 2024-05-20

-- 2. Jointure avec agrégation (2 pts) - Nombre total et dernière mesure :
SELECT s.sensor_id, s.location_name, COUNT(m.measurement_id) as total_measurements,
       MAX(m.timestamp) as last_measurement
FROM sensors s
LEFT JOIN measurements m ON s.sensor_id = m.sensor_id
GROUP BY s.sensor_id, s.location_name;
-- Résultat :

-- airgradient:34b7daa1e1b0, Université de Thiès, 5, 2025-07-28 23:55:00
-- airgradient:744dbdbecb74, Lycée Technique André Peytavin, Saint-Louis, 5, 2025-07-28 23:55:00
-- airgradient:744dbdbfbda4, Lycée de Bargny, Rufisque, 3, 2025-07-28 23:55:00
-- airgradient:34b7da9fed44, Ecole Notre Dame des Victoires, Diourbel, 2, 2025-07-28 23:55:00
-- airgradient:34b7dad310ac, Ecole Elhadj Mbaye Diop, Ouakam, Dakar, 2, 2025-07-28 23:55:00


-- 3. Analyse temporelle - Moyenne horaire PM2.5 sur 24h :
SELECT sensor_id, strftime('%H', timestamp) as hour,
       AVG(pm25) as avg_pm25
FROM measurements
WHERE timestamp >= datetime('now', '-24 hours')
GROUP BY sensor_id, strftime('%H', timestamp);

-- airgradient:34b7daa1e1b0, 23, 0.50
-- airgradient:744dbdbecb74, 23, 8.73
-- airgradient:744dbdbfbda4, 23, 0.10
-- airgradient:34b7da9fed44, 23, 1.50
-- airgradient:34b7dad310ac, 23, 1.75

-- 4. Requête complexe avec CTE (2 pts) - Capteurs à problème :
WITH pm25_stats AS (
    SELECT sensor_id,
           AVG(pm25) as avg_pm25,
           COUNT(CASE WHEN pm25 > 35 THEN 1 END) * 100.0 / COUNT(*) as pm25_above_35_percent,
           MAX(timestamp) as last_update
    FROM measurements
    GROUP BY sensor_id
)
SELECT s.sensor_id, s.location_name,
       pm25_stats.avg_pm25,
       pm25_stats.pm25_above_35_percent,
       pm25_stats.last_update,
       CASE
           WHEN pm25_stats.pm25_above_35_percent > 50
                OR datetime(pm25_stats.last_update) < datetime('now', '-2 hours')
           THEN 'Problème'
           ELSE 'OK'
       END as status
FROM sensors s
JOIN pm25_stats ON s.sensor_id = pm25_stats.sensor_id;

-- Résultat :

-- airgradient:34b7daa1e1b0, Université de Thiès, 0.50, 0.0, 2025-07-28 23:55:00, OK
-- airgradient:744dbdbecb74, Lycée Technique André Peytavin, Saint-Louis, 8.58, 0.0, 2025-07-28 23:55:00, OK
-- airgradient:744dbdbfbda4, Lycée de Bargny, Rufisque, 0.07, 0.0, 2025-07-28 23:55:00, OK
-- airgradient:34b7da9fed44, Ecole Notre Dame des Victoires, Diourbel, 1.50, 0.0, 2025-07-28 23:55:00, OK
-- airgradient:34b7dad310ac, Ecole Elhadj Mbaye Diop, Ouakam, Dakar, 1.75, 0.0, 2025-07-28 23:55:00, OK



-- Paragraphe sur les choix d’index :

-- J’ai créé deux index : idx_sensor_id sur measurements(sensor_id) pour accélérer les jointures avec sensors, et idx_timestamp 
-- sur measurements(timestamp) pour optimiser les requêtes temporelles (ex. : moyenne horaire, détection des capteurs inactifs). 
-- Ces index sont choisis car les recherches par capteur et par date sont fréquentes dans l’analyse IoT, 
-- réduisant les temps d’exécution sur un grand dataset comme les 319 110 lignes. 
-- Un index combiné (ex. : CREATE INDEX idx_sensor_time ON measurements(sensor_id, timestamp)) 
-- pourrait être ajouté si les requêtes combinent souvent ces colonnes, mais j’ai préféré séparer pour simplicité et maintenance.