from flask.globals import current_app
from settings import app
from models import db, Issue, User, Project
from flask import request, redirect, Response, jsonify
from datetime import datetime, timedelta
from functools import wraps
import jwt


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split()

        invalid_msg = {
            "message": "Invalid token",
            "authenticated": False,
        }
        expired_msg = {
            "message": "Expired token",
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
    try:

        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(user.to_dict()), 500
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
            "exp": datetime.utcnow() + timedelta(minutes=10),
        },
        current_app.config["SECRET_KEY"],
    )
    return jsonify({"token": token.decode("UTF-8")})


# route to get all projects
@app.route("/projects", methods=["GET"])
@token_required
def get_projects(current_user):
    """Returns all projects in the db"""

    return jsonify({"Projects": Project.get_all_projects(current_user)})


# route to add new issue
@app.route("/projects", methods=["POST"])
@token_required
def add_project(current_user):
    """Adds new project to db"""
    request_data = request.get_json(force=True)  # getting data from client
    Project.add_project(request_data["title"], current_user)
    response = Response("Project added", 201, mimetype="application/json")
    return response


# route to update issue with PUT method
@app.route("/projects/<int:id>", methods=["PUT"])
@token_required
def put_project(current_user, id):
    """Edits project in the db"""
    request_data = request.get_json(force=True)
    Project.update_project(
        id,
        request_data["title"],
    )
    response = Response("Project updated", status=200, mimetype="application/json")
    return response


# route to delete project using the DELETE method
@app.route("/projects/<int:id>", methods=["DELETE"])
@token_required
def remove_project(current_user, id):
    """Deletes project from the db"""
    Project.delete_project(id)
    response = Response("Project deleted", status=200, mimetype="application/json")
    return response


#######

# route to update project issue order
@app.route("/projects/<int:id>", methods=["PUT"])
@token_required
def update_order(current_user, id):
    """Edits project issue order"""
    request_data = request.get_json(force=True)
    Project.update_order(
        id,
        request_data["order"],
    )
    response = Response(
        "Project order updated", status=200, mimetype="application/json"
    )
    return response


# route to get project issue order
@app.route("/projects/<int:id>", methods=["GET"])
@token_required
def get_project_issue_order(current_user, id):
    """Returns project issue order"""
    return jsonify({"order": str(Project.get_project_issue_order(current_user, id))})


#######

# route to return issue table of specified project
@app.route("/projects/<int:id>/issues", methods=["GET"])
@token_required
def get_issues_of_project(current_user, id):
    """Returns issues of specified project"""
    return jsonify({"Issues": Issue.get_all_issues(id)})


# route to add new issue
@app.route("/projects/<int:id>/issues", methods=["POST"])
@token_required
def add_issue(current_user, id):
    """Adds new issue to db"""
    request_data = request.get_json(force=True)  # getting data from client
    # project = current_user.projects.filter_by(id=id).first()
    project = Project.query.get(id)
    Issue.add_issue(
        request_data["title"],
        request_data["details"],
        request_data["status"],
        request_data["priority"],
        project,
    )
    response = Response("Issue added", 201, mimetype="application/json")
    return response


# route to update issue with PUT method
@app.route("/issues/<int:id>", methods=["PUT"])
@token_required
def put_issue(user, id):
    """Edits issue in the db"""
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
def remove_issue(user, id):
    """Deletes issue from the db"""
    Issue.delete_issue(id)
    response = Response("Issue deleted", status=200, mimetype="application/json")
    return response


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    redirect("/issues")


if __name__ == "__main__":
    app.run(port=1234, debug=True)
