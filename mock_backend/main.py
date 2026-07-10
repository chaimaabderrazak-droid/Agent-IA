"""
mock_backend/main.py
-----------------------
Mock du Backend en attendant que l'API réelle soit stable (semaine 3).

Lancer avec (depuis le dossier mock_backend) :
    uvicorn main:app --reload

Puis tester sur http://127.0.0.1:8000 ou via Postman.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Mock Backend fonctionne"}


@app.post("/factures")
def creer_facture_endpoint(payload: dict):
    # TODO : remplacer par la vraie logique une fois l'API Backend stable.
    return {"status": "succès", "facture": payload}


@app.get("/regles-pays/{pays}")
def regles_pays(pays: str):
    # TODO : brancher sur les vraies règles TVA par pays côté Backend.
    # Ne JAMAIS laisser le LLM deviner ce taux — toujours passer par cet endpoint.
    regles_simulees = {"FR": {"tva": 20.0}, "TN": {"tva": 19.0}}
    return regles_simulees.get(pays.upper(), {"tva": None, "message": "Pays non reconnu"})
