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
- Lancer le menu interactif (bonus) : `py menu.py`

## Organisation du code

| Fichier | Contenu |
|---|---|
| `campuscafe.py` | les 4 classes (`Produit`, `Client`, `Commande`, `Cafeteria`), la création de la cafétéria et le scénario |
| `tests.py` | les assertions de test, dont les cas limites |
| `sortie_scenario.txt` | la sortie complète du scénario et du rapport |
| `conception/` | conception papier et calculs à la main (événements 2, 6, 11) |
| `JOURNAL.md` | journal de bord |
| `menu.py` | bonus : menu console pour saisir commandes, recharges et réapprovisionnements à la main |
| `scenario_v2.py` | lance le scénario v2 (évolution « Rappel de lot ») |
| `sortie_scenario_v2.txt` | la sortie du scénario v2 et du rapport de crise |
| `conception/evolution/` | calculs à la main des événements 12:18, 12:25 et 12:30 |

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

## Évolution v2.0 — « Rappel de lot »

### Lancement
- Scénario v1 (inchangé) : `py campuscafe.py`
- Scénario v2 (annulations et rappel) : `py scenario_v2.py`
- Régénérer la sortie v2 : `cmd /c "py -X utf8 scenario_v2.py > sortie_scenario_v2.txt"`
- Tests (v1 et v2) : `py tests.py`

### Ce qui a été ajouté
- **Statut d'une commande** : `acceptée` ou `annulée` (attributs de classe `STATUT_ACCEPTEE` et `STATUT_ANNULEE`). Une commande annulée reste dans le journal et son ticket affiche ANNULÉE.
- **Annulation** : `Cafeteria.annuler_commande(numero)` renvoie `(annulée, motif, montant remboursé)`. Motifs de refus : `commande inconnue`, `commande déjà annulée`.
- **Rappel** : `Cafeteria.rappeler_produit(code)` renvoie `(rappelé, motif, résumé)`. Le résumé contient le produit, les numéros des commandes annulées, les clients remboursés avec leur montant, et le total.
- **Rapport de crise** : les rubriques de la v1 ne comptent que les commandes non annulées ; nouvelles rubriques pour les annulations, le total remboursé et les clients touchés par chaque rappel ; les produits rappelés sont signalés sur la carte.

### Mes choix de conception
1. **Tout ou rien** : `annuler_commande` vérifie d'abord (commande inconnue, déjà annulée) sans rien modifier, puis défait la commande : stock remis, badge remboursé, statut annulé, fidélité recalculée.
2. **Remboursement ≠ recharge** : `Client.rembourser` recrédite le badge sans plafond (le plafond de 150 € ne s'applique pas). Un visiteur est remboursé comptant : son solde ne change pas, mais le montant compte dans le total remboursé.
3. **Remise en stock ≠ réapprovisionnement** : `Produit.remettre_en_stock` rend les articles d'une commande annulée ; `approvisionner` reste réservé aux livraisons. Un produit rappelé ne revient jamais en stock, par aucune des deux méthodes.
4. **Rejeu de fidélité placé dans `Cafeteria`** (`recalculer_fidelite`) : c'est la seule classe qui possède le journal, donc la seule qui connaît toutes les commandes d'un client.
5. **Rejeu pour ma variante B3** : l'état de fidélité est le cumul des montants payés. Le rejeu refait donc la somme des montants payés des commandes non annulées du client. Les montants des autres commandes ne sont jamais recalculés : un avantage déjà obtenu reste acquis. Après une annulation, un client peut repasser sous 40 € et perdre la réduction pour ses commandes **suivantes**.
6. **Ordre dans l'annulation** : le statut passe à `annulée` **avant** le rejeu, pour que la commande annulée ne soit plus comptée.
7. **Ordre dans le rappel** : le produit est marqué rappelé **avant** les annulations (son stock reste à 0), puis les commandes sont annulées dans l'ordre du journal, qui est l'ordre chronologique. Le rappel réutilise `annuler_commande`.
8. **Motifs de refus** : `produit rappelé` (commande ou réapprovisionnement) et `déjà rappelé` sont comptés dans le rapport. Les refus d'annulation (`commande inconnue`, `commande déjà annulée`) sont renvoyés mais pas comptés, car ce compteur concerne les commandes. Un code inconnu au rappel est refusé sans rien modifier ni compter.
9. **Test du rappel en premier** dans `est_disponible` : un produit rappelé a un stock de 0, il doit être refusé pour « produit rappelé » et non pour « rupture de stock ». De même, la carte teste « RAPPELÉ » avant « ÉPUISÉ ».
10. **Clients touchés par un rappel** : une ligne par commande annulée, triée par montant décroissant.
11. **Scénario v2** dans un fichier séparé (`scenario_v2.py`), pour que `py campuscafe.py` joue toujours la v1.
### Bonus — Click & collect
- `traiter_commande(client, heure, demandes, creneau=None)` : un créneau est désigné par son heure de début (`"12:30"` pour 12:30–12:45).
- Un créneau commence sur un quart d'heure, au moins 10 minutes après la commande, et se termine au plus tard à 18:30. Sinon : refus « créneau invalide ».
- Au plus 10 commandes par créneau (`CAPACITE_CRENEAU`) : refus « créneau complet ». Ces vérifications ont lieu avant la création de la commande.
- Les places occupées sont les commandes non annulées du créneau : une annulation libère donc la place automatiquement.
- Statuts : « à retirer » à l'acceptation, « retirée » avec `retirer_commande(numero)`, « annulée » après une annulation. Une commande sans créneau garde le statut « acceptée ».
- Les heures sont converties en minutes (`en_minutes`, `en_heure`) pour pouvoir ajouter 10 ou 15 minutes.
- Le rapport affiche le taux de remplissage de chaque créneau utilisé.
