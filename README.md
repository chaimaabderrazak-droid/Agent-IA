# Agent IA — Stage (logiciel de facturation)

Agent conversationnel qui exécute des tâches comptables de base (création de
facture, catégorisation de dépense, relance client, rapprochement bancaire,
résumé financier) via function calling, branché sur l'API du Backend.

LLM utilisé : **Groq** (API cloud gratuite, modèle `llama-3.3-70b-versatile`).

## Structure du projet

```
agent-ia-stage/
├── outils/              # une fonction métier par fichier
├── mock_backend/         # mock FastAPI simulant l'API Backend (en attendant l'API réelle)
├── tests/                 # scripts de test du function calling
├── agent.py               # boucle principale de l'agent
├── llm_client.py           # configuration centralisée du client Groq
├── tools_schema.py        # définitions JSON Schema des outils pour le LLM
├── prompts.py              # instruction système de l'agent
├── .env                     # contient GROQ_API_KEY (ne jamais versionner)
├── .env.example              # modèle du .env, sans la vraie clé
└── requirements.txt
```

## Installation

```
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Crée ton fichier `.env` à la racine du projet (copie `.env.example`) et renseigne ta clé :

```
GROQ_API_KEY=ta_cle_ici
```

Récupère ta clé sur **https://console.groq.com** (section "API Keys").

## Lancer l'agent

```
python agent.py
```

## Lancer le mock du Backend (optionnel, dans un autre terminal)

```
cd mock_backend
uvicorn main:app --reload
```

## Lancer les tests de function calling

```
python tests/test_function_calling.py
```

## Règles importantes du projet

- Ne jamais inventer un taux de TVA : toujours passer par l'endpoint de règles pays du Backend.
- Toute action à impact réel (facture, relance) doit être confirmée par l'utilisateur avant exécution.
- L'agent reste un assistant de gestion, jamais un expert-comptable : pas de conseil fiscal engageant.
- La clé API Groq ne doit jamais être écrite en dur dans le code ni versionnée sur Git (`.env` est dans `.gitignore`).
