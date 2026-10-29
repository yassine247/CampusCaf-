from campuscafe import Produit, Client, Commande, Cafeteria

cafe = Produit("B01", "Café expresso", "boisson chaude", 1.20, 100)
plat = Produit("P03", "Plat du jour", "plat", 7.20, 20)

# Créneau des plats : bornes exactes
assert plat.est_disponible(1, "11:30") == (True, "")              # 11:30 incluse
assert plat.est_disponible(1, "14:00") == (False, "hors créneau") # 14:00 exclue
assert plat.est_disponible(1, "11:29") == (False, "hors créneau")
assert cafe.est_disponible(1, "07:30") == (True, "")              # pas un plat : pas de créneau

# Stock : exactement suffisant puis insuffisant
assert plat.est_disponible(20, "12:00") == (True, "")
assert plat.est_disponible(21, "12:00") == (False, "rupture de stock")

# Vendre et approvisionner
assert plat.vendre(5) is True and plat.stock == 15
assert plat.vendre(100) is False and plat.stock == 15   # rien ne bouge
assert plat.approvisionner(10) is True and plat.stock == 25
assert plat.approvisionner(0) is False

# Égalité par code, ordre par prix
assert cafe == Produit("B01", "Autre nom", "boisson chaude", 9.99, 0)
assert cafe != plat
assert cafe < plat
assert sorted([plat, cafe]) == [cafe, plat]

print("Tests Produit : OK ✅")


# ---------- Tests Client ----------
alice = Client("Alice", "étudiant", 12.00)
farid = Client("Farid", "personnel", 0.00)
bruno = Client("Bruno", "alternant", 3.50)
visiteur = Client("visiteur", "visiteur")

# Badge
assert alice.a_un_badge() and not visiteur.a_un_badge()

# Recharge : limites de montant et plafond
assert bruno.recharger(20) is True and bruno.solde == 23.50
assert bruno.recharger(100) is True and bruno.solde == 123.50   # recharge de 100 € : acceptée
assert bruno.recharger(30) is False and bruno.solde == 123.50   # dépasserait 150 €
assert alice.recharger(4.99) is False                           # moins de 5 €
assert alice.recharger(150) is False and alice.solde == 12.00   # plus de 100 € (événement 10)
assert visiteur.recharger(10) is False                          # pas de badge
assert Client("Test", "étudiant", 50.00).recharger(100) is True # arrive pile à 150 € : accepté

# Paiement : solde exactement suffisant
assert alice.peut_payer(12.00) is True
assert alice.peut_payer(12.01) is False

# Paiement : découvert du personnel à -10 €
assert farid.peut_payer(10.00) is True
assert farid.peut_payer(10.01) is False
assert visiteur.peut_payer(1000) is True                         # paie comptant

# Débit
assert alice.debiter(2.40) is True and alice.solde == 9.60
assert alice.debiter(50) is False and alice.solde == 9.60        # refusé : rien ne bouge

# Fidélité B3 : réduction seulement APRÈS avoir atteint 40 €
chloe = Client("Chloé", "étudiant", 100.00)
assert chloe.avantage_fidelite(10.00) == 0.0
chloe.enregistrer_achat(39.99)
assert chloe.avantage_fidelite(10.00) == 0.0                     # 39,99 : pas encore
chloe.enregistrer_achat(0.01)
assert chloe.total_achats == 40.00
assert chloe.avantage_fidelite(10.00) == 0.50                    # 40,00 pile : -5 %
assert visiteur.avantage_fidelite(10.00) == 0.0                  # pas de fidélité sans badge

print("Tests Client : OK ✅")


# ---------- Tests Commande ----------
expresso = Produit("B01", "Café expresso", "boisson chaude", 1.20, 100)
croissant = Produit("V01", "Croissant", "viennoiserie", 1.20, 30)
the = Produit("B02", "Thé", "boisson chaude", 1.30, 60)
client = Client("Alice", "étudiant", 12.00)

c = Commande(client, "07:45")
c.ajouter_ligne(expresso, 1)
c.ajouter_ligne(croissant, 3)
assert len(c) == 4                                 # 1 + 3 articles
assert c.total() == 4.80                           # 1.20 + 3 x 1.20
assert expresso in c and croissant in c            # __contains__
assert the not in c
assert Produit("B01", "Autre nom", "boisson chaude", 9.99, 0) in c   # égalité par code

