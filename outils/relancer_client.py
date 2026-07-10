"""
Outil : relancer_client
-------------------------
Action à impact réel (envoi potentiel d'un message au client) :
DOIT toujours passer par une confirmation utilisateur avant exécution
(voir agent.py, boucle de confirmation).
"""


def relancer_client(client: str, motif: str = "impayé") -> dict:
    # TODO (semaine 3/4) : remplacer par un appel réel au Backend
    # qui déclenchera l'envoi effectif de la relance (email, etc.).
    return {
        "status": "succès",
        "relance": f"Relance envoyée à {client} (motif : {motif})",
    }
