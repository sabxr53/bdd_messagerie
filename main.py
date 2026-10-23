from database import (
    creer_connexion,
    creer_tables,   
    creer_utilisateur,
    recuperer_utilisateur,
    recuperer_tous_les_utilisateurs,
    envoyer_message,
    recuperer_boite_reception,
    recuperer_messages_non_lus,
    marquer_comme_lu,
    temps_reponse_moyen
)

from utilisateur import Utilisateur
from message import Message


def afficher_utilisateurs(connexion):
    utilisateurs = recuperer_tous_les_utilisateurs(connexion)

    print("`\n UTILISATEURS")

    if len(utilisateurs) == 0: 
        print("Aucun utilisateur trouvé")

    else : 

        for utilisateur in utilisateurs:

            print(
                f"{utilisateur[0]} - "
                f"{utilisateur[1]} - "
                f"{utilisateur[2]}"
            )


def creer_compte(connexion) : 
    username = input("Entrez un nom d'utilisateur : ")
    email = input("Entrez un email : ")

    utilisateur = creer_utilisateur(connexion, username, email)

    if utilisateur_id is not None : 
        print(
            f"Compte créé avec succès ! "
            f"votre id est {utilisateur_id}" 
        )


connexion = creer_connexion()

if connexion is not None:
    creer_tables(connexion)

    print("======================================")
    print("         MESSAGERIE ENTREPRISE        ")
    print("======================================")
    print("1. Créer un utilisateur")
    print("2. Se connecter")
    print("3. Envoyer un message")
    print("4. Voir ma boîte de réception")
    print("5. Voir mes messages non lus")
    print("6. Répondre à un message")
    print("7. Rechercher un utilisateur")
    print("8. Statistiques")
    print("9. Quitter")

    connexion.close()

