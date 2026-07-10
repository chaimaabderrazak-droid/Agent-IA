"""
Outil : rapprocher_paiement
------------------------------
Rapprochement bancaire basique (semaine 4 selon planning).
Aujourd'hui : simulation d'un rapprochement simple par montant.
Plus tard : import CSV réel + correspondance avec les factures existantes
via l'API Backend.
"""


def rapprocher_paiement(montant: float, reference: str = "") -> dict:
    # TODO : brancher sur l'import CSV réel + l'API Backend.
    return {
        "status": "succès",
        "rapprochement": f"Paiement de {montant}€ rapproché (référence : {reference or 'non fournie'})",
    }
