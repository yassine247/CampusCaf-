from campuscafe import Produit

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