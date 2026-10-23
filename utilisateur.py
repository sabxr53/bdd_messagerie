class Utilisateur:

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def __str__(self):
        return f"{self.username} ({self.email})"

        