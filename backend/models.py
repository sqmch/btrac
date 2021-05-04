from settings import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

# Initializing our database
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    projects = db.relationship("Project", backref="user")

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method="sha256")

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
        )


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    issues = db.relationship("Issue", backref="project")

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "issues": self.issues,
        }

    def add_project(_title, _user):
        """add new project to database"""
        new_project = Project(title=_title, user=_user)
        db.session.add(new_project)
        db.session.commit()

    def get_all_projects(_user):
        """get all projects in our database"""
        return [
            Project.json(project)
            for project in Project.query.filter_by(user=_user).all()
        ]


class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer, primary_key=True)
    # date = db.Column(db.String(20), nullable=False, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    title = db.Column(db.String(80), nullable=False)
    details = db.Column(
        db.String(1000), nullable=False
    )  # More detailed description of the issue
    status = db.Column(db.String(20), default="Open")  # Open, In Progress, Resolved
    priority = db.Column(db.String(20), default="Low")  # Low, Medium, High
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "status": self.status,
            "priority": self.priority,
        }

    def add_issue(_title, _details, _status, _priority, _project):
        """add new issue to database"""
        # creating an instance of our Issue constructor
        new_issue = Issue(
            title=_title,
            details=_details,
            status=_status,
            priority=_priority,
            project=_project,
        )
        db.session.add(new_issue)  # add new Issue to database session
        db.session.commit()  # commit changes to session

    def get_all_issues(_project_id):
        """get all issues in our database"""
        return [
            Issue.json(issue)
            for issue in Issue.query.filter_by(project_id=_project_id).all()
        ]

    def get_issue(_id):
        """get issue using the id as parameter"""
        return [Issue.json(Issue.query.filter_by(id=_id).first())]

    def update_issue(_id, _title, _details, _status, _priority):
        """update an issue"""
        issue = Issue.query.filter_by(id=_id).first()
        # issue.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        issue.title = _title
        issue.details = _details
        issue.status = _status
        issue.priority = _priority
        db.session.commit()

    def delete_issue(_id):
        """delete an issue from our database"""
        Issue.query.filter_by(id=_id).delete()
        # filter issue by id and delete
        db.session.commit()
