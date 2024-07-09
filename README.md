# README #

### What is this service for? ###

* Spam recognition service - for light weight API server

### Dependencies ###
* External
    - Django
    - djangorestframework
    - djangorestframework_simplejwt
    - rest_framework_simplejwt
    - psycopg2
    - psycopg2-binary

### Prerequisites
* Docker should be installed
* Python should be installed

### Docker commands
* Run the server `docker-compose up -d --build`
* To monitor logs `docker-compose logs -f --tail 1000 spam_recognition_service`

### Docker Containers
* spam_recognition_service
* db

### How to run tests?
* `docker exec -it spam_recognition_service-spam_recognition_service-1 bash`
* `cd /spam_recognition_service`
* `python3 manage.py test api/tests`

### How to populate global db data?
* `docker exec -it spam_recognition_service-spam_recognition_service-1 bash`
* `cd /spam_recognition_service`
* `python3 script_to_populate_db.py`

### How to view the table using django admin?
* `docker exec -it spam_recognition_service-spam_recognition_service-1 bash`
* `cd /spam_recognition_service`
* `python3 manage.py createsuperuser`
* Enter admin username, email id and password
* Open `http://localhost:8000/admin/` to view the table

### How to bring the docker down?
* `docker-compose down`

### How to run this locally?
* Make the DATABASE variable in the settings.py to point to local
<!-- # DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# } --> 
* `python3 manage.py makemigrations api`
* `python3 manage.py migrate`
* `python3 manage.py runserver 0.0.0.0:8000`



