from database import creer_connexion, creer_tables


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

