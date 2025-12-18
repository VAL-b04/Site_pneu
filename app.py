#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect, flash, url_for, g
import pymysql.cursors

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'

# mysql --user=valentin  --password=valentin --host=ASUSVAL.local --database=bdd_projet_pneu
# mysql --user=valentin --password=valentin --host=127.0.0.1 --database=bdd_projet_pneu

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="127.0.0.1",
            user="valentin",
            password="valentin",
            database="bdd_projet_pneu",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


#############################
#   ACCUEIL
#############################

@app.route('/', methods=['GET'])
def show_accueil():
    return render_template('index.html')


#############################
#   CONVERSION
#############################

# Pourquoi ces fonctions sont nécessaires :
# La validation HTML (required, type="number", etc.) peut être contournée par l'utilisateur
# Les champs vides ou invalides doivent être convertis en NULL pour MySQL
# Sans ces conversions, des erreurs SQL se produisent (notamment dans la page "état")
# car MySQL n'accepte pas de chaînes vides dans les colonnes DECIMAL/INT


def to_float(value):
    return float(value) if value and str(value).strip() else None

def to_int(value):
    return int(value) if value and str(value).strip() else None

@app.template_filter('format_price')
def format_price(value):
    return f"{float(value):.2f}" if value is not None else "N/A"


#############################
#   INIT
#############################

@app.route("/init-db")
def init_db():
    db = get_db()
    c = db.cursor()

    c.execute('''DROP TABLE IF EXISTS pneu_velo;''')
    c.execute('''DROP TABLE IF EXISTS type_pneu_velo;''')

    c.execute('''
        CREATE TABLE type_pneu_velo (
            id_type_pneu INT AUTO_INCREMENT PRIMARY KEY,
            libelle_type VARCHAR(50) NOT NULL
        );
    ''')

    c.execute('''
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
    ''')

    c.execute('''
        INSERT INTO type_pneu_velo (id_type_pneu, libelle_type) VALUES
        (NULL, 'Ville'),
        (NULL, 'VTT'),
        (NULL, 'Route'),
        (NULL, 'Vélo électrique'),
        (NULL, 'Fauteuil roulant'),
        (NULL, 'Enfant');
    ''')

    c.execute('''
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
    ''')

    db.commit()

    return redirect("/")


#############################
#   TYPE PNEU
#############################

@app.route('/type-pneu/show', methods=['GET'])
def show_type_pneu():
    mycursor = get_db().cursor()

    sql = '''
    SELECT id_type_pneu AS id,
    libelle_type AS libelleType
    FROM type_pneu_velo ORDER BY id_type_pneu;
    '''
    mycursor.execute(sql)
    types_pneu = mycursor.fetchall()

    return render_template('type_pneu/show_type_pneu.html', types_pneu=types_pneu)


@app.route('/type-pneu/add', methods=['GET'])
def add_type_pneu():
    return render_template('type_pneu/add_type_pneu.html')


@app.route('/type-pneu/add', methods=['POST'])
def valid_add_type_pneu():
    libelle = request.form.get('libelleType')

    mycursor = get_db().cursor()

    sql = '''INSERT INTO type_pneu_velo (libelle_type) VALUES (%s);'''
    mycursor.execute(sql, (libelle,))
    get_db().commit()

    flash(f'Type pneu ajouté : {libelle}', 'alert-success')
    return redirect('/type-pneu/show')


@app.route('/type-pneu/delete', methods=['POST'])
def delete_type_pneu():
    id_type = request.form.get('id')
    mycursor = get_db().cursor()

    sql_check = '''
    SELECT 
        id_pneu_velo AS id,
        nom_pneu AS nomPneu,
        fabricant,
        modele_pneu AS modelePneu,
        prix_pneu AS prixPneu
    FROM pneu_velo
    WHERE type_pneu_id = %s
    '''
    mycursor.execute(sql_check, (id_type,))
    pneus_associes = mycursor.fetchall()

    if pneus_associes:
        sql_type = '''
        SELECT id_type_pneu AS id_type_pneu,
               libelle_type AS libelleType
        FROM type_pneu_velo
        WHERE id_type_pneu = %s
        '''
        mycursor.execute(sql_type, (id_type,))
        type_info = mycursor.fetchone()

        return render_template('type_pneu/delete_cascade.html', type=type_info, pneus=pneus_associes)

    # Si aucun pneu associé, suppression normale
    sql_delete = 'DELETE FROM type_pneu_velo WHERE id_type_pneu = %s'
    mycursor.execute(sql_delete, (id_type,))
    get_db().commit()

    flash(f'Type de pneu supprimé, id : {id_type}', 'alert-warning')
    return redirect('/type-pneu/show')


