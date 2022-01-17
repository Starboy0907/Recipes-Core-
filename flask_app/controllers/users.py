from flask_app import app
from flask import Flask, render_template, redirect, session, request
from  flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask import flash

bcrypt = Bcrypt(app)

# Main landing page - contains log/reg
@app.route('/')
def landing():
    return redirect('/login')

@app.route('/login')
def index():
    return render_template('login.html')

# Register route
@app.route('/register', methods=['POST'])
def register():
    isValid = User.validate(request.form)
    if not isValid:
        return redirect('/')
    newUser = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
            }
    id = User.save(newUser)
    if not id:
        flash("Something went wrong!")
        return redirect('/')
    session['user_id'] = id
    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data)
    if not user:
        flash("Invalid Login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Wrong password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# Logout function
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')