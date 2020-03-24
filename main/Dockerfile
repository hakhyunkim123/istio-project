FROM python:latest

COPY ./mainpage_proj /usr/src/app

EXPOSE 8000

WORKDIR /usr/src/app

RUN pip install django
RUN pip install requests
#RUN pip install djangorestframework
RUN pip install whitenoise
RUN pip install channels
RUN pip install channels-redis
RUN pip install jwcrypto

CMD ["python", "manage.py", "makemigrations", "mainpage"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "collectstatic", "--no-input"]
CMD ["python", "manage.py", "runserver", "0:8000"]
