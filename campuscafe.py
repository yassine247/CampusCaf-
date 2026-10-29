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