class FinanceTracker {
    constructor() {
        this.currentDate = new Date();
        this.init();
    }

    init() {
        this.updateMonthLabel();
        this.loadData();
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.getElementById('expenseForm').addEventListener('submit', (e) => this.addExpense(e));
        document.getElementById('incomeForm').addEventListener('submit', (e) => this.addIncome(e));
    }

    async loadData() {
        const month = this.currentDate.getMonth() + 1;
        const year = this.currentDate.getFullYear();

        try {
            const [expenses, income, summary] = await Promise.all([
                this.fetchExpenses(month, year),
                this.fetchIncome(month, year),
                this.fetchSummary(month, year)
            ]);

            this.displayExpenses(expenses);
            this.displayIncome(income);
            this.displaySummary(summary);
            this.displayCategories(summary.category_summary);
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError('Error loading data. Please try again.');
        }
    }

    async fetchExpenses(month, year) {
        const response = await fetch(`/expenses/?month=${month}&year=${year}`);
        if (!response.ok) throw new Error('Failed to fetch expenses');
        return response.json();
    }

    async fetchIncome(month, year) {
        const response = await fetch(`/income/?month=${month}&year=${year}`);
        if (!response.ok) throw new Error('Failed to fetch income');
        return response.json();
    }

    async fetchSummary(month, year) {
        const response = await fetch(`/summary/?month=${month}&year=${year}`);
        if (!response.ok) throw new Error('Failed to fetch summary');
        return response.json();
    }

    async addExpense(event) {
        event.preventDefault();
        
        const amount = parseFloat(document.getElementById('expenseAmount').value);
        const category = document.getElementById('expenseCategory').value;
        const description = document.getElementById('expenseDescription').value;

        if (!category) {
            this.showError('Please select a category');
            return;
        }

        const expense = {
            amount: amount,
            category: category,
            description: description,
            date: new Date().toISOString().split('T')[0]
        };

        try {
            const response = await fetch('/expenses/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expense)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to add expense');
            }

            document.getElementById('expenseForm').reset();
            this.loadData();
            this.showSuccess('Expense added successfully!');
        } catch (error) {
            console.error('Error adding expense:', error);
            this.showError('Error adding expense: ' + error.message);
        }
    }

    async addIncome(event) {
        event.preventDefault();
        
        const amount = parseFloat(document.getElementById('incomeAmount').value);
        const source = document.getElementById('incomeSource').value;
        const description = document.getElementById('incomeDescription').value;

        if (!source) {
            this.showError('Please select a source');
            return;
        }

        const income = {
            amount: amount,
            source: source,
            description: description,
            date: new Date().toISOString().split('T')[0]
        };

        try {
            const response = await fetch('/income/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(income)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to add income');
            }

            document.getElementById('incomeForm').reset();
            this.loadData();
            this.showSuccess('Income added successfully!');
        } catch (error) {
            console.error('Error adding income:', error);
            this.showError('Error adding income: ' + error.message);
        }
    }

    async deleteExpense(id) {
        if (!confirm('Are you sure you want to delete this expense?')) return;

        try {
            const response = await fetch(`/expenses/${id}`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Failed to delete expense');
            
            this.loadData();
            this.showSuccess('Expense deleted successfully!');
        } catch (error) {
            console.error('Error deleting expense:', error);
            this.showError('Error deleting expense. Please try again.');
        }
    }

    async deleteIncome(id) {
        if (!confirm('Are you sure you want to delete this income?')) return;

        try {
            const response = await fetch(`/income/${id}`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Failed to delete income');
            
            this.loadData();
            this.showSuccess('Income deleted successfully!');
        } catch (error) {
            console.error('Error deleting income:', error);
            this.showError('Error deleting income. Please try again.');
        }
    }

    displayExpenses(expenses) {
        const tbody = document.getElementById('expensesTable');
        
        if (expenses.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No expenses found</td></tr>';
            return;
        }

        tbody.innerHTML = expenses.map(expense => `
            <tr>
                <td>€${expense.amount.toFixed(2)}</td>
                <td>${expense.category}</td>
                <td>${expense.description || '-'}</td>
                <td>${expense.date}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="tracker.deleteExpense(${expense.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            </tr>
        `).join('');
    }

    displayIncome(income) {
        const tbody = document.getElementById('incomeTable');
        
        if (income.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No income found</td></tr>';
            return;
        }

        tbody.innerHTML = income.map(inc => `
            <tr>
                <td>€${inc.amount.toFixed(2)}</td>
                <td>${inc.source}</td>
                <td>${inc.description || '-'}</td>
                <td>${inc.date}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="tracker.deleteIncome(${inc.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            </tr>
        `).join('');
    }

    displaySummary(summary) {
        document.getElementById('totalIncome').textContent = `€${summary.total_income.toFixed(2)}`;
        document.getElementById('totalExpenses').textContent = `€${summary.total_expenses.toFixed(2)}`;
        
        const balanceElement = document.getElementById('balance');
        balanceElement.textContent = `€${summary.balance.toFixed(2)}`;
        balanceElement.className = summary.balance >= 0 ? 'balance-positive' : 'balance-negative';
    }

    displayCategories(categories) {
        const tbody = document.getElementById('categoriesTable');
        
        if (categories.length === 0) {
            tbody.innerHTML = '<tr><td colspan="2" class="text-center">No data available</td></tr>';
            return;
        }

        tbody.innerHTML = categories.map(cat => `
            <tr>
                <td>${cat.category}</td>
                <td>€${cat.total.toFixed(2)}</td>
            </tr>
        `).join('');
    }

    changeMonth(delta) {
        this.currentDate.setMonth(this.currentDate.getMonth() + delta);
        
        // Don't allow navigating to future months
        const now = new Date();
        if (this.currentDate > now) {
            this.currentDate = new Date(now.getFullYear(), now.getMonth(), 1);
            this.showError('Cannot navigate to future months');
        }
        
        this.updateMonthLabel();
        this.loadData();
    }

    updateMonthLabel() {
        const monthNames = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"];
        const monthName = monthNames[this.currentDate.getMonth()];
        const year = this.currentDate.getFullYear();
        document.getElementById('monthLabel').textContent = `${monthName} ${year}`;
    }

    showSuccess(message) {
        alert('Success: ' + message);
    }

    showError(message) {
        alert('Error: ' + message);
    }
}

// Initialize the tracker when the page loads
let tracker;
document.addEventListener('DOMContentLoaded', () => {
    tracker = new FinanceTracker();
});
