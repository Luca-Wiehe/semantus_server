# Semantus Django Server

This is the Django server that belongs to Semantus. Once it is finished, it is supposed to serve a website, an Android app as well as an iOS app by providing an API that allows user authentication, a database of registered users, a database of in-game friends, and more.

## Setup

To work with this repository, all required Python packages have to be installed. For this purpose, we provide `requirements.txt`. It contains all required packages and modules to successfully run the server. Use `pip install -r requirements.txt` to install all required packages.

If you use a virtual environment created with conda, make sure to use the pip instance from your virtual environment. In many cases, Python will try to use the global environment despite the fact that a conda environment is activated. For Mac, explicitly specify the location of your virtual environment pip:

```
conda create semantus_env
conda activate semantus_env
conda install pip
~/opt/anaconda3/envs/semantus_env/bin/pip install -r requirements.txt
```

## Running the server

To run the server run the following commands in the project directory:

```
python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```
