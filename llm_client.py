"""
llm_client.py
----------------
Configuration centralisée du client Groq.

Toute la logique de connexion au LLM passe par ce fichier : si Groq change
de nom de modèle, ou si tu changes de fournisseur plus tard, tu ne modifies
que ce fichier, pas le reste du projet.

La clé API est lue depuis le fichier .env (jamais écrite en dur dans le code).
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # charge les variables définies dans .env

API_KEY = os.environ.get("GROQ_API_KEY")

if not API_KEY:
    sys.exit(
        "Erreur : GROQ_API_KEY est introuvable.\n"
        "Vérifie que ton fichier .env existe à la racine du projet et contient :\n"
        "GROQ_API_KEY=ta_cle_ici"
    )

client = Groq(api_key=API_KEY)

# Modèle utilisé pour tout le projet. Llama 3.3 70B offre un bon compromis
# qualité / vitesse / fiabilité du function calling sur le tier gratuit.
MODELE = "llama-3.3-70b-versatile"
