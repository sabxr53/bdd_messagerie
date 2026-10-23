import sqlite3
from sqlite3 import Error
from datetime import datetime

def creer_connexion():
    try:
        connexion = sqlite3.connect("messagerie.db")
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