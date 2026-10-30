# CampusCafé

Caisse de la cafétéria du campus — projet Python, Mastère 1, 2026-2027.
Auteur : Yassine Abdelkefi

## Ma variante

- **Axe A : A1 — Tarif solidaire** : étudiants −10 %, alternants −5 % sur le total ; visiteurs +0,50 € de frais de service.
- **Axe B : B3 — Client fidèle** : dès que le client a cumulé 40,00 € d'achats, il obtient −5 % sur ses commandes suivantes.

## Lancement

Python 3.10 ou plus, bibliothèque standard uniquement.

- Lancer le scénario de la journée : `py campuscafe.py`
- Lancer les tests : `py tests.py`
- Régénérer la sortie : `cmd /c "py -X utf8 campuscafe.py > sortie_scenario.txt"`

## Organisation du code

| Fichier | Contenu |
|---|---|
| `campuscafe.py` | les 4 classes (`Produit`, `Client`, `Commande`, `Cafeteria`), la création de la cafétéria et le scénario |
| `tests.py` | les assertions de test, dont les cas limites |
| `sortie_scenario.txt` | la sortie complète du scénario et du rapport |
| `conception/` | conception papier et calculs à la main (événements 2, 6, 11) |
| `JOURNAL.md` | journal de bord |

## Mes choix

1. **Ordre des calculs** : total → remise A1 → avantage fidélité B3 (calculé sur le montant après remise) → arrondi au centime.
2. **Fidélité B3, « commandes suivantes »** : on regarde le total des achats **avant** d'y ajouter la commande en cours. La commande qui fait franchir les 40 € n'a donc pas encore la réduction.
3. **Total des achats** : on cumule le **montant réellement payé** (après remise et fidélité).
4. **Frais visiteur** : stockés comme une remise négative (−0,50 €). Ils ne sont **pas** comptés dans le « total des remises et avantages » du rapport, car ce ne sont pas des réductions.
5. **Numéros de commande** : une commande reçoit un numéro dès qu'elle est créée, c'est-à-dire après la vérification des codes et des quantités. Une commande refusée ensuite (rupture, hors créneau, solde insuffisant) garde son numéro : les tickets acceptés peuvent sauter des numéros. Un produit inconnu ou une quantité invalide ne consomme pas de numéro.
6. **Ordre des vérifications** : produit inconnu, puis quantité invalide, puis rupture de stock, puis hors créneau, puis solde insuffisant. Un seul motif est compté par refus : le premier rencontré.
7. **Tout ou rien** : les vérifications et les calculs ne modifient rien. Le solde, le stock, la fidélité et le journal ne sont modifiés qu'une fois toutes les vérifications passées.
8. **Arrondis** : tous les montants sont arrondis au centime avec `round(..., 2)`, pour éviter le piège de la comparaison des flottants.
9. **Smoothie mangue** (événement 13) : absent de la carte, il est représenté par le code `SMOOTHIE`, refusé comme « produit inconnu ».
10. **Visiteurs** : un nouvel objet `Client("visiteur", "visiteur")` est créé à chaque commande, puisqu'ils n'ont ni badge ni fidélité.
