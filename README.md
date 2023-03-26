# Semantus Django Server
This is the Django server that belongs to Semantus. Once it is finished, it is supposed to serve a website, an Android app as well as an iOS app by providing an API that allows user authentication, a database of registered users, a database of in-game friends, and more. 

## Setup
To work with this repository, all required Python packages have to be installed. For this purpose, we provide `requirements.txt`. It contains all required packages and modules to successfully run the server. Use `pip install -r requirements.txt` to install all required packages. 

## Running the server
Use `python manage.py makemigrations` and `python manage.py migrate` to create database tables from models defined in `models.py`. Use `python manage.py runserver` to run the server.
