from flask import Flask, render_template, redirect, url_for, request

from webservices import ApiCaller

app = Flask(__name__)
api_caller = ApiCaller.ApiCaller()


@app.route('/')
def hello_world():
    return 'Invalid Page'


"""
A Simple login form to validate credentials.

"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'corpuscule' or request.form['password'] != 'corpuscule':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('display_shopping_cart'))
    return render_template('login.html', error=error)


"""
    Method to get the items from the shopping cart
    
"""


@app.route('/shoppingcart', methods=['GET', 'POST'])
def display_shopping_cart():
    error = None
    if request.method == 'POST':
        item_name = request.form['itemname']
        item_amount = request.form['amount']
        item_quantity = request.form['quantity']
        # Here corpuscule should be replaced with the customer id.
        invoice = {"data": {"Corpuscule": {'name': item_name, 'price': item_amount, 'quantity': item_quantity}}}
        metadata = {'Customer ID': 'Customer Name'}
        tx_id = api_caller.submit_transaction(invoice, metadata)
        if tx_id is not None:
            success = tx_id
            return render_template('shopping_cart.html', success=success)
        else:
            error = "Something went wrong."
    return render_template('shopping_cart.html', error=error)


"""
Retrieve the invoice based on the transaction id.

"""


@app.route('/retrieveinvoice', methods=['GET', 'POST'])
def display_invoice_based_on_transaction_id():
    error = None
    if request.method == 'POST':
        transaction_id = request.form['txid']
        invoice_details = api_caller.get_invoice_based_on_transaction_id(transaction_id)
        if invoice_details is not None:
            result = invoice_details
            return render_template("retreive_invoice.html", result=result)
        else:
            error = "The Transaction id is invalid."
    return render_template('retreive_invoice.html', error=error)


if __name__ == '__main__':
    app.run()
