./manage.py makemigrations
./manage.py makemigrations orders
./manage.py migrate
./manage.py collectstatic --noinput
./manage.py runserver 0.0.0.0:8000