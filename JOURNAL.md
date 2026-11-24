## 29/10/2026
- Fait : installation de l'environnement (Python 3.14.7, Git), classes Produit, Client, Commande et leurs tests.
- Bloqué : `python` non reconnu → utilisé `py`. ImportError → le fichier n'était pas enregistré (Ctrl + S).
- Bloqué : `__pycache__` suivi par Git → espaces avant le nom dans .gitignore, corrigé avec `git rm -r --cached`.
- Fait : classe Cafeteria (tout ou rien, remise A1, fidélité B3), scénario de la journée.
- Vérifié : les événements 2, 6 et 11 correspondent au calcul à la main (2,16 € ; 4,94 € ; 6,84 €).

## 30/10/2026
- Fait : rapport de clôture et ses tests, fichier sortie_scenario.txt, README.
- Bloqué : IndentationError ligne 286 → le corps d'une méthode n'était pas assez décalé (8 espaces).
- Remarqué : les numéros de tickets sautent (3, 6, 9) → ce sont des commandes créées puis refusées. Choix expliqué dans le README.

## 24/11/2026 — Journée d'évolution « Rappel de lot »
- Fait : tag v1.0 posé sur la version soutenue (oublié avant), création de la branche evolution.
- Fait : calculs à la main des événements 12:15, 12:18, 12:25 et 12:30 (conception/evolution/).
- Phase 1 : statut des commandes, annulation en tout ou rien, rejeu de fidélité B3 dans Cafeteria, 8 tests.
- Phase 2 : rappel d'un produit, nouveaux motifs de refus, réutilisation de l'annulation, 6 tests.
- Phase 3 : rapport de crise (commandes non annulées seulement), scénario v2, sortie_scenario_v2.txt, README.
- Vérifié : le programme donne les mêmes résultats que le calcul à la main (8,74 € ; 4,14 € ; 4,14 € remboursés ; rappel 15,58 €).
- Remarqué : dans le rappel, le stock du Wrap doit rester à 0 → il faut marquer le produit rappelé AVANT les annulations.
