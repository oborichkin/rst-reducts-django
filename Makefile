serve:
	pipenv run ./manage.py runserver

migrate:
	pipenv run ./manage.py migrate

freeze:
	pipenv run pip freeze > requirements.txt