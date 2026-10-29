class Produit:
    """Un produit de la carte de la cafétéria."""

    # Attributs de CLASSE : partagés par tous les produits
    HEURE_DEBUT_PLATS = "11:30"     # incluse
    HEURE_FIN_PLATS = "14:00"       # exclue

    def __init__(self, code, nom, categorie, prix, stock):
        self.code = code
        self.nom = nom
        self.categorie = categorie
        self.prix = prix
        self.stock = stock

    def est_disponible(self, quantite, heure):
        """Renvoie (True, "") si le produit peut être servi, sinon (False, motif)."""
        if quantite > self.stock:
            return (False, "rupture de stock")
        if self.categorie == "plat":
            if not (self.HEURE_DEBUT_PLATS <= heure < self.HEURE_FIN_PLATS):
                return (False, "hors créneau")
        return (True, "")

    def vendre(self, quantite):
        """Retire la quantité du stock si possible. Renvoie True si la vente a eu lieu."""
        if quantite > self.stock:
            return False
        self.stock -= quantite
        return True

    def approvisionner(self, quantite):
        """Ajoute la quantité au stock. Renvoie False si la quantité n'est pas positive."""
        if quantite <= 0:
            return False
        self.stock += quantite
        return True

    def __str__(self):
        return f"{self.code} {self.nom:<25} {self.prix:.2f} € (stock : {self.stock})"

    def __repr__(self):
        return f"Produit({self.code!r}, {self.nom!r}, {self.categorie!r}, {self.prix!r}, {self.stock!r})"

    def __eq__(self, autre):
        if not isinstance(autre, Produit):
            return NotImplemented
        return self.code == autre.code

    def __lt__(self, autre):
        return self.prix < autre.prix

class Client:
    """Un client de la cafétéria : nom, profil, solde du badge et fidélité."""

    # Attributs de CLASSE : les règles de l'énoncé, communes à tous les clients
    RECHARGE_MIN = 5.00
    RECHARGE_MAX = 100.00
    SOLDE_MAX = 150.00
    DECOUVERT_PERSONNEL = -10.00
    SEUIL_FIDELITE = 40.00      # variante B3
    TAUX_FIDELITE = 0.05        # variante B3 : -5 %

    def __init__(self, nom, profil, solde=0.0):
        self.nom = nom
        self.profil = profil
        self.solde = solde
        self.total_achats = 0.0     # état de fidélité (B3)

    def a_un_badge(self):
        """Renvoie True si le client a un badge (tous les profils sauf visiteur)."""
        return self.profil != "visiteur"

    def recharger(self, montant):
        """Ajoute le montant au solde. Renvoie False si la recharge n'est pas conforme."""
        if not self.a_un_badge():
            return False
        if montant < self.RECHARGE_MIN or montant > self.RECHARGE_MAX:
            return False
        if round(self.solde + montant, 2) > self.SOLDE_MAX:
            return False
        self.solde = round(self.solde + montant, 2)
        return True

    def peut_payer(self, montant):
        """Renvoie True si le client peut payer ce montant selon son profil."""
        if not self.a_un_badge():
            return True                     # le visiteur paie comptant
        reste = round(self.solde - montant, 2)
        if self.profil == "personnel":
            return reste >= self.DECOUVERT_PERSONNEL
        return reste >= 0

    def debiter(self, montant):
        """Retire le montant du solde si possible. Renvoie True si le paiement a eu lieu."""
        if not self.peut_payer(montant):
            return False
        if self.a_un_badge():
            self.solde = round(self.solde - montant, 2)
        return True

    def avantage_fidelite(self, montant):
        """Renvoie la réduction fidélité (B3) sur ce montant, 0.0 si aucune."""
        if self.a_un_badge() and self.total_achats >= self.SEUIL_FIDELITE:
            return round(montant * self.TAUX_FIDELITE, 2)
        return 0.0

    def enregistrer_achat(self, montant):
        """Ajoute le montant payé au total des achats (fidélité B3)."""
        if self.a_un_badge():
            self.total_achats = round(self.total_achats + montant, 2)

    def __str__(self):
        if not self.a_un_badge():
            return f"{self.nom} (visiteur)"
        return f"{self.nom} ({self.profil}) : solde {self.solde:.2f} €, achats {self.total_achats:.2f} €"

    def __repr__(self):
        return f"Client({self.nom!r}, {self.profil!r}, {self.solde!r})"