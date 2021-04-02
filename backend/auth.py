from flask import  redirect

@auth.route('/login')
def login():
    return "login"

@auth.route('/signup')
def signup():
    return "Signup"

@auth.route('/logout')
def logout():
    return 'Logout'
