class Message:

    def __init__(
        self,
        id,
        expediteur,
        destinataire,
        contenu,
        heure,
        lu=False,
        reponse_a=None
    ):
        self.id = id
        self.expediteur = expediteur
        self.destinataire = destinataire
        self.contenu = contenu
        self.heure = heure
        self.lu = lu
        self.reponse_a = reponse_a

    def marquer_comme_lu(self):
        self.lu = True

    def __str__(self):
        statut = "Lu" if self.lu else "Non lu"

        return (
            f"[{self.heure}] "
            f"{self.expediteur} → {self.destinataire} : "
            f"{self.contenu} ({statut})"
        )