from flask import redirect


@app.route("/login", methods=["GET", "POST"])
def login():
    return "login"


@auth.route("/signup")
def signup():
    return "Signup"


@auth.route("/logout")
def logout():
    return "Logout"
