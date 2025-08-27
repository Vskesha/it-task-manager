# Task Manager for IT Company

Django project for project management

## Check it out 
Deployed at [it-task-manager-bttq.onrender.com/](https://it-task-manager-bttq.onrender.com/)


You can test:
```
login: test_user
password: Pass123456
```

## Installation

Python3 must be already installed

```shell
git clone https://github.com/Vskesha/it-task-manager.git
cd it-task-manager
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

## Features

* Authentication functionality for User
* Manage tasks and workers directly from website.
* The superuser has full access. They can create positions, workers, tasks, delete workers, delete tasks, and edit the task deadline.
* An employee has partial access can create tasks, select tasks, and mark completed tasks.

## Demo
![Dashboard Interface](demo_dashboard.png)
![Login page](demo_login.png)
