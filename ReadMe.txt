Встановлення системи.
1. Python 2.7
	1.1. Ubuntu: входить в поставку
	1.2. Windows: http://mirkobonadei.wordpress.com/2010/01/25/install-python-and-django-on-windows/
2. Django 1.4
	2.1. Ubuntu: sudo apt-get install python-django
	2.2. Windows: http://mirkobonadei.wordpress.com/2010/01/25/install-python-and-django-on-windows/

3. REST Framework
	pip install djangorestframework
	P.S. sudo apt-get install python-pip

3.1. Користування API
3.1.1. Через браузер
Заходити по силці http://localhost:8000/api/
Клацнути Log in(http://localhost:8000/api-auth/login/?next=/api/)
Ввести логін і пароль
Далі по http://localhost:8000/api/ будуть доступні основні функції(зараз 3 для тесту):
{
    "writers": "http://localhost:8000/api/writers/", 
    "stories": "http://localhost:8000/api/stories/", 
    "user": "http://localhost:8000/api/user/"
}
Якщо даних багато - відображаються по 10 на сторінці.

3.2.2. Програмно
Для отримання чистої json-відповіді потрібно дописувати в кінці “?format=json”, наприклад:
	http://localhost:8000/api/stories/?format=json
сам запит(з консолі) може виглядати наступним чином:
curl -u username:password http://localhost:8000/api/user/?format=json
Для створення нового користувача-адміна заходимо в папку socialstory і вводимо:
python manage.py createsuperuser
Далі все логічно зрозуміло.

Перед запуском потрібно вказати дані про локальну базу даних. В файлі socialstory/source/settings.py міняємо кусок коду на зручну вам бд. В мене PostgreSQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'socialstory',                      # Or path to database file if using sqlite3.
        'USER': 'Detonavomek',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

Далі заходимо з консолі в папку socialstory/
Вводимо: python manage.py syncdb для синхронізації з базою даних.
Вводимо: python manage.py runserver [port] - якщо порт не вказати, то проект буде на  localhost:8000