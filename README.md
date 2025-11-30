# Personal Finance Tracker

A web-based personal finance tracking application built with FastAPI and vanilla JavaScript.

## Features

- Track income and expenses
- Categorize transactions
- Monthly financial summaries
- Category-wise spending analysis
- Easy data management

## Tech Stack

- **Backend**: FastAPI, SQLite
- **Frontend**: Bootstrap, Vanilla JavaScript
- **Currency**: Euros (€)

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `uvicorn main:app --reload`
4. Open http://localhost:8000

## API Endpoints

- `POST /expenses/` - Add new expense
- `POST /income/` - Add new income
- `GET /expenses/` - Get expenses
- `GET /income/` - Get income
- `GET /summary/` - Get financial summary
- `DELETE /expenses/{id}` - Delete expense
- `DELETE /income/{id}` - Delete income
