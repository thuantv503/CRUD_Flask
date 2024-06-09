# Import libraries
from flask import Flask, redirect, request, render_template, url_for
app = Flask(__name__)
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation: List all transactions
@app.route("/")
def get_transactions():
    total_balance = 0
    for transaction in transactions:
        total_balance = total_balance + float(transaction['amount'])
    return render_template("transactions.html", transactions=transactions, total_balance=total_balance)


@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        transation = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transation)
        return redirect(url_for("get_transactions"))
    return render_template("form.html")

@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = request.form['amount']

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
        return redirect(url_for("get_transactions"))

    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

@app.route("/search", methods=["GET", "POST"])
def search_transaction():
    if request.method == "POST":
        filtered_transactions = []
        for transaction in transactions:
            if float(transaction['amount']) > float(request.form['min_amount']) and float(transaction['amount']) < float(request.form['max_amount']):
                filtered_transactions.append(transaction)
        return render_template("transactions.html", transactions=filtered_transactions)

    return render_template("search.html")


if __name__ == "__main__":
    app.run(debug=True)
