FROM python:2.7

WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py makemigrations projecthandler
RUN python manage.py migrate

RUN python manage.py shell \
    -c "from sf_user.models import CustomUser; CustomUser.objects.create_superuser('admin', 'admin')"

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

