from campuscafe import Client, creer_cafeteria


def demander_entier(message):
    """Redemande tant que l'utilisateur ne tape pas un nombre entier."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Erreur : veuillez entrer un nombre entier.")


def demander_montant(message):
    """Redemande tant que l'utilisateur ne tape pas un nombre (avec un point : 12.50)."""
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Erreur : veuillez entrer un nombre, avec un point (exemple : 12.50).")


def demander_heure():
    """Redemande tant que l'heure n'est pas au format HH:MM."""
    while True:
        heure = input("Heure (HH:MM) : ").strip()
        if len(heure) == 5 and heure[2] == ":":
            return heure
        print("Erreur : l'heure doit être au format HH:MM (exemple : 09:15).")


def choisir_client(cafet):
    """Renvoie le client choisi, un nouveau visiteur, ou None si le nom est inconnu."""
    print("Clients :", ", ".join(cafet.clients), "ou visiteur")
    nom = input("Nom du client : ").strip()
    if nom == "visiteur":
        return Client("visiteur", "visiteur")
    if nom in cafet.clients:
        return cafet.clients[nom]
    print(f"Erreur : client inconnu ({nom}).")
    return None


def saisir_commande(cafet):
    """Demande les informations d'une commande, puis la fait traiter par la cafétéria."""
    client = choisir_client(cafet)
    if client is None:
        return
    heure = demander_heure()

    demandes = []
    while True:
        code = input("Code produit (Entrée vide pour terminer) : ").strip().upper()
        if code == "":
            break
        quantite = demander_entier("Quantité : ")
        demandes.append((code, quantite))

    if not demandes:
        print("Commande vide : rien à traiter.")
        return

    acceptee, motif, montant = cafet.traiter_commande(client, heure, demandes)
    if acceptee:
        print(f"Commande acceptée ({montant:.2f} €)")
        print(cafet.journal[-1])
    else:
        print(f"Commande REFUSÉE ({motif})")


def saisir_recharge(cafet):
    """Demande un client et un montant, puis recharge son badge."""
    client = choisir_client(cafet)
    if client is None:
        return
    montant = demander_montant("Montant de la recharge (€) : ")
    if cafet.recharger(client, montant):
        print(f"Recharge acceptée. Nouveau solde : {client.solde:.2f} €")
    else:
        print("Recharge REFUSÉE (entre 5 et 100 €, solde maximum 150 €, badge obligatoire).")


def saisir_reappro(cafet):
    """Demande un code et une quantité, puis réapprovisionne le produit."""
    code = input("Code produit : ").strip().upper()
    quantite = demander_entier("Quantité à ajouter : ")
    if cafet.reapprovisionner(code, quantite):
        print(f"Réapprovisionnement fait. Nouveau stock : {cafet.carte[code].stock}")
    else:
        print("Réapprovisionnement REFUSÉ (code inconnu ou quantité non positive).")


def afficher_clients(cafet):
    """Affiche tous les clients de la cafétéria."""
    for client in cafet.clients.values():
        print(f"  {client}")


def menu():
    """Boucle principale du menu."""
    cafet = creer_cafeteria()
    while True:
        print("\n===== CampusCafé — Menu =====")
        print("1. Passer une commande")
        print("2. Recharger un badge")
        print("3. Réapprovisionner un produit")
        print("4. Afficher la carte")
        print("5. Afficher les clients")
        print("6. Rapport de clôture")
        print("0. Quitter")
        choix = input("Votre choix : ").strip()

        match choix:
            case "1":
                saisir_commande(cafet)
            case "2":
                saisir_recharge(cafet)
            case "3":
                saisir_reappro(cafet)
            case "4":
                for produit in cafet.carte_triee():
                    print(f"  {produit}")
            case "5":
                afficher_clients(cafet)
            case "6":
                cafet.afficher_rapport()
            case "0":
                print("Au revoir !")
                break
            case _:
                print("Choix invalide : tapez un chiffre entre 0 et 6.")


if __name__ == "__main__":
    menu()