DROP TABLE IF EXISTS pneu_velo;
DROP TABLE IF EXISTS type_pneu_velo;

CREATE TABLE type_pneu_velo (
    id_type_pneu INT AUTO_INCREMENT PRIMARY KEY,
    libelle_type VARCHAR(50) NOT NULL
);

CREATE TABLE pneu_velo (
    id_pneu_velo INT AUTO_INCREMENT PRIMARY KEY,
    nom_pneu VARCHAR(100) NOT NULL,
    fabricant VARCHAR(100),
    modele_pneu VARCHAR(100),
    largeur_pneu DECIMAL(4,1),
    diametre_jante INT,
    dimension VARCHAR(20),
    type_pneu_id INT NOT NULL,
    prix_pneu DECIMAL(10,2),
    image VARCHAR(200),
    FOREIGN KEY (type_pneu_id) REFERENCES type_pneu_velo(id_type_pneu)
);

INSERT INTO type_pneu_velo (id_type_pneu, libelle_type) VALUES
(NULL, 'Ville'),
(NULL, 'VTT'),
(NULL, 'Route'),
(NULL, 'Vélo électrique'),
(NULL, 'Fauteuil roulant'),
(NULL, 'Enfant');

INSERT INTO pneu_velo (id_pneu_velo, nom_pneu, fabricant, modele_pneu, largeur_pneu, diametre_jante, dimension, type_pneu_id, prix_pneu, image) VALUES
(NULL, 'Pneu velo Confort Michelin', 'Michelin', 'Pneu Michelin blanc et noir', 3, 65, '22 pouces', 1, 22.00, 'pneu_michelin_blanc_noir.png'),
(NULL, 'Pneu VTT Crossmax','Mavic','Crossmax Pro', 2.4, 60, '29 pouces', 2, 55.00, 'pneu_VTT_crossmax.png'),
(NULL, 'Pneu ville CityTouring','Continental','TourRide', 3, 62, '28 pouces', 1, 35.58, 'pneu_ville_touring.png'),
(NULL, 'Pneu Route Ultrasport','Schwalbe','Ultrasport', 2, 70, '28 pouces', 3, 28.00, 'pneu_ultrasport.png'),
(NULL, 'Pneu fauteuil roulant Marathon','Schwalbe','Rightrun', 2, 35, '24 pouces', 5, 9.15, 'pneu_fauteuil_roulant_marathon.png'),
(NULL, 'Pneu Cars','Michelin','Mich&Flash', 1.3, 15, '16 pouces', 6, 15.00, 'pneu_cars.png'),
(NULL, 'Pneu Big Ben','Schwalbe','Ballon', 2.3, 30, '26 pouces', 4, 20.00, 'pneu_big_ben.png'),
(NULL, 'Pneu Touring Marathon','Schwalbe','Touring', 5, 55, '26 pouces', 3, 60.00, 'pneu_touring_marathon.png'),
(NULL, 'Pneu VTT Ikon','Maxxis','EXO', 7, 63, '29 pouces', 2, 33.99, 'pneu_VTT_Ikon.png'),
(NULL, 'Pneu Route Corsa','Veloflex','Corsa Evo', 2, 75, '25 pouces', 3, 49.26, 'pneu_route_corsa.png'),
(NULL, 'Pneu velo Zig Zag','Oxford','Noir traditionnel', 3.2, 58, '26 pouces', 1, 10.00, 'pneu_velo_zig_zag.png'),
(NULL, 'Pneu Kid Road','Bike Original','RoadTown', 1.5, 18, '18 pouces', 6, 12.00, 'pneu_kid_road.png'),
(NULL, 'Pneu VTT Syerra','Vittoria','TLR G2', 3, 46, '27 pouces', 2, 44.99, 'pneu_VTT_syerra.png'),
(NULL, 'Pneu Energy','Michelin','ElectrikRide', 3, 35, '29 pouces', 4, 22.64, 'pneu_energy.png'),
(NULL, 'Pneu Contact','Continental','Urban', 4, 40, '25 pouces', 5, 25.47, 'pneu_contact.png');