from settings import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

# Initializing database
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    projects = db.relationship("Project", lazy="dynamic", backref="user")

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
    order = db.Column(db.String())

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "order": self.order,
        }

    def add_project(_title: str, _user):
        """Add new project to database"""
        new_project = Project(title=_title, user=_user)
        db.session.add(new_project)
        db.session.commit()

    def get_all_projects(_user):
        """Get all projects from database"""
        return [
            Project.json(project)
            for project in Project.query.filter_by(user=_user).all()
        ]

    def update_project(_id: int, _title: str):
        """Update a project"""
        project = Project.query.filter_by(id=_id).first()
        project.title = _title
        db.session.commit()

    def update_order(_id: int, _order: str):
        """Update project issue order"""
        project = Project.query.filter_by(id=_id).first()
        project.order = str(_order)
        print(f"project.order {project.order}")
        db.session.commit()

    def get_project_issue_order(_user: User, _id: int):
        """Returns project issue order"""
        issue_order = Project.json(Project.query.filter_by(user=_user, id=_id).first())[
            "order"
        ]
        print(f"issue_order - {issue_order}")
        return issue_order

    def delete_project(_id: int):
        """Delete a project from the database"""
        Project.query.filter_by(id=_id).delete()
        db.session.commit()


class Issue(db.Model):
    __tablename__ = "issues"
    id = db.Column(db.Integer, primary_key=True)
    # date = db.Column(db.String(20), nullable=False, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    title = db.Column(db.String(80), nullable=False)
    details = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.String(20), default="Open")
    priority = db.Column(db.String(20), default="Low")
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "status": self.status,
            "priority": self.priority,
        }

    def add_issue(_title: str, _details: str, _status: str, _priority: str, _project):
        """Add new issue to database"""
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
        """Get all issues in database"""
        return [
            Issue.json(issue)
            for issue in Issue.query.filter_by(project_id=_project_id).all()
        ]

    def get_issue(_id):
        """Get issue using the id"""
        return [Issue.json(Issue.query.filter_by(id=_id).first())]

    def update_issue(
        _id: int, _title: str, _details: str, _status: str, _priority: str
    ):
        """Update an issue"""
        issue = Issue.query.filter_by(id=_id).first()
        # issue.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        issue.title = _title
        issue.details = _details
        issue.status = _status
        issue.priority = _priority
        db.session.commit()

    def delete_issue(_id: int):
        """Delete an issue from database"""
        Issue.query.filter_by(id=_id).delete()
        # filter issue by id and delete
        db.session.commit()
