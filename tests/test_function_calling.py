"""
tests/test_function_calling.py
---------------------------------
Script de test isolé pour valider que le modèle (via Groq) appelle
correctement un outil donné avec les bons arguments. Sert à rejouer les
mêmes scénarios après chaque modification du prompt ou des schémas d'outils.

IMPORTANT : ce script importe llm_client, donc il doit être lancé depuis
la racine du projet (pas depuis le dossier tests/) :

    python tests/test_function_calling.py
"""

import json
import sys
from pathlib import Path

# Permet d'importer llm_client.py et tools_schema.py depuis la racine
# du projet, même en lançant ce script depuis le dossier tests/.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from llm_client import client, MODELE
from tools_schema import TOOLS

# Jeu de phrases de test : ajoute-en au fur et à mesure de tes essais.
PHRASES_DE_TEST = [
    "Crée une facture pour Ahmed de 500 euros pour du conseil",
    "Catégorise cette dépense : 45 euros chez Amazon, achat de fournitures",
    "Relance le client Ali pour impayé",
    "Comment va ma trésorerie ce mois-ci ?",
    "Fais une facture",  # cas ambigu volontaire : infos manquantes
]


def tester_phrase(phrase: str):
    print(f"\n{'=' * 60}\nPhrase testée : {phrase}")
    response = client.chat.completions.create(
        model=MODELE,
        messages=[{"role": "user", "content": phrase}],
        tools=TOOLS,
    )
    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            arguments = json.loads(tool_call.function.arguments)
            print(f"  -> Outil appelé : {tool_call.function.name}")
            print(f"     Arguments   : {arguments}")
    else:
        print(f"  -> Réponse texte (pas d'appel d'outil) : {message.content}")


if __name__ == "__main__":
    for phrase in PHRASES_DE_TEST:
        tester_phrase(phrase)
