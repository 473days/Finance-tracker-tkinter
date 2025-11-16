import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('finance_tracker.db')
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
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
        
        self.conn.commit()
    
    def add_expense(self, amount, category, description, date):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?, ?, ?, ?)
        ''', (amount, category, description, date))
        self.conn.commit()
    
    def add_income(self, amount, source, description, date):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO income (amount, source, description, date)
            VALUES (?, ?, ?, ?)
        ''', (amount, source, description, date))
        self.conn.commit()
    
    def get_expenses(self, month=None, year=None):
        cursor = self.conn.cursor()
        if month and year:
            cursor.execute('''
                SELECT * FROM expenses 
                WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                ORDER BY date DESC
            ''', (f"{month:02d}", str(year)))
        else:
            cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        return cursor.fetchall()
    
    def get_income(self, month=None, year=None):
        cursor = self.conn.cursor()
        if month and year:
            cursor.execute('''
                SELECT * FROM income 
                WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                ORDER BY date DESC
            ''', (f"{month:02d}", str(year)))
        else:
            cursor.execute('SELECT * FROM income ORDER BY date DESC')
        return cursor.fetchall()
    
    def get_category_summary(self, month, year):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            GROUP BY category
        ''', (f"{month:02d}", str(year)))
        return cursor.fetchall()
    
    def delete_expense(self, expense_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        self.conn.commit()
    
    def delete_income(self, income_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM income WHERE id = ?', (income_id,))
        self.conn.commit()
    
    def close(self):
        self.conn.close()

class FinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg="#F5F5F5")
        
        # Initialize database
        self.db = Database()
        
        # Current view date
        self.current_date = datetime.now()
        
        # Setup UI
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Personal Finance Tracker", 
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        # Month navigation
        nav_frame = ttk.Frame(header_frame)
        nav_frame.pack(side=tk.RIGHT)
        
        ttk.Button(nav_frame, text="←", 
                  command=self.previous_month).pack(side=tk.LEFT, padx=5)
        self.month_label = ttk.Label(nav_frame, text="", font=("Arial", 12, "bold"))
        self.month_label.pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="→", 
                  command=self.next_month).pack(side=tk.LEFT, padx=5)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Input forms
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        self.create_input_forms(left_frame)
        
        # Right panel - Data display
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_display_area(right_frame)
        
        self.update_month_label()
    
    def create_input_forms(self, parent):
        # Expense form
        expense_frame = ttk.LabelFrame(parent, text="Add Expense", padding=10)
        expense_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(expense_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.expense_amount = ttk.Entry(expense_frame)
        self.expense_amount.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        
        ttk.Label(expense_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.expense_category = ttk.Combobox(expense_frame, values=[
            "Food", "Transport", "Entertainment", "Utilities", 
            "Shopping", "Healthcare", "Education", "Other"
        ])
        self.expense_category.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        
        ttk.Label(expense_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.expense_desc = ttk.Entry(expense_frame)
        self.expense_desc.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        
        ttk.Button(expense_frame, text="Add Expense", 
                  command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Income form
        income_frame = ttk.LabelFrame(parent, text="Add Income", padding=10)
        income_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(income_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.income_amount = ttk.Entry(income_frame)
        self.income_amount.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        
        ttk.Label(income_frame, text="Source:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.income_source = ttk.Combobox(income_frame, values=[
            "Salary", "Freelance", "Investment", "Gift", "Other"
        ])
        self.income_source.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        
        ttk.Label(income_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.income_desc = ttk.Entry(income_frame)
        self.income_desc.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        
        ttk.Button(income_frame, text="Add Income", 
                  command=self.add_income).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        expense_frame.columnconfigure(1, weight=1)
        income_frame.columnconfigure(1, weight=1)
    
    def create_display_area(self, parent):
        # Summary frame
        summary_frame = ttk.LabelFrame(parent, text="Financial Summary", padding=10)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Summary labels
        summary_grid = ttk.Frame(summary_frame)
        summary_grid.pack(fill=tk.X)
        
        self.total_income_label = ttk.Label(summary_grid, text="Total Income: $0", 
                                           font=("Arial", 12, "bold"))
        self.total_income_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        self.total_expense_label = ttk.Label(summary_grid, text="Total Expenses: $0", 
                                            font=("Arial", 12, "bold"))
        self.total_expense_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        self.balance_label = ttk.Label(summary_grid, text="Balance: $0", 
                                      font=("Arial", 12, "bold"))
        self.balance_label.grid(row=0, column=2, sticky=tk.W)
        
        # Notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Expenses tab
        expenses_frame = ttk.Frame(notebook)
        notebook.add(expenses_frame, text="Expenses")
        self.create_expenses_tab(expenses_frame)
        
        # Income tab
        income_frame = ttk.Frame(notebook)
        notebook.add(income_frame, text="Income")
        self.create_income_tab(income_frame)
        
        # Categories tab
        categories_frame = ttk.Frame(notebook)
        notebook.add(categories_frame, text="Categories")
        self.create_categories_tab(categories_frame)
    
    def create_expenses_tab(self, parent):
        # Treeview for expenses
        columns = ("ID", "Amount", "Category", "Description", "Date")
        self.expenses_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.expenses_tree.heading(col, text=col)
            self.expenses_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.expenses_tree.yview)
        self.expenses_tree.configure(yscrollcommand=scrollbar.set)
        
        self.expenses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Delete button
        delete_btn = ttk.Button(parent, text="Delete Selected", 
                               command=self.delete_expense)
        delete_btn.pack(pady=5)
    
    def create_income_tab(self, parent):
        # Treeview for income
        columns = ("ID", "Amount", "Source", "Description", "Date")
        self.income_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        # Configure columns
        for col in columns:
            self.income_tree.heading(col, text=col)
            self.income_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.income_tree.yview)
        self.income_tree.configure(yscrollcommand=scrollbar.set)
        
        self.income_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Delete button
        delete_btn = ttk.Button(parent, text="Delete Selected", 
                               command=self.delete_income)
        delete_btn.pack(pady=5)
    
    def create_categories_tab(self, parent):
        # Treeview for categories
        columns = ("Category", "Amount")
        self.categories_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        for col in columns:
            self.categories_tree.heading(col, text=col)
            self.categories_tree.column(col, width=150)
        
        self.categories_tree.pack(fill=tk.BOTH, expand=True)
    
    def add_expense(self):
        try:
            amount = float(self.expense_amount.get())
            category = self.expense_category.get()
            description = self.expense_desc.get()
            date = datetime.now().strftime("%Y-%m-%d")
            
            if not category:
                messagebox.showerror("Error", "Please select a category")
                return
            
            self.db.add_expense(amount, category, description, date)
            
            # Clear form
            self.expense_amount.delete(0, tk.END)
            self.expense_category.set('')
            self.expense_desc.delete(0, tk.END)
            
            self.load_data()
            messagebox.showinfo("Success", "Expense added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def add_income(self):
        try:
            amount = float(self.income_amount.get())
            source = self.income_source.get()
            description = self.income_desc.get()
            date = datetime.now().strftime("%Y-%m-%d")
            
            if not source:
                messagebox.showerror("Error", "Please select a source")
                return
            
            self.db.add_income(amount, source, description, date)
            
            # Clear form
            self.income_amount.delete(0, tk.END)
            self.income_source.set('')
            self.income_desc.delete(0, tk.END)
            
            self.load_data()
            messagebox.showinfo("Success", "Income added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def delete_expense(self):
        selected = self.expenses_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            for item in selected:
                expense_id = self.expenses_tree.item(item)['values'][0]
                self.db.delete_expense(expense_id)
            
            self.load_data()
            messagebox.showinfo("Success", "Expense deleted successfully!")
    
    def delete_income(self):
        selected = self.income_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an income to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this income?"):
            for item in selected:
                income_id = self.income_tree.item(item)['values'][0]
                self.db.delete_income(income_id)
            
            self.load_data()
            messagebox.showinfo("Success", "Income deleted successfully!")
    
    def load_data(self):
        # Clear existing data
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        for item in self.income_tree.get_children():
            self.income_tree.delete(item)
        
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        
        # Load expenses
        expenses = self.db.get_expenses(self.current_date.month, self.current_date.year)
        for expense in expenses:
            # Format the amount to 2 decimal places
            formatted_expense = (expense[0], f"${expense[1]:.2f}", expense[2], expense[3], expense[4])
            self.expenses_tree.insert("", tk.END, values=formatted_expense)
        
        # Load income
        income = self.db.get_income(self.current_date.month, self.current_date.year)
        for inc in income:
            # Format the amount to 2 decimal places
            formatted_income = (inc[0], f"${inc[1]:.2f}", inc[2], inc[3], inc[4])
            self.income_tree.insert("", tk.END, values=formatted_income)
        
        # Load category summary
        categories = self.db.get_category_summary(self.current_date.month, self.current_date.year)
        for category, amount in categories:
            self.categories_tree.insert("", tk.END, values=(category, f"${amount:.2f}"))
        
        # Update summary
        self.update_summary()
    
    def update_summary(self):
        expenses = self.db.get_expenses(self.current_date.month, self.current_date.year)
        income = self.db.get_income(self.current_date.month, self.current_date.year)
        
        total_expenses = sum(expense[1] for expense in expenses)
        total_income = sum(inc[1] for inc in income)
        balance = total_income - total_expenses
        
        self.total_income_label.config(text=f"Total Income: ${total_income:.2f}")
        self.total_expense_label.config(text=f"Total Expenses: ${total_expenses:.2f}")
        self.balance_label.config(text=f"Balance: ${balance:.2f}")
        
        # Color code balance
        if balance >= 0:
            self.balance_label.configure(foreground="green")
        else:
            self.balance_label.configure(foreground="red")
    
    def previous_month(self):
        # First day of current month minus one day gives last day of previous month
        first_day_current = self.current_date.replace(day=1)
        self.current_date = first_day_current - timedelta(days=1)
        self.update_month_label()
        self.load_data()
    
    def next_month(self):
        # First day of next month
        next_month = self.current_date.replace(day=28) + timedelta(days=4)
        self.current_date = next_month.replace(day=1)
        # Don't allow navigating to future months
        if self.current_date > datetime.now():
            self.current_date = datetime.now()
            messagebox.showinfo("Info", "Cannot navigate to future months")
        self.update_month_label()
        self.load_data()
    
    def update_month_label(self):
        month_name = self.current_date.strftime("%B %Y")
        self.month_label.config(text=month_name)
    
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

def main():
    root = tk.Tk()
    app = FinanceManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()