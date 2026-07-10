"""
tools_schema.py
------------------
Définitions JSON Schema des outils transmises au LLM (Ollama).

Important : ce fichier décrit uniquement "ce que le LLM voit" (nom,
description, paramètres attendus). La logique réelle de chaque outil
vit dans outils/*.py. Garder les deux séparés facilite l'ajustement
des descriptions (souvent la partie la plus itérative) sans toucher
au code métier.

Astuce : plus une description est précise et concrète, plus le LLM
extrait correctement les arguments. N'hésite pas à donner des exemples
dans les descriptions si le modèle se trompe souvent.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "creer_facture",
            "description": "Crée une facture pour un client à partir d'une demande en langage naturel.",
            "parameters": {
                "type": "object",
                "properties": {
                    "client": {"type": "string", "description": "Nom du client à facturer"},
                    "montant": {"type": "number", "description": "Montant total en euros"},
                    "description": {"type": "string", "description": "Détail de la prestation ou du produit"},
                },
                "required": ["client", "montant"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "categoriser_depense",
            "description": "Catégorise une dépense à partir d'un reçu ou d'une ligne de relevé bancaire.",
            "parameters": {
                "type": "object",
                "properties": {
                    "montant": {"type": "number", "description": "Montant de la dépense en euros"},
                    "fournisseur": {"type": "string", "description": "Nom du fournisseur ou commerçant"},
                    "description": {"type": "string", "description": "Détail complémentaire de la dépense"},
                },
                "required": ["montant", "fournisseur"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "relancer_client",
            "description": "Envoie une relance à un client pour un impayé. Action à impact réel : nécessite confirmation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "client": {"type": "string", "description": "Nom du client à relancer"},
                    "motif": {"type": "string", "description": "Raison de la relance (ex. impayé, retard)"},
                },
                "required": ["client"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rapprocher_paiement",
            "description": "Rapproche un paiement reçu avec une facture ou dépense existante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "montant": {"type": "number", "description": "Montant du paiement en euros"},
                    "reference": {"type": "string", "description": "Référence bancaire ou libellé du paiement"},
                },
                "required": ["montant"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "resumer_finances",
            "description": "Donne un résumé de la situation financière de l'utilisateur sur une période. Lecture seule, pas de confirmation nécessaire.",
            "parameters": {
                "type": "object",
                "properties": {
                    "periode": {"type": "string", "description": "Période concernée (ex. ce mois-ci, le mois dernier)"},
                },
                "required": [],
            },
        },
    },
]

# Outils dont l'exécution a un impact réel et nécessite donc une confirmation
# explicite de l'utilisateur avant d'être exécutés (voir agent.py).
OUTILS_A_CONFIRMER = {"creer_facture", "relancer_client", "rapprocher_paiement"}
