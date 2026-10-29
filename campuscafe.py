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



class Commande:
    """Une commande : un client, une heure et des lignes [produit, quantite]."""

    compteur = 0        # attribut de CLASSE : sert à numéroter les commandes

    def __init__(self, client, heure, lignes=None):
        Commande.compteur += 1              # on écrit sur la CLASSE
        self.numero = Commande.compteur
        self.client = client
        self.heure = heure
        self.lignes = []
        if lignes is not None:
            for produit, quantite in lignes:    # on COPIE les lignes reçues
                self.ajouter_ligne(produit, quantite)
        # Remplis par la Cafeteria au moment du traitement
        self.remise = 0.0
        self.avantage = 0.0
        self.montant_paye = 0.0

    def ajouter_ligne(self, produit, quantite):
        """Ajoute une ligne ; si le produit est déjà présent, cumule la quantité."""
        for ligne in self.lignes:
            if ligne[0] == produit:             # utilise Produit.__eq__ (même code)
                ligne[1] += quantite
                return
        self.lignes.append([produit, quantite])

    def total(self):
        """Renvoie le total TTC avant remise, arrondi au centime."""
        somme = 0
        for produit, quantite in self.lignes:
            somme += produit.prix * quantite
        return round(somme, 2)

    def __len__(self):
        """len(commande) : nombre total d'articles."""
        nombre = 0
        for produit, quantite in self.lignes:
            nombre += quantite
        return nombre

    def __contains__(self, produit):
        """produit in commande : le produit est-il dans une des lignes ?"""
        for ligne in self.lignes:
            if ligne[0] == produit:
                return True
        return False

    def __iter__(self):
        """for ligne in commande : parcourt les lignes [produit, quantite]."""
        return iter(self.lignes)

    def __str__(self):
        texte = f"=== Ticket n°{self.numero} — {self.client.nom} — {self.heure} ===\n"
        for produit, quantite in self.lignes:
            texte += f"  {produit.nom:<25} x{quantite:<3} {produit.prix * quantite:6.2f} €\n"
        texte += f"  {'Total':<30} {self.total():6.2f} €\n"
        if self.remise > 0:
            texte += f"  {'Remise':<30} {-self.remise:6.2f} €\n"
        if self.remise < 0:
            texte += f"  {'Frais de service':<30} {-self.remise:6.2f} €\n"
        if self.avantage > 0:
            texte += f"  {'Fidélité':<30} {-self.avantage:6.2f} €\n"
        texte += f"  {'Payé':<30} {self.montant_paye:6.2f} €"
        return texte

    def __repr__(self):
        return f"Commande(n°{self.numero}, {self.client.nom!r}, {self.heure!r}, {len(self)} articles)"    


class Cafeteria:
    """La cafétéria : la carte, les clients, le journal et les refus."""

    # Attributs de CLASSE : variante A1 (tarif solidaire)
    REMISE_ETUDIANT = 0.10
    REMISE_ALTERNANT = 0.05
    FRAIS_VISITEUR = 0.50

    def __init__(self):
        self.carte = {}         # {code: Produit}
        self.clients = {}       # {nom: Client}
        self.journal = []       # commandes acceptées
        self.refus = {
            "produit inconnu": 0,
            "quantité invalide": 0,
            "rupture de stock": 0,
            "hors créneau": 0,
            "solde insuffisant": 0,
        }

    def ajouter_produit(self, produit):
        self.carte[produit.code] = produit

    def ajouter_client(self, client):
        self.clients[client.nom] = client

    def calculer_remise(self, client, total):
        """Variante A1. Renvoie la remise (négative pour les frais visiteur)."""
        if client.profil == "étudiant":
            return round(total * self.REMISE_ETUDIANT, 2)
        if client.profil == "alternant":
            return round(total * self.REMISE_ALTERNANT, 2)
        if client.profil == "visiteur":
            return -self.FRAIS_VISITEUR
        return 0.0

    def refuser(self, motif):
        """Compte un refus et renvoie le triplet (acceptée, motif, montant)."""
        self.refus[motif] += 1
        return (False, motif, 0.0)

    def traiter_commande(self, client, heure, demandes):
        """Traite une commande en tout ou rien. Renvoie (acceptée, motif, montant)."""
        # 1. Vérifier les codes et les quantités
        for code, quantite in demandes:
            if code not in self.carte:
                return self.refuser("produit inconnu")
            if quantite <= 0:
                return self.refuser("quantité invalide")

        commande = Commande(client, heure)
        for code, quantite in demandes:
            commande.ajouter_ligne(self.carte[code], quantite)

        # 1. (suite) Vérifier la disponibilité de chaque produit
        for produit, quantite in commande:
            disponible, motif = produit.est_disponible(quantite, heure)
            if not disponible:
                return self.refuser(motif)

        # 2. Calculer : total -> remise A1 -> fidélité B3
        total = commande.total()
        remise = self.calculer_remise(client, total)
        apres_remise = round(total - remise, 2)
        avantage = client.avantage_fidelite(apres_remise)
        montant = round(apres_remise - avantage, 2)

        # 3. Encaisser : vérifier que le client peut payer
        if not client.peut_payer(montant):
            return self.refuser("solde insuffisant")

        # 4. Enregistrer : à partir d'ici, on MODIFIE
        client.debiter(montant)
        for produit, quantite in commande:
            produit.vendre(quantite)
        client.enregistrer_achat(montant)
        commande.remise = remise
        commande.avantage = avantage
        commande.montant_paye = montant
        self.journal.append(commande)
        return (True, "", montant)

    def recharger(self, client, montant):
        """Recharge le badge d'un client. Renvoie True si la recharge est acceptée."""
        return client.recharger(montant)

    def reapprovisionner(self, code, quantite):
        """Ajoute du stock à un produit. Renvoie False si le code est inconnu."""
        if code not in self.carte:
            return False
        return self.carte[code].approvisionner(quantite)

    def __repr__(self):
        return f"Cafeteria({len(self.carte)} produits, {len(self.clients)} clients, {len(self.journal)} commandes)"    