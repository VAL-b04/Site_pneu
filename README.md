# Gestion des Pneus Vélo - Application Web

Une application web de gestion de stock développée en **Python** avec le micro-framework **Flask** et utilisant une base de données **MySQL** pour le stockage des données.

L'interface permet de gérer les types de pneus, les articles en stock, d'appliquer des filtres de recherche et de consulter des statistiques de stock.

---

## Démonstration en Ligne

Le site est déployé et accessible pour consultation :

[**Accéder au site Gestion des Pneus**](https://valb04.pythonanywhere.com/)

---

## Fonctionnalités

Ce projet implémente un CRUD (Create, Read, Update, Delete) complet et des fonctionnalités d'analyse de données :

* **Gestion des Types de Pneus** (`type_pneu_velo`) : Créer, modifier et supprimer les catégories (Ville, VTT, Route, etc.).
* **Gestion des Pneus** (`pneu_velo`) : Ajouter, modifier et supprimer les articles en stock (nom, fabricant, prix, dimensions, etc.).
* **Filtrage Dynamique** : Rechercher des pneus par nom, type de pneu (multi-sélection), et plage de prix (Min/Max).
* **Statistiques de Stock** : Affichage d'un état complet du stock (nombre total, coût total), ainsi que des statistiques détaillées par catégorie (coût par type, prix moyen/min/max).
* **Initialisation de la Base de Données** : Fonctionnalité `/init-db` pour recréer la structure et insérer les données initiales du catalogue.

---

## Installation et Lancement Local

Pour mettre en place l'environnement de développement local, suivez ces étapes.

### Prérequis

* **Python 3** (version recommandée 3.8+)
* **MySQL** (ou MariaDB)

### 1. Téléchargement et Configuration

1.  **Cloner le dépôt**
    ```bash
    git clone [https://github.com/VAL-b04/Site_Pneu](https://github.com/VAL-b04/Site_Pneu)
    cd Site_Pneu
    ```

2.  **Créer et Activer l'Environnement Virtuel (Recommandé)**
    ```bash
    python -m venv venv
    # Activation (Linux/macOS)
    source venv/bin/activate
    # Activation (Windows - PowerShell)
    # .\venv\Scripts\Activate.ps1
    ```

3.  **Installer les Dépendances Python**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Configuration de la Base de Données

Le projet est configuré pour se connecter à la base de données nommée `projet_pneu`.

**Avertissement de Sécurité :** Le fichier `app.py` contient des identifiants de connexion MySQL (utilisateur, mot de passe) codés en dur. **Vous devez modifier ces informations** (lignes 22-27) pour utiliser vos propres identifiants MySQL locaux.

**Création de la BDD (via terminal MySQL) :**

1.  Connectez-vous à votre console MySQL en utilisant vos propres identifiants :
    ```bash
    mysql --user=VOTRE_USER --password=VOTRE_MDP --host=localhost
    ```
2.  Dans la console MySQL, créez la base de données :
    ```sql
    CREATE DATABASE projet_pneu;
    ```

### 3. Lancement de l'Application

1.  **Lancer le Serveur Flask**
    ```bash
    flask --debug  --app app  run   --host 0.0.0.0
    ```
    L'application sera accessible à l'adresse par défaut : `http://127.0.0.1:5000/`.

2.  **Initialiser les Tables et les Données**
    Une fois le serveur lancé, ouvrez votre navigateur et accédez à cette route pour créer la structure et insérer les données initiales de démonstration :
    
    `http://127.0.0.1:5000/init-db`
