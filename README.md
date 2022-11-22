# talking-python-api



## Getting started

Hello. We will create project that maintain public api. So, we will use django-rest-framework for back-end. Then we will
use swagger as a utils for testing our api.

## First steps

- Clone this repo
- Download and install python >= 3.10
- Then create virtual env it needs for your work. If you use pycharm, you can add new interpreter in settings for existing project. Or you can do it in terminal, just use this commands:
```
python3 -m venv .
source ./venv/bin/activate.
```
- Then install all requirements from requirements.txt:
```
pip install -r ./requirements.txt
```

## Migrations
Creating a model in db and synching it for the first time
```
python manage.py makemigrations <model_folder>
python manage.py migrate <model_folder>
```

## Json body for POST
An example of a valid json body for a POST request looks like this:
```
{
    "users":[
        {
        "first_name": "Mike",
        "last_name": "Kedzierski"
        },
        {
        "first_name": "Ayaan",
        "last_name": "Badawi"
        }
    ]
}
```