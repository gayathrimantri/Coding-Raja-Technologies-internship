import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime
from matplotlib import pyplot as plt
from matplotlib_venn import venn2

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Budget Tracker')
        self.root.geometry('800x500')

        self.expenses_file = "expenses.txt"
        self.income_file = "income.txt"
        self.categories_file = "categories.txt"
        self.expense_categories = ['Stay', 'Food', 'Clothing', 'Travel', 'Home', 'Others']

        self.main_label = tk.Label(self.root, text='Budget Tracker', font=('Arial', 24))
        self.main_label.pack()

        self.create_income_expense_toggle()
        self.create_category_menu()
        self.create_amount_entry()

        self.add_expense_button = tk.Button(self.root, text='Add Entry', command=self.add_entry)
        self.add_expense_button.pack(pady=10)

        self.show_budget_button = tk.Button(self.root, text='Available Budget', command=self.show_available_budget)
        self.show_budget_button.pack(pady=10)

        self.show_insights_button = tk.Button(self.root, text='Show Insights', command=self.show_insights)
        self.show_insights_button.pack(pady=10)

        self.transactions_tree = ttk.Treeview(self.root, columns=('Category', 'Amount', 'Date'), show='headings')
        self.transactions_tree.heading('Category', text='Category')
        self.transactions_tree.heading('Amount', text='Amount')
        self.transactions_tree.heading('Date', text='Date')
        self.transactions_tree.pack(pady=10)

    def create_income_expense_toggle(self):
        self.toggle_var = tk.StringVar(self.root)
        self.toggle_var.set("Expense")
        self.toggle_expense = tk.Radiobutton(self.root, text="Expense", variable=self.toggle_var, value="Expense")
        self.toggle_income = tk.Radiobutton(self.root, text="Income", variable=self.toggle_var, value="Income")
        self.toggle_expense.pack()
        self.toggle_income.pack()

    def create_category_menu(self):
        self.category_var = tk.StringVar(self.root)
        self.category_var.set("Select Category")
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *self.expense_categories)
        self.category_menu.pack(pady=10)

    def create_amount_entry(self):
        self.amount_label = tk.Label(self.root, text="Enter Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

    def get_category(self):
        category = self.category_var.get()
        return category if category != "Select Category" else None

    def get_amount(self):
        amount = self.amount_entry.get()
        if not amount:
            messagebox.showwarning("Warning", "Please enter amount.")
            return None
        try:
            amount = float(amount)
            return amount
        except ValueError:
            messagebox.showwarning("Warning", "Invalid amount. Please enter a valid number.")
            return None

    def add_entry(self):
        entry_type = self.toggle_var.get()
        category = self.get_category() if entry_type == "Expense" else "Income"
        if category is None and entry_type == "Expense":
            messagebox.showwarning("Warning", "Please select a category for expenses.")
            return
        amount = self.get_amount()
        if amount:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            if entry_type == "Expense":
                with open(self.expenses_file, "a") as file:
                    file.write(f"{category}, {amount}, {date}\n")
            else:
                with open(self.income_file, "a") as file:
                    file.write(f"{category}, {amount}, {date}\n")
            messagebox.showinfo("Success", "Entry added successfully.")
            # Update the transactions tree
            self.update_transactions_tree(category, amount, date)

    def calculate_available_budget(self):
        total_income = 0
        if os.path.exists(self.income_file):
            with open(self.income_file, "r") as file:
                lines = file.readlines()
            for line in lines:
                _, amount, _ = line.strip().split(", ")
                total_income += float(amount)
        total_expenses = 0
        if os.path.exists(self.expenses_file):
            with open(self.expenses_file, "r") as file:
                lines = file.readlines()
            for line in lines:
                _, amount, _ = line.strip().split(", ")
                total_expenses += float(amount)
        available_budget = total_income - total_expenses
        messagebox.showinfo("Available Budget", f"Available Budget: {available_budget}")

    def show_available_budget(self):
        self.calculate_available_budget()

    def get_expense_categories(self):
        expenses_categories = set()
        if os.path.exists(self.expenses_file):
            with open(self.expenses_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    category, _, _ = line.strip().split(", ")
                    expenses_categories.add(category)
        return expenses_categories

    def get_income_categories(self):
        income_categories = set()
        if os.path.exists(self.income_file):
            with open(self.income_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    category, _, _ = line.strip().split(", ")
                    income_categories.add(category)
        return income_categories
    
    def show_insights(self):
        total_expense_amount = sum(self.get_expense_amounts())
        total_income_amount = sum(self.get_income_amounts())

        plt.figure(figsize=(8, 6))
        venn2(subsets=(total_expense_amount, total_income_amount, total_income_amount - total_expense_amount),
            set_labels=('Expenses', 'Income'))
        plt.title('Transactions range')
        plt.show()

    def get_expense_amounts(self):
        expense_amounts = []
        if os.path.exists(self.expenses_file):
            with open(self.expenses_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    _, amount, _ = line.strip().split(", ")
                    expense_amounts.append(float(amount))
        return expense_amounts

    def get_income_amounts(self):
        income_amounts = []
        if os.path.exists(self.income_file):
            with open(self.income_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    _, amount, _ = line.strip().split(", ")
                    income_amounts.append(float(amount))
        return income_amounts

    def update_transactions_tree(self, category, amount, date):
        self.transactions_tree.insert('', 'end', values=(category, amount, date))

def main():
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

