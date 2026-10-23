import sqlite3
from sqlite3 import Error
from datetime import datetime

def creer_connexion():
    try:
        connexion = sqlite3.connect("messagerie.db")

        #activer la vérification des clés étrangères
        connexion.execute("PRAGMA foreign_keys = ON")


        print("Connexion réussie à SQLite")
        return connexion

    except Error as e:
        print(f"Erreur lors de la connexion : {e}")
        return None


def creer_tables(connexion) : 

    connexion.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
    )
""")

    connexion.execute("""
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expediteur INTEGER NOT NULL,
            destinataire INTEGER NOT NULL,
            contenu TEXT NOT NULL,
            horodatage TEXT NOT NULL,
            lu INTEGER DEFAULT 0,
            reponse_a INTEGER,

            FOREIGN KEY (expediteur)
                REFERENCES utilisateur(id),

            FOREIGN KEY (destinataire)
                REFERENCES utilisateur(id),

            FOREIGN KEY (reponse_a)
                REFERENCES message(id)
        )
    """)

    connexion.commit()


#UTILISATEURS

def creer_utilisateur(connexion, username, email) : 

    sql = """
        INSERT INTO utilisateur (username, email)
        VALUES (?, ?)
    """

    try : 
        curseur = connexion.execute(sql, (username, email))

        connexion.commit()

        return curseur.lastrowid

    except sqlite3.IntegrityError:
        print("Erreur : cet email est déjà utilisé")
        return None

def recuperer_utilisateur(connexion, utilisateur_id) : 
    
    sql = """
        SELECT id, username, email
        FROM utilisateur
        Where id = ? 
    """

    return connexion.execute(sql, (utilisateur_id,)).fetchone()

def recuperer_tous_les_utilisateurs(connexion) : 

    sql = """
        SELECT id, username, email
        FROM utilisateur    
        ORDER BY id 
    """

    return connexion.execute(sql).fetchall()

#messages

def envoyer_message(
    connexion,
    expediteur,
    destinataire,
    contenu,
    reponse_a=None
):

    # Récupération automatique de l'heure actuelle
    heure = datetime.now().isoformat(
        timespec="seconds"
    )

    sql = """
        INSERT INTO message
        (expediteur, destinataire, contenu, horodatage, reponse_a)
        VALUES (?, ?, ?, ?, ?)
    """

    try:

        curseur = connexion.execute(
            sql,
            (
                expediteur,
                destinataire,
                contenu,
                heure,
                reponse_a
            )
        )

        connexion.commit()

        return curseur.lastrowid

    except sqlite3.IntegrityError:
        print("Erreur : utilisateur inexistant.")
        return None


def recuperer_boite_reception(
    connexion,
    utilisateur_id
):

    sql = """
        SELECT
            id,
            expediteur,
            destinataire,
            contenu,
            horodatage,
            lu,
            reponse_a
        FROM message
        WHERE destinataire = ?
        ORDER BY horodatage DESC
    """

    return connexion.execute(
        sql,
        (utilisateur_id,)
    ).fetchall()


def recuperer_messages_non_lus(
    connexion,
    utilisateur_id
):

    sql = """
        SELECT
            id,
            expediteur,
            contenu,
            horodatage
        FROM message
        WHERE destinataire = ?
        AND lu = 0
        ORDER BY horodatage DESC
    """

    return connexion.execute(
        sql,
        (utilisateur_id,)
    ).fetchall()


def marquer_comme_lu(
    connexion,
    message_id
):

    sql = """
        UPDATE message
        SET lu = 1
        WHERE id = ?
    """

    connexion.execute(
        sql,
        (message_id,)
    )

    connexion.commit()


#temps de reponse 

def calculer_temps_reponse(
    connexion,
    message_id,
    reponse_id
):

    sql = """
        SELECT horodatage
        FROM message
        WHERE id = ?
    """

    message = connexion.execute(
        sql,
        (message_id,)
    ).fetchone()

    reponse = connexion.execute(
        sql,
        (reponse_id,)
    ).fetchone()

    if message is None or reponse is None:
        return None

    date_message = datetime.fromisoformat(
        message[0]
    )

    date_reponse = datetime.fromisoformat(
        reponse[0]
    )

    return (
        date_reponse - date_message
    ).total_seconds()


def temps_reponse_moyen(
    connexion,
    utilisateur_id
):

    sql = """
        SELECT
            m.horodatage,
            r.horodatage
        FROM message AS m
        JOIN message AS r
            ON r.reponse_a = m.id
        WHERE m.destinataire = ?
    """

    resultats = connexion.execute(
        sql,
        (utilisateur_id,)
    ).fetchall()

    if len(resultats) == 0:
        return None

    total = 0

    for message, reponse in resultats:

        date_message = datetime.fromisoformat(message)
        date_reponse = datetime.fromisoformat(reponse)

        total += (
            date_reponse - date_message
        ).total_seconds()

    return total / len(resultats)