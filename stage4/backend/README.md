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

To schedule token clean up: (syntax of crontab: `<minute(0-59)> <hour(0-23)> <day(1-31)/*(everyday)> <month(1-12)/*(everymonth)> <weekday(0-7)/(everyweekday)> command_to_run`)
```
( crontab -l ; echo "0 2 * * 1 /home/xavier/holbertonschool-portfolio/stage4/backend/.venv/bin/python /home/xavier/holbertonschool-portfolio/stage4/backend/manage.py cleanup_blacklisted_tokens" ) | crontab -
```
