from flask.globals import current_app
from settings import *
from models import db, Issue, User
from flask import request, redirect
from datetime import datetime, timedelta
from functools import wraps
import jwt


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split()

        invalid_msg = {
            "message": "Invalid token. Registeration and / or authentication required",
            "authenticated": False,
        }
        expired_msg = {
            "message": "Expired token. Reauthentication required.",
            "authenticated": False,
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config["SECRET_KEY"])
            user = User.query.filter_by(email=data["sub"]).first()
            if not user:
                raise RuntimeError("User not found")
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@app.route("/register", methods=("POST",))
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.route("/auth", methods=["POST"])
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({"message": "Invalid credentials", "authenticated": False}), 401

    token = jwt.encode(
        {
            "sub": user.email,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=2),
        },
        current_app.config["SECRET_KEY"],
    )
    print(jsonify({"token": token.decode("UTF-8")}))
    return jsonify({"token": token.decode("UTF-8")})


# route to get all issues
@app.route("/issues", methods=["GET"])
@token_required
def get_issues(current_user):
    """get all the issues in the database"""
    return jsonify({"Issues": Issue.get_all_issues()})


# route to get issue by id
@app.route("/issues/<int:id>", methods=["GET"])
@token_required
def get_issue_by_id(id):
    return_value = Issue.get_issue(id)
    return jsonify(return_value)


# route to add new issue
@app.route("/issues", methods=["POST"])
@token_required
def add_issue():
    """add new issue to our database"""
    request_data = request.get_json(force=True)  # getting data from client
    Issue.add_issue(
        request_data["title"],
        request_data["details"],
        request_data["status"],
        request_data["priority"],
    )
    response = Response("Issue added", 201, mimetype="application/json")
    return response


# route to update issue with PUT method
@app.route("/issues/<int:id>", methods=["PUT"])
@token_required
def update_issue(id):
    """edit issue in our database using issue id"""
    request_data = request.get_json(force=True)
    Issue.update_issue(
        id,
        request_data["title"],
        request_data["details"],
        request_data["status"],
        request_data["priority"],
    )
    response = Response("Issue updated", status=200, mimetype="application/json")
    return response


# route to delete issue using the DELETE method
@app.route("/issues/<int:id>", methods=["DELETE"])
@token_required
def remove_issue(id):
    """Function to delete issue from our database"""
    Issue.delete_issue(id)
    response = Response("Issue deleted", status=200, mimetype="application/json")
    return response


"""
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    redirect("/issues")
"""

if __name__ == "__main__":
    app.run(port=1234, debug=True)