# Même produit ajouté deux fois : la quantité se cumule
c.ajouter_ligne(expresso, 2)
assert len(c) == 6 and len(c.lignes) == 2
assert c.total() == 7.20

# __iter__ : for ... in commande
quantites = []
for produit, quantite in c:
    quantites.append(quantite)
assert quantites == [3, 3]

# Numéro automatique
c2 = Commande(client, "08:00")
assert c2.numero == c.numero + 1

# Copie de la liste reçue
mes_lignes = [(expresso, 1)]
c3 = Commande(client, "09:00", mes_lignes)
mes_lignes.append((the, 5))                        # on modifie la liste APRÈS
assert len(c3) == 1                                # la commande n'a pas bougé

print(c)                                           # pour voir le ticket
print("Tests Commande : OK ✅")


# ---------- Tests Cafeteria ----------
cafet = Cafeteria()
cafet.ajouter_produit(Produit("B01", "Café expresso", "boisson chaude", 1.20, 100))
cafet.ajouter_produit(Produit("B03", "Chocolat chaud", "boisson chaude", 1.60, 40))
cafet.ajouter_produit(Produit("B05", "Eau 50 cl", "boisson froide", 1.00, 40))
cafet.ajouter_produit(Produit("V01", "Croissant", "viennoiserie", 1.20, 30))
cafet.ajouter_produit(Produit("P02", "Wrap végétarien", "plat", 4.60, 10))
cafet.ajouter_produit(Produit("P03", "Plat du jour", "plat", 7.20, 20))
cafet.ajouter_produit(Produit("D02", "Fruit de saison", "dessert", 0.80, 30))

alice = Client("Alice", "étudiant", 12.00)
bruno = Client("Bruno", "alternant", 3.50)
chloe = Client("Chloé", "étudiant", 25.00)
visiteur = Client("visiteur", "visiteur")

# Événement 2 (calcul à la main : 2,16 €, solde 9,84 €)
assert cafet.traiter_commande(alice, "07:45", [("B01", 1), ("V01", 1)]) == (True, "", 2.16)
assert alice.solde == 9.84 and alice.total_achats == 2.16
assert cafet.carte["V01"].stock == 29

# Événement 4 : solde insuffisant -> tout ou rien
assert cafet.traiter_commande(bruno, "08:30", [("B03", 1), ("V01", 3)]) == (False, "solde insuffisant", 0.0)
assert bruno.solde == 3.50                       # solde inchangé
assert cafet.carte["V01"].stock == 29            # stock inchangé
assert len(cafet.journal) == 1                   # journal inchangé

# Événements 5 et 6 (calcul à la main : 4,94 €, solde 18,56 €)
assert cafet.recharger(bruno, 20) is True and bruno.solde == 23.50
assert cafet.traiter_commande(bruno, "08:40", [("B03", 1), ("V01", 3)]) == (True, "", 4.94)
assert bruno.solde == 18.56 and cafet.carte["V01"].stock == 26

# Événement 8 : plat du jour à 11:00 -> hors créneau
assert cafet.traiter_commande(chloe, "11:00", [("P03", 1)]) == (False, "hors créneau", 0.0)

# Événement 10 : recharge de 150 € refusée
assert cafet.recharger(alice, 150) is False and alice.solde == 9.84

# Événement 11 (calcul à la main : 6,84 €, solde 3,00 €)
assert cafet.traiter_commande(alice, "12:20", [("P02", 1), ("B05", 1), ("D02", 1), ("B01", 1)]) == (True, "", 6.84)
assert alice.solde == 3.00 and alice.total_achats == 9.00

# Produit inconnu (événement 13 : Smoothie mangue) et quantité invalide
assert cafet.traiter_commande(bruno, "13:00", [("P01", 1), ("SM01", 1)])[1] == "produit inconnu"
assert cafet.traiter_commande(bruno, "13:00", [("B01", 0)])[1] == "quantité invalide"

# Visiteur : +0,50 € de frais (A1)
assert cafet.traiter_commande(visiteur, "09:15", [("B01", 1)]) == (True, "", 1.70)

# Comptage des refus
assert cafet.refus["solde insuffisant"] == 1
assert cafet.refus["hors créneau"] == 1
assert cafet.refus["produit inconnu"] == 1
assert cafet.refus["quantité invalide"] == 1
assert len(cafet.journal) == 4

print(cafet.journal[-1])          # le ticket du visiteur
print("Tests Cafeteria : OK ✅")