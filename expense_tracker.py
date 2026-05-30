import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# File to save expenses
FILE_NAME = "expenses.csv"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💸 Expense Tracker")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # Initialize CSV
        self.initialize_csv()

        # Title
        title = tk.Label(root, text="Expense Tracker", font=("Arial", 20, "bold"), bg="#f0f0f0")
        title.pack(pady=10)

        # Input Frame
        input_frame = tk.LabelFrame(root, text="Add New Expense", padx=10, pady=10, bg="#f0f0f0")
        input_frame.pack(fill="x", padx=20, pady=10)

        # Date
        tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Amount
        tk.Label(input_frame, text="Amount (₹):", bg="#f0f0f0").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.amount_entry = tk.Entry(input_frame, width=12)
        self.amount_entry.grid(row=0, column=3, padx=5)

        # Category
        tk.Label(input_frame, text="Category:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=(10,0))
        self.category_combo = ttk.Combobox(input_frame, values=[
            "Food", "Transport", "Rent", "Shopping", "Entertainment", 
            "Bills", "Education", "Health", "Others"], width=18)
        self.category_combo.grid(row=1, column=1, padx=5, pady=(10,0))
        self.category_combo.set("Food")

        # Description
        tk.Label(input_frame, text="Description:", bg="#f0f0f0").grid(row=1, column=2, sticky="w", padx=(20,0), pady=(10,0))
        self.desc_entry = tk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=(10,0))

        # Add Button
        add_btn = tk.Button(input_frame, text="Add Expense", bg="#4CAF50", fg="white", 
                           font=("Arial", 10, "bold"), command=self.add_expense)
        add_btn.grid(row=2, column=1, columnspan=3, pady=15)

        # Treeview Frame
        tree_frame = tk.Frame(root)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview (Table)
        columns = ("Date", "Amount", "Category", "Description")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Buttons Frame
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Refresh", bg="#2196F3", fg="white", command=self.load_expenses).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", bg="#f44336", fg="white", command=self.delete_expense).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Show Summary", bg="#FF9800", fg="white", command=self.show_summary).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Exit", bg="#9E9E9E", fg="white", command=root.quit).pack(side="left", padx=5)

        # Load existing data
        self.load_expenses()

    def initialize_csv(self):
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Amount", "Category", "Description"])

    def add_expense(self):
        date = self.date_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_combo.get().strip()
        description = self.desc_entry.get().strip()

        if not amount or not category:
            messagebox.showwarning("Input Error", "Amount and Category are required!")
            return

        try:
            float(amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number!")
            return

        with open(FILE_NAME, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date, amount, category, description])

        messagebox.showinfo("Success", "Expense added successfully!")
        
        # Clear inputs
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        
        self.load_expenses()

    def load_expenses(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with open(FILE_NAME, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if row:
                        self.tree.insert("", "end", values=row)
        except FileNotFoundError:
            pass

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an expense to delete!")
            return

        if messagebox.askyesno("Confirm Delete", "Delete selected expense?"):
            # Get all rows except selected
            all_rows = []
            with open(FILE_NAME, 'r') as f:
                reader = csv.reader(f)
                all_rows = list(reader)

            # Write back without selected row(s)
            with open(FILE_NAME, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(all_rows[:1])  # Write header
                
                # Get values of selected items
                selected_values = [self.tree.item(item)['values'] for item in selected]
                
                for row in all_rows[1:]:
                    if row not in selected_values:
                        writer.writerow(row)

            self.load_expenses()
            messagebox.showinfo("Deleted", "Selected expense(s) deleted.")

    def show_summary(self):
        total = 0.0
        category_total = {}

        try:
            with open(FILE_NAME, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if row:
                        amount = float(row[1])
                        total += amount
                        cat = row[2]
                        category_total[cat] = category_total.get(cat, 0) + amount
        except:
            messagebox.showinfo("Summary", "No expenses found!")
            return

        summary_text = f"💰 Total Expenses: ₹{total:.2f}\n\nBy Category:\n"
        for cat, amt in sorted(category_total.items(), key=lambda x: x[1], reverse=True):
            summary_text += f"• {cat}: ₹{amt:.2f}\n"

        messagebox.showinfo("Expense Summary", summary_text)


# =============== RUN THE APP ===============
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()