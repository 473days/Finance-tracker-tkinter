Personal Finance Tracker

Eine webbasierte Anwendung zur Verwaltung persönlicher Finanzen, entwickelt mit FastAPI und vanilla JavaScript.
Screenshots und Demos
Anwendungsübersicht
<img width="1914" height="915" alt="image" src="https://github.com/user-attachments/assets/1ba0e276-d2b2-47e8-98f2-6d218e9e1d33" />
Funktionsdemo
<img width="1265" height="425" alt="image" src="https://github.com/user-attachments/assets/bcefb8d7-2400-446f-a435-4a454352c160" /><img width="1267" height="424" alt="image" src="https://github.com/user-attachments/assets/eca44b7c-46d2-498c-b5cf-139e9c869df9" />
Funktionen

    Einnahmen und Ausgaben verfolgen

    Transaktionen kategorisieren

    Monatliche Finanzübersichten

    Ausgabenanalyse nach Kategorien

    Einfache Datenverwaltung

Tech Stack

    Backend: FastAPI, SQLite, Pydantic, Uvicorn

    Frontend: Bootstrap, Vanilla JavaScript, Fetch API

    Währung: Euro (€)

Installation

    Repository klonen

    Abhängigkeiten installieren: pip install -r requirements.txt

    Anwendung starten: uvicorn main:app --reload

    Öffnen Sie http://localhost:8000

API Endpoints

    POST /expenses/ - Neue Ausgabe hinzufügen

    POST /income/ - Neue Einnahme hinzufügen

    GET /expenses/ - Ausgaben abrufen

    GET /income/ - Einnahmen abrufen

    GET /summary/ - Finanzübersicht abrufen

    DELETE /expenses/{id} - Ausgabe löschen

    DELETE /income/{id} - Einnahme löschen

Geplante Erweiterungen

    Benutzerauthentifizierung und mehrere Konten

    Datenexport (CSV, PDF-Berichte)

    Wiederkehrende Transaktionen

    Budgeteinstellungen und Warnungen

    Diagramme und Datenvisualisierung

    Mobile App-Version

    Währungsumrechnung

    Belegbild-Upload
