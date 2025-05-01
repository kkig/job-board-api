# Job Board API

## Project overview
WIP

## Tech Stack
- Python - Language used for this project
- Django - Core Framework
- PostgreSQL - SQL DB

## Set Database (PostgreSQL)
1. [Download PostgreSQL](https://www.postgresql.org/download/)
2. Start databse (ex. `brew services start postgresql`)
3. Connect to database
    ```
    psql postgres
    ```
4. Create database
    ```
    postgres=# CREATE DATABASE mydatabase;
    ```
5. Create user
    ```
    postgres=# CREATE USER myuser WITH PASSWORD 'mypassword';
    ```
6. Grant access to user
    ```
    postgres=# GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
    ```
7. Exit
    ```
    postgres=# \q
    ```
8. Create Superuser & Migrate
    ```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```

## Set App
1. Clone this repo
2. Run commands below

## Features
WIP