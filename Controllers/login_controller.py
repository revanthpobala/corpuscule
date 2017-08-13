from flask import Flask, render_template, redirect, url_for, request

from webservices import ApiCaller

app = Flask(__name__)
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