@app.route('/type-pneu/delete-cascade/<int:id_type>', methods=['POST'])
def delete_type_pneu_cascade(id_type):
    mycursor = get_db().cursor()

    mycursor.execute('SELECT libelle_type FROM type_pneu_velo WHERE id_type_pneu = %s', (id_type,))
    type_info = mycursor.fetchone()
    if not type_info:
        flash("Erreur : type de pneu introuvable.", "alert-danger")
        return redirect('/type-pneu/show')

    libelle_type = type_info['libelle_type']

    mycursor.execute('DELETE FROM pneu_velo WHERE type_pneu_id = %s', (id_type,))

    mycursor.execute('DELETE FROM type_pneu_velo WHERE id_type_pneu = %s', (id_type,))

    get_db().commit()

    flash(f'Type de pneu "{libelle_type}" et tous les pneus associés ont été supprimés.', 'alert-warning')
    return redirect('/type-pneu/show')


@app.route('/type-pneu/edit', methods=['GET'])
def edit_type_pneu():
    id = request.args.get('id')

    mycursor = get_db().cursor()

    sql = '''
    SELECT id_type_pneu AS id,
    libelle_type AS libelleType
    FROM type_pneu_velo
    WHERE id_type_pneu = %s
    '''
    mycursor.execute(sql, (id,))
    type_pneu = mycursor.fetchone()

    return render_template('type_pneu/edit_type_pneu.html', type_pneu=type_pneu)


@app.route('/type-pneu/edit', methods=['POST'])
def valid_edit_type_pneu():
    id_type = request.form.get('id')
    libelle = request.form.get('libelleType')

    mycursor = get_db().cursor()

    sql = '''
    UPDATE type_pneu_velo
    SET libelle_type = %s
    WHERE id_type_pneu = %s
    '''
    mycursor.execute(sql, (libelle, id_type))
    get_db().commit()

    flash(f'Type modifié : {libelle}', 'alert-success')
    return redirect('/type-pneu/show')


#############################
#   PNEU VELO
#############################

@app.route('/pneu-velo/show', methods=['GET'])
def show_pneu_velo():
    mycursor = get_db().cursor()

    sql = '''
    SELECT id_pneu_velo AS id,
    nom_pneu AS nomPneu,
    fabricant, 
    modele_pneu AS modelePneu,
    largeur_pneu AS largeurPneu, 
    diametre_jante AS diametreJante,
    dimension,
    type_pneu_id AS typePneu_id,
    prix_pneu AS prixPneu, 
    image
    FROM pneu_velo
    ORDER BY id_pneu_velo;
    '''
    mycursor.execute(sql)
    pneus = mycursor.fetchall()

    sql_types = '''
    SELECT id_type_pneu AS id,
    libelle_type AS libelleType
    FROM type_pneu_velo
    ORDER BY libelle_type;
    '''
    mycursor.execute(sql_types)
    types_pneu = mycursor.fetchall()

    return render_template('pneu_velo/show_pneu_velo.html', pneus=pneus, types_pneu=types_pneu)


@app.route('/pneu-velo/add', methods=['GET'])
def add_pneu_velo():
    mycursor = get_db().cursor()

    sql = '''
    SELECT id_type_pneu AS id,
    libelle_type AS libelleType
    FROM type_pneu_velo 
    ORDER BY libelle_type;
    '''
    mycursor.execute(sql)
    types_pneu = mycursor.fetchall()

    return render_template('pneu_velo/add_pneu_velo.html', types_pneu=types_pneu)


