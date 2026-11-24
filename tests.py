from campuscafe import Produit, Client, Commande, Cafeteria, creer_cafeteria

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


# ---------- Tests du rapport ----------
cafet.ajouter_client(alice)
cafet.ajouter_client(bruno)

assert cafet.nb_acceptees() == 4
assert cafet.chiffre_affaires() == 15.64          # 2.16 + 4.94 + 6.84 + 1.70
assert cafet.total_remises() == 1.26              # 0.24 + 0.26 + 0.76 (les frais visiteur ne comptent pas)

top = cafet.plus_vendus(3)
assert top[0][0].code == "V01" and top[0][1] == 4   # croissant : 1 + 3
assert top[1][0].code == "B01" and top[1][1] == 3   # café : 1 + 1 + 1
assert len(top) == 3

triee = cafet.carte_triee()
assert triee[0].code == "D02"                       # fruit, 0.80 € : le moins cher
assert triee[-1].code == "P03"                      # plat du jour, 7.20 € : le plus cher
assert max(cafet.carte.values()).code == "P03"

assert alice.solde == 3.00
assert cafet.badges_faibles() == []                 # 3.00 pile : PAS inférieur à 3.00

print("Tests rapport : OK ✅")
# ---------- Tests évolution : annulation (phase 1) ----------
cafet2 = creer_cafeteria()
alice2 = cafet2.clients["Alice"]

# 1. Annuler la dernière commande : retour exact à l'état d'avant (instantané)
avant = (alice2.solde, alice2.total_achats, cafet2.carte["B01"].stock, cafet2.carte["V01"].stock)
cafet2.traiter_commande(alice2, "07:45", [("B01", 1), ("V01", 1)])
numero = cafet2.journal[-1].numero
assert cafet2.annuler_commande(numero) == (True, "", 2.16)
apres = (alice2.solde, alice2.total_achats, cafet2.carte["B01"].stock, cafet2.carte["V01"].stock)
assert apres == avant

# 2. Commande inconnue
assert cafet2.annuler_commande(999) == (False, "commande inconnue", 0.0)

# 3. Commande déjà annulée
assert cafet2.annuler_commande(numero) == (False, "commande déjà annulée", 0.0)

# 4. Annulation refusée : rien n'est modifié
assert alice2.solde == 12.00 and cafet2.carte["B01"].stock == 100
assert len(cafet2.journal) == 1                    # la commande annulée reste dans le journal

# 5. Remboursement d'un visiteur (comptant : pas de solde)
visiteur2 = Client("visiteur", "visiteur")
cafet2.traiter_commande(visiteur2, "09:15", [("B02", 1)])
assert cafet2.annuler_commande(cafet2.journal[-1].numero) == (True, "", 1.80)
assert visiteur2.solde == 0.0

# 6. Remboursement qui fait dépasser 150 € : autorisé
riche = Client("Riche", "personnel", 145.00)
cafet2.traiter_commande(riche, "08:00", [("B01", 1)])          # solde 143.80
assert riche.recharger(6.20) is True and riche.solde == 150.00
assert cafet2.annuler_commande(cafet2.journal[-1].numero)[0] is True
assert riche.solde == 151.20

# 7. Annulation d'une commande qui avait utilisé un avantage de fidélité
dina = Client("Dina", "étudiant", 100.00)
cafet2.traiter_commande(dina, "12:00", [("P03", 7)])           # 50.40 - 5.04 = 45.36
num_gros = cafet2.journal[-1].numero
cafet2.traiter_commande(dina, "12:10", [("B01", 1)])           # 1.08 - 0.05 (fidélité) = 1.03
num_cafe = cafet2.journal[-1].numero
assert cafet2.journal[-1].avantage == 0.05
assert dina.total_achats == 46.39
assert cafet2.annuler_commande(num_cafe) == (True, "", 1.03)
assert dina.total_achats == 45.36 and dina.solde == 54.64

