from settings import *
from datetime import datetime
import json

# Initializing our database
db = SQLAlchemy(app)

class Issue(db.Model):
    __tablename__ = 'issues'  # creating a table name
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    #date = db.Column(db.String(20), nullable=False, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    title = db.Column(db.String(80), nullable=False)
    details = db.Column(db.String(80), nullable=False)

    def json(self):
        return {'id': self.id, 'title': self.title, 'details': self.details}

    def add_issue(_title, _details):
        '''add issue to database using _title, _details as parameters'''
        # creating an instance of our Issue constructor
        new_issue = Issue(title=_title, details=_details)
        db.session.add(new_issue)  # add new Issue to database session
        db.session.commit()  # commit changes to session

    def get_all_issues():
        '''get all issues in our database'''
        return [Issue.json(issue) for issue in Issue.query.all()]

    def get_issue(_id):
        '''get issue using the id as parameter'''
        return [Issue.json(Issue.query.filter_by(id=_id).first())]

    def update_issue(_id, _title, _details):
        '''update an issue'''
        issue = Issue.query.filter_by(id=_id).first()
        #issue.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        issue.title = _title
        issue.details = _details
        db.session.commit()

    def delete_issue(_id):
        '''delete a issue from our database'''
        Issue.query.filter_by(id=_id).delete()
        # filter issue by id and delete
        db.session.commit()
