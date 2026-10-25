from database import (
    creer_connexion,
    creer_tables,   
    creer_utilisateur,
    recuperer_utilisateur,
    recuperer_tous_les_utilisateurs,
    envoyer_message as envoyer_message_db,
    recuperer_boite_reception,
    recuperer_messages_non_lus,
    marquer_comme_lu,
    temps_reponse_moyen
)

from utilisateur import Utilisateur
from message import Message


def afficher_utilisateurs(connexion):
    utilisateurs = recuperer_tous_les_utilisateurs(connexion)

    print("\n UTILISATEURS")

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
    username = input("Entrez un nom d'utilisateur : ").strip()
    email = input("Entrez un email : ").strip()

    if not username or not email:
        print("Le nom d'utilisateur et l'email ne peuvent pas être vides.")
        return None

    utilisateur = creer_utilisateur(connexion, username, email)

    if utilisateur is not None : 
        print(
            f"Compte créé avec succès ! "
            f"votre id est {utilisateur}" 
        )

def envoyer_message(connexion, utilisateur_id):
    choix_reponse = input(
        "ID du message auquel répondre (Entrée pour un nouveau message) : "
    ).strip()

    reponse_a = None

    if choix_reponse:
        try:
            reponse_a = int(choix_reponse)
        except ValueError:
            print("ID invalide.")
            return

        message_original = recuperer_expediteur_message(
            connexion, reponse_a, utilisateur_id
        )

        if message_original is None:
            print("Message introuvable dans votre boîte de réception.")
            return

        destinataire_id = message_original[0]
    else:
        afficher_utilisateurs(connexion)

        try:
            destinataire_id = int(input("ID du destinataire : "))
        except ValueError:
            print("ID invalide, l'id doit être un nombre.")
            return

    contenu = input("Entrez le message : ").strip()

    if not contenu:
        print("Le message ne peut pas être vide.")
        return

    message_id = envoyer_message_db(
        connexion,
        utilisateur_id,
        destinataire_id,
        contenu,
        reponse_a
    )

    if message_id is not None:
        print(f"Message envoyé avec succès ! ID : {message_id}")



def afficher_boite_reception(connexion, utilisateur_id) : 
    
    messages = recuperer_boite_reception(connexion, utilisateur_id)

    print("\n BOÎTE DE RÉCEPTION")

    if len(messages) == 0 :
        print("Aucun message trouvé")
        return 

    for message in messages : 
        id_message = message[0]
        expediteur = message[1]
        contenu = message[3]
        horodatage = message[4]
        lu = message[5]

        statut = "Lu" if lu else "Non lu"

        print(
            f"ID : {id_message} | "
            f"Expéditeur : {expediteur} | "
            f"Contenu : {contenu} | "
            f"Horodatage : {horodatage} | "
            f"Statut : {statut}"
        )


def afficher_messages_non_lus(connexion, utilisateur_id) : 
    
    messages = recuperer_messages_non_lus(connexion, utilisateur_id)

    print("\n MESSAGES NON LUS")

    if len(messages) == 0 :
        print("Aucun message non lu trouvé")
        return 

    for message in messages : 
        print(
            f"ID : {message[0]} | "
            f"Expéditeur : {message[1]} | "
            f"Contenu : {message[2]} | "
            f"Horodatage : {message[3]}"
        )

def lire_message(connexion, utilisateur_id) :

    try:

        message_id = int(
            input("ID du message : ")
        )

    except ValueError:

        print("ID invalide.")
        return

    if marquer_comme_lu(connexion, message_id, utilisateur_id):
        print("Message marqué comme lu.")
    else:
        print("Message introuvable dans votre boîte de réception.")


def menu(connexion, utilisateur_id) : 
    while True : 
        print("\n")
        print("MESSAGERIE ENTREPRISE")
        print("1. voir les utilisateurs")
        print("2. envoyer un message")
        print("3. voir ma boîte de réception")
        print("4. voir mes messages non lus")
        print("5.marquer un message comme lu")
        print("6. temps de réponse moyen")
        print("7. quitter")

        choix = input("Choisissez une option : ")

        if choix == "1": 
            afficher_utilisateurs(connexion)

        elif choix == "2" : 
            envoyer_message(connexion, utilisateur_id)  
        
        elif choix == "3" :
            afficher_boite_reception(connexion, utilisateur_id)

        elif choix == "4" :
            afficher_messages_non_lus(connexion, utilisateur_id)

        elif choix == "5" :
            lire_message(connexion, utilisateur_id)

        elif choix == "6" :
            moyenne = temps_reponse_moyen(connexion, utilisateur_id)
            if moyenne is None:
                print(f"Aucune réponses")
            else : 
                print(f"Temps de réponse moyen : {moyenne:.2f} secondes")

        elif choix == "7" :
            print("Déconnexion...")
            break

        else : 
            print("Choix invalide, réessayez.")



connexion = creer_connexion()

if connexion is not None:
    creer_tables(connexion)

    print("======================================")
    print("         MESSAGERIE ENTREPRISE        ")
    print("======================================")
    print("1. Créer un compte")
    print("2. Se connecter")

    choix = input("Choisissez une option : ")
    if choix == "1":
        creer_compte(connexion)

    elif choix == "2":
        afficher_utilisateurs(connexion)

        try :
            utilisateur_id = int(input("Entrez votre ID : "))

        except ValueError : 
            print("ID invalide, l'id doit être un nombre")
            connexion.close()
            exit()

        utilisateur = recuperer_utilisateur(connexion, utilisateur_id)

        if utilisateur is None :
            print("Utilisateur non trouvé")
        else : 
            print(f"Bienvenue {utilisateur[1]} !")
            menu(connexion, utilisateur_id)


    connexion.close()

