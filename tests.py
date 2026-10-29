from campuscafe import Produit, Client, Commande

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