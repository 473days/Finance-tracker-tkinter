# Personal Finance Tracker

A web-based personal finance tracking application built with FastAPI and vanilla JavaScript.

## Screenshots and Demos

# Application Overview
<img width="1914" height="915" alt="image" src="https://github.com/user-attachments/assets/1ba0e276-d2b2-47e8-98f2-6d218e9e1d33" />

# Features Demo
<img width="1265" height="425" alt="image" src="https://github.com/user-attachments/assets/bcefb8d7-2400-446f-a435-4a454352c160" />

<img width="1267" height="424" alt="image" src="https://github.com/user-attachments/assets/eca44b7c-46d2-498c-b5cf-139e9c869df9" />




## Features

- Track income and expenses
- Categorize transactions
- Monthly financial summaries
- Category-wise spending analysis
- Easy data management

## Tech Stack

- **Backend**: FastAPI, SQLite, Pydantic, Uvicorn
- **Frontend**: Bootstrap, Vanilla JavaScript, Fetch API
- **Currency**: Euro (€)

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

## Project Structure
finance-tracker/
├── main.py                 # FastAPI backend application
├── requirements.txt        # Python dependencies
├── static/                # Frontend assets
│   ├── index.html         # Main HTML file
│   └── app.js            # JavaScript application logic
└── README.md             # This file

## Future Enhancements
User authentication and multiple accounts
Data export (CSV, PDF reports)
Recurring transactions
Budget setting and alerts
Charts and data visualization
Mobile app version
Currency conversion
Receipt image upload
