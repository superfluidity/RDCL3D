FROM python:2.7

WORKDIR /usr/src/app
COPY code .

RUN pip install -r requirements.txt

# fix pbr-based packages versioning
RUN echo "__version__ = '0.0.1'" | tee toscaparser/__init__.py | tee translator/__init__.py
# delete the copy of the database inside the container (if exists)
RUN rm -f db.sqlite3

RUN python manage.py makemigrations sf_user projecthandler deploymenthandler
RUN python manage.py migrate

RUN python manage.py shell \
    -c "from sf_user.models import CustomUser; CustomUser.objects.create_superuser('admin', 'admin')"


EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

