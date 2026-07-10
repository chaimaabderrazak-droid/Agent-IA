"""
Outil : categoriser_depense
-----------------------------
Aujourd'hui : logique simulée très basique.
Plus tard : appellera l'API réelle du Backend (catégories définies côté serveur).
"""


def categoriser_depense(montant: float, fournisseur: str, description: str = "") -> dict:
    # TODO (semaine 3) : remplacer par un appel réel au Backend.
    # Pour l'instant, catégorisation simulée en dur, juste pour tester le flux.
    categorie_simulee = "Fournitures" if "amazon" in fournisseur.lower() else "Autre"

    return {
        "status": "succès",
        "depense": f"{montant}€ chez {fournisseur} classée en '{categorie_simulee}' ({description})",
    }
