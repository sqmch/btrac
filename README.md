# trvcker - a simple issue tracker

## Built with

- Python (Flask)
- Vue.js (Vuetify)


## About the project

This is a practice project with the goal of further exploring SQLAlchemy, relational databases, JWT authentication and full stack development in general.  trvcker allows the user to create an account, create projects and add issues to a project for easy tracking. Issues have a status and priority levels and can be added/removed/edited with ease.

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
Run the flask server
```python
python api.py
```
