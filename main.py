# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os

# Create FastAPI app instance
app = FastAPI(title="Personal Finance Tracker", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    print(f"Created {static_dir} directory")

# Database setup
class Database:
    def __init__(self):
        self.db_path = 'finance_tracker.db'
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        ''')
        
        # Income table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                source TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    
    def add_expense(self, amount: float, category: str, description: str, date: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        ''', (amount, category, description, date))
        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()
        return expense_id
    
    def add_income(self, amount: float, source: str, description: str, date: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO income (amount, source, description, date)
            VALUES (?, ?, ?, ?)
        ''', (amount, source, description, date))
        conn.commit()
        income_id = cursor.lastrowid
        conn.close()
        return income_id
    
    def get_expenses(self, month: Optional[int] = None, year: Optional[int] = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if month and year:
            cursor.execute('''
                SELECT * FROM expenses 
                WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                ORDER BY date DESC
            ''', (f"{month:02d}", str(year)))
        else:
            cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        
        expenses = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "amount": row[1],
                "category": row[2],
                "description": row[3],
                "date": row[4]
            }
            for row in expenses
        ]
    
    def get_income(self, month: Optional[int] = None, year: Optional[int] = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if month and year:
            cursor.execute('''
                SELECT * FROM income 
                WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                ORDER BY date DESC
            ''', (f"{month:02d}", str(year)))
        else:
            cursor.execute('SELECT * FROM income ORDER BY date DESC')
        
        income = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "amount": row[1],
                "source": row[2],
                "description": row[3],
                "date": row[4]
            }
            for row in income
        ]
    
    def get_category_summary(self, month: int, year: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY category
        ''', (f"{month:02d}", str(year)))
        
        summary = cursor.fetchall()
        conn.close()
        
        return [{"category": row[0], "total": row[1]} for row in summary]
    
    def delete_expense(self, expense_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    
    def delete_income(self, income_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM income WHERE id = ?', (income_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

# Pydantic models
class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str = ""
    date: str

class IncomeCreate(BaseModel):
    amount: float
    source: str
    description: str = ""
    date: str

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str
    date: str

class IncomeResponse(BaseModel):
    id: int
    amount: float
    source: str
    description: str
    date: str

class CategorySummary(BaseModel):
    category: str
    total: float

class FinancialSummary(BaseModel):
    total_income: float
    total_expenses: float
    balance: float
    category_summary: List[CategorySummary]

# Dependency
def get_db():
    db = Database()
    try:
        yield db
    finally:
        pass

# Routes
@app.post("/expenses/", response_model=dict)
def add_expense(expense: ExpenseCreate, db: Database = Depends(get_db)):
    try:
        expense_id = db.add_expense(
            expense.amount,
            expense.category,
            expense.description,
            expense.date
        )
        return {"message": "Expense added successfully", "id": expense_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/income/", response_model=dict)
def add_income(income: IncomeCreate, db: Database = Depends(get_db)):
    try:
        income_id = db.add_income(
            income.amount,
            income.source,
            income.description,
            income.date
        )
        return {"message": "Income added successfully", "id": income_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/expenses/", response_model=List[ExpenseResponse])
def get_expenses(month: Optional[int] = None, year: Optional[int] = None, db: Database = Depends(get_db)):
    return db.get_expenses(month, year)

@app.get("/income/", response_model=List[IncomeResponse])
def get_income(month: Optional[int] = None, year: Optional[int] = None, db: Database = Depends(get_db)):
    return db.get_income(month, year)

@app.get("/summary/", response_model=FinancialSummary)
def get_summary(month: int, year: int, db: Database = Depends(get_db)):
    expenses = db.get_expenses(month, year)
    income = db.get_income(month, year)
    category_summary = db.get_category_summary(month, year)
    
    total_expenses = sum(expense["amount"] for expense in expenses)
    total_income = sum(inc["amount"] for inc in income)
    balance = total_income - total_expenses
    
    return FinancialSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        category_summary=category_summary
    )

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Database = Depends(get_db)):
    success = db.delete_expense(expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}

@app.delete("/income/{income_id}")
def delete_income(income_id: int, db: Database = Depends(get_db)):
    success = db.delete_income(income_id)
    if not success:
        raise HTTPException(status_code=404, detail="Income not found")
    return {"message": "Income deleted successfully"}

# Serve frontend - this should be after all API routes
@app.get("/")
async def read_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        raise HTTPException(status_code=404, detail="Frontend not found. Make sure static/index.html exists.")

# Mount static files - this should be last
app.mount("/static", StaticFiles(directory=static_dir), name="static")

print("Finance Tracker backend started successfully!")
print("Available routes:")
print("  GET  / - Main application")
print("  POST /expenses/ - Add expense")
print("  POST /income/ - Add income")
print("  GET  /expenses/ - Get expenses")
print("  GET  /income/ - Get income")
print("  GET  /summary/ - Get financial summary")
print("  DELETE /expenses/{id} - Delete expense")
print("  DELETE /income/{id} - Delete income")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)