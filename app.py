from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

FILE_NAME = "expenses.csv"

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Amount", "Category", "Description"])
        from flask import render_template
import csv
import os

@app.route("/")
def home():
    expenses = []

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", newline="") as f:
            reader = csv.reader(f)

            # Skip header row safely
            next(reader, None)

            for row in reader:
                expenses.append(row)

    return render_template(
        "index.html",
        expenses=expenses
    )
   from flask import 
import csv

@app.route("/add", methods=["POST"])
def add_expense():
    date = request.form.get("date")
    amount = request.form.get("amount")
    category = request.form.get("category")
    description = request.form.get("description")

    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            date,
            amount,
            category,
            description
        ])

    return redirect(url_for("home"))

    return redirect("/")
    if __name__ == "__main__":
    app.run(debug=True)