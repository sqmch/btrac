# trvcker - a simple issue tracker

## Built with

- Python (Flask, sqlite with SQLAlchemy)
- Vue.js (Vuetify)

### Demo: https://trvcker.netlify.app/
Frontend hosted on Netlify, backend hosted on Heroku.

## About the project

This is a practice project with the goal of further exploring SQLAlchemy, relational databases, JWT authentication, Vue.js, drag and drop functionality and full stack development in general.  trvcker allows the user to create an account, create projects and add issues/tasks to a project for easy tracking.

## How to run in development

Install frontend dependencies:
```
npm install
```
Run in root directory:
```
npm run serve
```

Create a virtual environment in .\backend and activate it:
```
cd backend
python -m venv venv
.\venv\Scripts\activate
```
Install backend dependencies:
```
pip install -r requirements.txt
```
Create the db tables for the default sqlite example (run in python interpreter):
```
>>> from models import db
>>> db.create_all()
```
Run the flask server
```python
python api.py
```
