# BOLD project

This document aim to help the installation on both API and UI project for the **BOLD CHALLANGE 2021**.

Credentials to access the Django admin
- **Username**: bold
- **Password**: devoteam

Bearer Authentication faked on database
- Bearer 1PgxQwoSV3HHuR3eSuM6YLDxVB3QBU

##### API
- Running (docker) on 8000 http://localhost:8000
- Python
- Django

##### Angular 11
- Running (docker) on 8080 http://localhost:8080
- Angular project with static already compiled on /dist

## API instalation

- Initialize docker images running the command
```docker-compose up --build```
- All configuration is made on docker scripts, like feed database with initial data.
- Access the Django admin using the [link](http://127.0.0.1:8000/admin/)
- Access the api using the [link](http://127.0.0.1:8000/swagger/)

## UI instalation

- The UI was made on Angular, but the project was already compiled on /dist and is being serve by nginx on the 8080 port.
- Go to /{root_project}/angular
- Initialize docker images running the command
- ```docker-compose up --build```
- Access the UI using the [link](http://127.0.0.1:8080)

## API Tests
 - To running the massive **2** unit tests on the API, run the command
  ```python manage.py tests```

## Postman collection
- Import the Postman collection with all needed request on
- ```{{root_dir}}/Postman/BOLD.postman_collection.json```