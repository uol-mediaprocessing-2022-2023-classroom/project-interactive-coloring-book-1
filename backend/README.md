# Backend Demo

## Setup
1. Python wird benötigt und kann hier heruntergeladen werden: https://www.python.org/downloads/ (ich nutze Python 3.10)
2. Führe diesen Befehlt in der Konsole aus:
```
pip install -r .\requirements.txt
```

## Starten der App
```
uvicorn app.main:app --reload
```

## Zum Backend
<p>Die Anwendung dient als ein simples Python basiertes Backend für eine Webapp.</p>
<p>Der einzige Endpoint ("/get-blur") fügt einen Blur einen Bild hinzu und Antwortet mit dem bearbeitetem Bild.</p>

Docs: https://fastapi.tiangolo.com/tutorial/
