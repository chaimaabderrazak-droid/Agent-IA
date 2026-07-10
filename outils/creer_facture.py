"""
Outil : creer_facture
----------------------
Aujourd'hui : retourne des données simulées.
Plus tard : appellera l'API réelle du Backend via requests.post(...).
"""


def creer_facture(client: str, montant: float, description: str = "") -> dict:
    # TODO (semaine 3) : remplacer par un appel réel au Backend, par ex :
    # import requests
    # response = requests.post("http://backend-api/factures", json={...})
    # return response.json()

    return {
        "status": "succès",
        "facture": f"Facture créée pour {client} : {montant}€ ({description})",
    }
