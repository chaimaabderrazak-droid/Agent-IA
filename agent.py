"""
agent.py
----------
Boucle principale de l'Agent IA, connectée à Groq.

Cycle général (agent loop) :
  1. Message utilisateur
  2. Envoi au LLM (Groq) avec le prompt système + la liste des outils
  3. Si le LLM demande un appel d'outil :
       - si l'outil est sensible (impact réel) -> demander confirmation
       - exécuter la fonction correspondante
       - renvoyer le résultat au LLM pour qu'il formule une réponse finale
  4. Si le LLM répond directement en texte (ex. clarification) -> afficher

Lancer avec : python agent.py
"""

import json

from groq import APIError, APIConnectionError, BadRequestError, RateLimitError

from llm_client import client, MODELE
from prompts import SYSTEM_PROMPT
from tools_schema import TOOLS, OUTILS_A_CONFIRMER
from outils.creer_facture import creer_facture
from outils.categoriser_depense import categoriser_depense
from outils.relancer_client import relancer_client
from outils.rapprocher_paiement import rapprocher_paiement
from outils.resumer_finances import resumer_finances

# Table de correspondance nom d'outil -> fonction Python réelle
FONCTIONS_DISPONIBLES = {
    "creer_facture": creer_facture,
    "categoriser_depense": categoriser_depense,
    "relancer_client": relancer_client,
    "rapprocher_paiement": rapprocher_paiement,
    "resumer_finances": resumer_finances,
}


def demander_confirmation(nom_outil: str, arguments: dict) -> bool:
    print(f"\n⚠️  L'agent souhaite exécuter : {nom_outil}({arguments})")
    reponse = input("Confirmer cette action ? (o/n) : ").strip().lower()
    return reponse == "o"


def executer_outil(nom_outil: str, arguments: dict) -> dict:
    fonction = FONCTIONS_DISPONIBLES.get(nom_outil)
    if fonction is None:
        return {"status": "erreur", "message": f"Outil inconnu : {nom_outil}"}
    return fonction(**arguments)


def appeler_llm(messages: list):
    """Appelle Groq et intercepte les erreurs possibles au lieu de laisser
    planter le programme. Retourne le message du LLM, ou None en cas d'échec
    (auquel cas un message d'erreur adapté a déjà été affiché à l'utilisateur)."""

    try:
        response = client.chat.completions.create(
            model=MODELE,
            messages=messages,
            tools=TOOLS,
        )
        return response.choices[0].message

    except BadRequestError as e:
        # Cas typique : "tool_use_failed" -> le modèle a généré un appel
        # d'outil mal formé (JSON tronqué/invalide). Ce n'est pas une erreur
        # de notre code, mais un raté ponctuel de génération du LLM.
        print(
            "\n⚠️  L'agent n'a pas réussi à formuler correctement son action "
            "(erreur interne du modèle). Peux-tu reformuler ta demande "
            "de façon plus précise ?"
        )
        return None

    except RateLimitError:
        print(
            "\n⚠️  Limite de requêtes Groq atteinte pour le moment. "
            "Réessaie dans quelques instants."
        )
        return None

    except APIConnectionError:
        print(
            "\n⚠️  Impossible de contacter l'API Groq (problème réseau). "
            "Vérifie ta connexion internet et réessaie."
        )
        return None

    except APIError as e:
        print(f"\n⚠️  Erreur inattendue de l'API Groq : {e}")
        return None


def traiter_message(messages: list) -> list:
    """Envoie les messages au LLM, gère l'appel d'outil éventuel,
    et retourne l'historique de messages mis à jour."""

    message_llm = appeler_llm(messages)
    if message_llm is None:
        # Échec du premier appel : on ne touche pas à l'historique, on laisse
        # l'utilisateur reformuler son dernier message au tour suivant.
        return messages

    # On ajoute la réponse du LLM à l'historique (format attendu par l'API :
    # un dict, pas l'objet Python directement)
    messages.append(message_llm.model_dump(exclude_none=True))

    if message_llm.tool_calls:
        for tool_call in message_llm.tool_calls:
            nom_outil = tool_call.function.name

            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                resultat = {
                    "status": "erreur",
                    "message": "Arguments d'outil invalides (JSON malformé).",
                }
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(resultat, ensure_ascii=False),
                })
                continue

            if nom_outil in OUTILS_A_CONFIRMER:
                if not demander_confirmation(nom_outil, arguments):
                    resultat = {"status": "annulé", "message": "Action annulée par l'utilisateur."}
                else:
                    resultat = executer_outil(nom_outil, arguments)
            else:
                # Outils en lecture seule (ex. resumer_finances) : pas de confirmation
                resultat = executer_outil(nom_outil, arguments)

            # On renvoie le résultat de l'outil au LLM. Le format OpenAI/Groq
            # exige un role "tool" avec le tool_call_id correspondant.
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(resultat, ensure_ascii=False),
            })

        # Deuxième appel : le LLM formule sa réponse finale à partir du résultat
        message_final = appeler_llm(messages)
        if message_final is None:
            # L'outil a bien été exécuté (le résultat est dans l'historique),
            # seule la formulation finale du LLM a échoué. On informe
            # l'utilisateur sans perdre le travail déjà fait.
            print(
                "\nAgent : L'action a été traitée, mais je n'ai pas réussi à "
                "formuler ma réponse. Tu peux me redemander un résumé."
            )
            return messages

        messages.append(message_final.model_dump(exclude_none=True))
        print(f"\nAgent : {message_final.content}")
    else:
        print(f"\nAgent : {message_llm.content}")

    return messages


def main():
    print("Agent IA (Groq) — tape 'quitter' pour arrêter.\n")
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        entree_utilisateur = input("Toi : ").strip()
        if entree_utilisateur.lower() in ("quitter", "exit", "quit"):
            break

        messages.append({"role": "user", "content": entree_utilisateur})
        messages = traiter_message(messages)


if __name__ == "__main__":
    main()