# 7 bis. Un avantage déjà obtenu reste acquis
cafet2.traiter_commande(dina, "12:20", [("B01", 1)])           # encore 1.03 (fidélité)
cafet2.annuler_commande(num_gros)
assert dina.total_achats == 1.03                    # il ne reste que ce café
assert cafet2.journal[-1].montant_paye == 1.03      # son montant n'est pas recalculé

# 8. Ticket d'une commande annulée
assert "ANNULÉE" in str(cafet2.trouver_commande(num_cafe))

print("Tests annulation : OK ✅")
# ---------- Tests évolution : rappel (phase 2) ----------
cafet3 = creer_cafeteria()
alice3 = cafet3.clients["Alice"]
bruno3 = cafet3.clients["Bruno"]
chloe3 = cafet3.clients["Chloé"]
bruno3.recharger(20.00)                                              # 23.50

cafet3.traiter_commande(bruno3, "12:15", [("P02", 2)])               # 8.74
cafet3.traiter_commande(chloe3, "12:18", [("P02", 1)])               # 4.14
cafet3.traiter_commande(alice3, "12:20", [("P02", 1), ("B05", 1), ("D02", 1), ("B01", 1)])   # 6.84
cafet3.traiter_commande(chloe3, "12:22", [("B01", 1)])               # 1.08, sans Wrap

# 1. Rappel d'un produit présent dans plusieurs commandes
rappele, motif, resume = cafet3.rappeler_produit("P02")
assert rappele is True
assert len(resume["commandes"]) == 3
assert resume["commandes"] == sorted(resume["commandes"])          # ordre chronologique
assert resume["total"] == 19.72                                     # 8.74 + 4.14 + 6.84
assert cafet3.carte["P02"].stock == 0                               # le Wrap ne revient pas
assert cafet3.carte["B05"].stock == 40                              # l'eau d'Alice revient
assert bruno3.solde == 23.50 and alice3.solde == 12.00
assert chloe3.solde == 23.92 and chloe3.total_achats == 1.08        # son café reste payé

# 2. Rappel d'un produit sans aucune commande
assert cafet3.rappeler_produit("D01") == (True, "", {"produit": "Cookie", "commandes": [],
                                                     "remboursements": [], "total": 0.0})

# 3. Commande contenant un produit rappelé : refusée, rien modifié
avant = (alice3.solde, cafet3.carte["B01"].stock, len(cafet3.journal))
assert cafet3.traiter_commande(alice3, "12:35", [("B01", 1), ("P02", 1)]) == (False, "produit rappelé", 0.0)
assert (alice3.solde, cafet3.carte["B01"].stock, len(cafet3.journal)) == avant

# 4. Réapprovisionnement d'un produit rappelé : refusé
assert cafet3.reapprovisionner("P02", 10) is False and cafet3.carte["P02"].stock == 0

# 5. Second rappel du même produit
assert cafet3.rappeler_produit("P02") == (False, "déjà rappelé", None)

# 6. Code inconnu : refusé, rien modifié
assert cafet3.rappeler_produit("XYZ") == (False, "produit inconnu", None)

# Comptage des nouveaux refus
assert cafet3.refus["produit rappelé"] == 2                         # commande + réappro
assert cafet3.refus["déjà rappelé"] == 1

print("Tests rappel : OK ✅")

# ---------- Tests évolution : rapport de crise (phase 3) ----------
assert cafet3.nb_acceptees() == 1                   # seul le café de Chloé reste valide
assert cafet3.nb_annulees() == 3
assert cafet3.nb_annulees_rappel() == 3
assert cafet3.total_rembourse() == 19.72
assert cafet3.chiffre_affaires() == 1.08
assert cafet3.total_remises() == 0.12               # remise étudiante du café de Chloé
assert cafet3.plus_vendus(3)[0][0].code == "B01" and len(cafet3.plus_vendus(3)) == 1

print("Tests rapport de crise : OK ✅")