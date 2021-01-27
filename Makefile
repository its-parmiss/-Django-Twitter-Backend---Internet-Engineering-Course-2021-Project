run:
	python3 ./manage.py makemigrations
	python3 ./manage.py migrate
	python3 ./manage.py runserver  0.0.0.0:8888

add_super_user:
	python ./manage.py createsuperuser

make_migration:
	python3 ./manage.py makemigrations

shell:
	python3 ./manage.py shell
