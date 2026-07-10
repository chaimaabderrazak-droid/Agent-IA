"""
Outil : resumer_finances
---------------------------
Action de lecture seule (aucun impact réel) : ne nécessite PAS de
confirmation avant exécution, contrairement à creer_facture ou relancer_client.
"""


def resumer_finances(periode: str = "ce mois-ci") -> dict:
    # TODO (semaine 4) : remplacer par un appel réel au Backend
    # pour récupérer les vrais chiffres de l'utilisateur.
    return {
        "status": "succès",
        "resume": f"Résumé simulé pour {periode} : 3 factures émises, 2 encaissées, 1 en retard.",
    }
