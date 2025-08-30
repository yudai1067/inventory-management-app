FROM python:3.13.6
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev && rm -rf /var/lib/apt/lists/*

COPY ./app .

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]