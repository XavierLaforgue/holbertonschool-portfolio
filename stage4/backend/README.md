Access the database with
```
psql -U myuser -d mydb -h localhost
```

The three-step guide to making model changes:
- Change your models (in `models.py`).
- Run `python manage.py makemigrations` to create migrations for those changes
- Run `python manage.py migrate` to apply those changes to the database.

Create superuser for admin panel
```
python manage.py createsuperuser
```

Launch django server with 
```
python manage.py runserver
```

Create or update requirements.txt
```
pip freeze > requirements.txt
```
Install dependencies
```
pip install -r requirements.txt
```
Activate environment
```
source .venv/bin/activate
```