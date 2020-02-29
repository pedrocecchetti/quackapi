FROM python:3.7
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt && rm -rf /root/.cache

CMD ["python", "manage.py", "runserver" , "0:8000"]