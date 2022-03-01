# DemoTrading

## Run (normal)

1) `cp .env-sample .env` and paste variables with your own.
2) ``` pip install -r requirements.txt ```
3) ``` ./manage.py makemigrations && ./manage.py migrate && ./manage.py migrate --run-syncdb && ./manage.py runserver ```

## Run (docker)

Just run this command: `docker-compose up --build`