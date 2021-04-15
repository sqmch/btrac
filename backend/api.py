from settings import *
from models import db, Issue, UserModel

from flask import request, redirect, render_template

# route to get all issues
@app.route("/issues", methods=["GET"])
def get_issues():
    """get all the issues in the database"""
    return jsonify({"Issues": Issue.get_all_issues()})


# route to get issue by id
@app.route("/issues/<int:id>", methods=["GET"])
def get_issue_by_id(id):
    return_value = Issue.get_issue(id)
    return jsonify(return_value)


# route to add new issue
@app.route("/issues", methods=["POST"])
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
def remove_issue(id):
    """Function to delete issue from our database"""
    Issue.delete_issue(id)
    response = Response("Issue deleted", status=200, mimetype="application/json")
    return response


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    redirect("/issues")


if __name__ == "__main__":
    app.run(port=1234, debug=True)
