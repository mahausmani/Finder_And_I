# 🧭 Finder And I 🔍 

This is a simple application that helps you locate your friends on campus.

It is built using Django

# Contents
- [Getting Started](#getting-started)
     - [Installation](#installation)

# Getting Started
## Requirements
The website requires Python 3.10 or later. It also requires the following packages:
```bash
contourpy==1.2.0
crispy-bootstrap4==2023.1
Django==5.0
django-crispy-forms==2.1
matplotlib==3.8.2
numpy==1.26.3
pillow==10.2.0
sqlparse==0.4.4
```

## Installation
- clone the repository
- go to the path where your manag.py file is (dashboard)
- create a virtual environment using `python3 -m venv venv`
- activate the virtual envirenment using `source venv/bin/activate`
- run `pip install -r requirements.txt`
- make migrations `python3 manage.py makemigrations` 
- run migrations `python manage.py migrate`
- create a super user `python manage.py createsuperuser`
- Now you can run the server to see the app running `python manage.py runserver`
