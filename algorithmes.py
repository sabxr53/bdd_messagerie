def recherche_dichotomique(liste, valeur):

    gauche = 0
    droite = len(liste) - 1

    while gauche <= droite:

        milieu = (gauche + droite) // 2

        if liste[milieu] == valeur:
            return milieu

        elif liste[milieu] < valeur:
            gauche = milieu + 1

        else:
            droite = milieu - 1

    return -1

def recherche_lineaire(liste, valeur):

    for i in range(len(liste)):

        if liste[i] == valeur:
            return i

    return -1

#fonction de hachage 

def fonction_hachage(username, taille_table):

    valeur = 0

    for caractere in username:

        valeur += ord(caractere)

    return valeur % taille_table