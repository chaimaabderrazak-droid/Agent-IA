import ollama

def creer_facture(client, montant, description):
    """Fonction simulée — remplacera l'appel réel au Backend plus tard"""
    return {
        "status": "succès",
        "facture": f"Facture créée pour {client} : {montant}€ ({description})"
    }

response = ollama.chat(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Crée une facture pour Ahmed de 500 euros pour du conseil"}],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "creer_facture",
                "description": "Crée une facture pour un client",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client": {"type": "string"},
                        "montant": {"type": "number"},
                        "description": {"type": "string"},
                    },
                    "required": ["client", "montant"],
                },
            },
        }
    ],
)

print(response)