@app.route('/pneu-velo/add', methods=['POST'])
def valid_add_pneu_velo():
    nom = request.form.get('nomPneu')
    fabricant = request.form.get('fabricant') or None
    modele = request.form.get('modelePneu') or None
    largeur = to_float(request.form.get('largeurPneu'))
    diametre = to_float(request.form.get('diametreJante'))
    dimension = request.form.get('dimension') or None
    type_id = int(request.form.get('typePneu_id'))
    prix = to_float(request.form.get('prixPneu'))
    image = request.form.get('image') or None

    mycursor = get_db().cursor()

    sql = '''
    INSERT INTO pneu_velo (nom_pneu, fabricant, modele_pneu, largeur_pneu, diametre_jante, dimension, type_pneu_id, prix_pneu, image)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    mycursor.execute(sql, (nom, fabricant, modele, largeur, diametre, dimension, type_id, prix, image))
    get_db().commit()

    flash(f'Pneu ajouté : {nom}', 'alert-success')
    return redirect('/pneu-velo/show')


@app.route('/pneu-velo/delete', methods=['POST'])
def delete_pneu_velo():
    id = request.values.get('id')

    mycursor = get_db().cursor()

    sql_get = '''SELECT nom_pneu FROM pneu_velo WHERE id_pneu_velo = %s'''
    mycursor.execute(sql_get, (id,))
    pneu = mycursor.fetchone()
    nom = pneu['nom_pneu']

    sql = '''DELETE FROM pneu_velo WHERE id_pneu_velo = %s'''
    mycursor.execute(sql, (id,))
    get_db().commit()

    flash(f'Pneu supprimé : {nom}, id : {id}', 'alert-warning')
    return redirect('/pneu-velo/show')


@app.route('/pneu-velo/edit', methods=['GET'])
def edit_pneu_velo():
    id = request.args.get('id')

    mycursor = get_db().cursor()

    sql = '''
    SELECT id_pneu_velo AS id,
    nom_pneu AS nomPneu,
    fabricant,
    modele_pneu AS modelePneu,
    largeur_pneu AS largeurPneu,
    diametre_jante AS diametreJante, 
    dimension,
    type_pneu_id AS typePneu_id, 
    prix_pneu AS prixPneu, 
    image
    FROM pneu_velo 
    WHERE id_pneu_velo = %s
    '''
    mycursor.execute(sql, (id,))
    pneu = mycursor.fetchone()

    sql_types = '''
    SELECT id_type_pneu AS id,
    libelle_type AS libelleType
    FROM type_pneu_velo 
    ORDER BY libelle_type;
    '''
    mycursor.execute(sql_types)
    types_pneu = mycursor.fetchall()

    return render_template('pneu_velo/edit_pneu_velo.html', pneu=pneu, types_pneu=types_pneu)


@app.route('/pneu-velo/edit', methods=['POST'])
def valid_edit_pneu_velo():
    id_pneu = request.form.get('id')
    nom = request.form.get('nomPneu')
    fabricant = request.form.get('fabricant') or None
    modele = request.form.get('modelePneu') or None
    largeur = to_float(request.form.get('largeurPneu'))
    diametre = to_float(request.form.get('diametreJante'))
    dimension = request.form.get('dimension') or None
    type_id = int(request.form.get('typePneu_id'))
    prix = to_float(request.form.get('prixPneu'))
    image = request.form.get('image') or None

    mycursor = get_db().cursor()

    sql = '''
    UPDATE pneu_velo 
    SET nom_pneu=%s,
    fabricant=%s,
    modele_pneu=%s,
    largeur_pneu=%s,
    diametre_jante=%s,
    dimension=%s,
    type_pneu_id=%s, 
    prix_pneu=%s,
    image=%s
    WHERE id_pneu_velo=%s
    '''
    mycursor.execute(sql, (nom, fabricant, modele, largeur, diametre, dimension, type_id, prix, image, id_pneu))
    get_db().commit()

    flash(f'Pneu modifié : {nom}', 'alert-success')
    return redirect('/pneu-velo/show')


#############################
#   ETAT
#############################

@app.route('/pneu-velo/etat')
def etat_pneu_velo():
    mycursor = get_db().cursor()

    mycursor.execute('''
    SELECT 
        COUNT(*) AS nombre_total_articles,
        COALESCE(SUM(prix_pneu),0) AS cout_total_stock
    FROM pneu_velo;
    ''')
    totaux = mycursor.fetchone()

    mycursor.execute('''
    SELECT 
        t.id_type_pneu AS type_id,
        t.libelle_type AS type_pneu,
        COUNT(p.id_pneu_velo) AS nombre_articles,
        COALESCE(SUM(p.prix_pneu), 0) AS cout_stock
    FROM type_pneu_velo t
    LEFT JOIN pneu_velo p ON p.type_pneu_id = t.id_type_pneu
    GROUP BY t.id_type_pneu, t.libelle_type
    ORDER BY t.libelle_type;
    ''')
    stats_par_type = mycursor.fetchall()

    mycursor.execute('''
    SELECT 
        t.libelle_type AS type_pneu,
        COALESCE(AVG(p.prix_pneu),0) AS prix_moyen,
        COALESCE(MIN(p.prix_pneu),0) AS prix_min,
        COALESCE(MAX(p.prix_pneu),0) AS prix_max
    FROM type_pneu_velo t
    LEFT JOIN pneu_velo p ON p.type_pneu_id = t.id_type_pneu
    GROUP BY t.id_type_pneu, t.libelle_type
    HAVING COUNT(p.id_pneu_velo) > 0
    ORDER BY prix_moyen DESC;
    ''')
    prix_moyens = mycursor.fetchall()

    return render_template('pneu_velo/etat_pneu_velo.html', totaux=totaux, stats_par_type=stats_par_type, prix_moyens=prix_moyens)


#############################
#   FILTRE
#############################

@app.route('/pneu-velo/filtre', methods=['GET'])
def filtre_pneu_velo():
    filtre_nom = request.args.get('filter_word', '').strip()
    filtre_types = request.args.getlist('filter_items')
    filtre_prix_min = request.args.get('filter_value_min', '').strip()
    filtre_prix_max = request.args.get('filter_value_max', '').strip()

    mycursor = get_db().cursor()

    sql_types = '''
    SELECT id_type_pneu AS id, libelle_type AS libelleType
    FROM type_pneu_velo 
    ORDER BY libelle_type;
    '''
    mycursor.execute(sql_types)
    types_pneu = mycursor.fetchall()

    sql = '''
    SELECT p.id_pneu_velo AS id,
    p.nom_pneu AS nomPneu,
    p.fabricant,
    p.modele_pneu AS modelePneu,
    p.largeur_pneu AS largeurPneu,
    p.diametre_jante AS diametreJante,
    p.dimension,
    p.prix_pneu AS prixPneu,
    p.image,
    t.libelle_type AS typePneu,
    t.id_type_pneu AS typePneu_id
    FROM pneu_velo p
    JOIN type_pneu_velo t ON p.type_pneu_id = t.id_type_pneu
    WHERE 1=1
    '''

    params = []

    if filtre_nom:
        sql += " AND p.nom_pneu LIKE %s"
        params.append(f"%{filtre_nom}%")

    if filtre_types:
        placeholders = ",".join(["%s"] * len(filtre_types))
        sql += f" AND t.id_type_pneu IN ({placeholders})"
        params.extend(filtre_types)

    if filtre_prix_min:
        sql += " AND p.prix_pneu >= %s"
        params.append(to_float(filtre_prix_min) or 0)

    if filtre_prix_max:
        sql += " AND p.prix_pneu <= %s"
        params.append(to_float(filtre_prix_max) or 999999)

    sql += " ORDER BY p.nom_pneu;"

    mycursor.execute(sql, tuple(params))
    pneus = mycursor.fetchall()

    types_noms = ", ".join([t['libelleType'] for t in types_pneu if str(t['id']) in filtre_types]) or "Tous"

    flash(f'Filtres appliqués — nom : {filtre_nom or "Tous"}, types : {types_noms}, min : {filtre_prix_min or "0"}, max : {filtre_prix_max or "∞"}', 'alert-info')

    return render_template('pneu_velo/front_pneu_filtre_show.html', types_pneu=types_pneu, pneus=pneus)


if __name__ == '__main__':
    app.run(debug=True, port=5000)