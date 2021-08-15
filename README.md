# FSND-Casting-Agency

Udacity Full Stack Nanodegree capstone project - Casting Ageny

## Motivation

This project is the capstone project for `Udacity Full Stack web development nanondegree`.

This project covers all the learnt concepts that were covered by the nanodegree which includes data modeling for web using `postgres`, API development and testing with `Flask`, Authorization with RBAC, `JWT` authentication and finally API deployment using `Heroku`.

## Start the project locally

This section will introduce you to how to run and setup the app locally.

### Dependencies

This project is based on `Python 3` and `Flask`.

To install project dependencies:

```bash
$ pip install -r requirements.txt
```

Note: you must have the latest version of Python 3

### Local Database connection

- You need to install and start `postgres` database.
- You need to update the database_params variable found in `config.py` file as shown below:

```python
database_param = {
    "username": "postgres",
    "password": "YOUR_DB_PASSWORD",
    "db_name": "capstone",
    "dialect": "postgresql"
}
```

Note: you can create a db named `capstone` by using `createdb` command as shown below:


**Permissions**:
  ```code
    - Assitant:
        - `view:genres`
        - `view:actors`
        - `view:movies`
    - Director:
        - All permissions of assistant
        -  `add:actors`
        -  `delete:actors`
        -  `patch:actors`
        -  `patch:actors`
        -  `patch:actors`
    - Executive Producer:
        - All permissions of director
        - `add:genres`
        - `add:movies`
        - `delete:genres`
        - `delete:movies`
  ```

  **To testing API, I`ve prepared three accounts**:
  ```code
    - Assistant account:
        - **email**: udacityjon@mail.ru
    - Director account:
        - **email**: muvaffaqiyat12@mail.ru
    - Executive Producer:
        - **email**: intelligent_7404@gmail.ru
    - Password🔑:
        - **Boburshoh777!**
  ```

## Login🔐 to accounts*:
### To `login/signup` you should go to the page: [login/signup](https://capstone-7404.us.auth0.com/authorize?

### After `login/signup` get token from url, this token is used to send requests to API endpoints
### Let's decode jwt, to decode jwt navigate to jwt.io website
### To logout, naviagte to page: https://capstone-7404.us.auth0.com/logout

# Testing
* ⚠ First of all ran all commands in Run application section!
* ⚠ Firstly you should create database for API testing and change database_path on ` test_app.py ` file, and setup environment variables

## First method: unittest
1. **Run the following comands:**
```bash
        python3 manage.py runtests
```

## Endpoints
```
# Movies

GET '/movies'
POST '/movies'
PATCH '/movies/<id>'
DELETE '/movies/<id>'

GET '/movies'
- Fetches all movies on the platform
- Request Arguments: None
- Allowed users: Executive Producer, Casting Assistant and casting Director
- Required permission (get:movies)
- Response
{
  "movies": [
    {
      "id": 3,
      "release_date": "Thu, 23 Jun 2005 00:00:00 GMT",
      "title": "A fall from Grace"
    },
    {
      "id": 1,
      "release_date": "Thu, 28 Jun 2000 00:00:00 GMT",
      "title": "Jumanji"
    }
  ],
  "success": True
}

POST '/movies'
- Creates a new movie with the provided parameters
- Request Arguments: None
- Allowed users: Executive Producer
- Required permission (add:movies)
- Request Body: {
	"title": "Slap of the Century"
	"release_date": "2/26/1996"
}

- Response
{
  "movie": {
    "id": 4,
    "release_date": "Mon, 26 Feb 1996 00:00:00 GMT",
    "title": "Slap of the Century"
  },
  "success": true
}


PATCH '/movies/<id>'
- Updates a specific movie with the provided parameters
- Request Arguments: movie_id (The ID of the movie to update)
- Allowed users: Executive Producer, Casting Director
- Required permission (edit:movies)
- Request Body: {
	"title": "Silicon Valley"
}

- Response
{
  "movie": {
    "id": 4,
    "release_date": "Thu, 26 Feb 2004 00:00:00 GMT",
    "title": "Silicon Valley"
  },
  "success": true
}

DELETE '/movies/<id>'
- Deletes a specific movie
- Request Arguments: movie_id (The ID of the movie to delete)
- Allowed users: Executive Producer
- Required permission (delete:movie)
- Response
{
  "delete": id,
  "success": true
}



# Actors

GET '/actors'
POST '/actors'
PATCH '/actors/<id>'
DELETE '/actors/<id>'

GET '/actors'
- Fetches all actors on the platform
- Request Arguments: None
- Allowed users: Executive Producer, Casting Assistant and casting Director
- Required permission (get:actors)
- Response
{
  "actors": [
    {
      "age": 25,
      "gender": "male",
      "id": 3,
      "name": "Kevin Hart"
    },
    {
      "age": 20,
      "gender": "male",
      "id": 1,
      "name": "Desmond Elliot"
    }
  ],
  "success": true
}

POST '/actors'
- Creates a new actor with the provided parameters
- Request Arguments: None
- Allowed users: Executive Producer and casting Director
- Required permission (add:actors)
- Request Body: {
	"name": "Kunle Afolayan",
	"age": 20,
	"gender": "male"
}

- Response
{
  "actor": {
    "age": 20,
    "gender": "female",
    "id": 4,
    "name": "Kunle Afolayan"
  },
  "success": true
}


PATCH '/actors/<id>'
- Updates a specific actor with the provided parameters
- Request Arguments: actor_id (The ID of the actor to update)
- Allowed users: Executive Producer and Casting Director
- Required permission (edit:actor)
- Request Body: {
	"name": "RMD",
}

- Response
{
  "actor": {
    "age": 28,
    "gender": "female",
    "id": 4,
    "name": "RMD"
  },
  "success": true
}

DELETE '/actors/<id>'
- Deletes a specific actor
- Request Arguments: actor_id (The ID of the actor to delete)
- Required permission (delete:actors)
- Response
{
  "delete": id,
  "success": true
}

Errors 
For errors, the server returns a json object with a description of the type of error. Find the description below:

400 (Bad Request)
  {
    "success": False, 
    "error": 400,
    "message": "bad request, please check your input"
  }

401 (Unauthorised)
  {
    "success": False, 
    "error": 401,
    "message": "authorisation error"
  }



404 (Resource Not Found)
  {
    "success": False, 
    "error": 404,
    "message": "resource not found"
  }



422 (Unprocessable entity)
  {
    "success": False, 
    "error": 422,
    "message": "unprocessable"
  }

500 (Internal server error)
  {
    "success": False, 
    "error": 500,
    "message": "Server error
  }
```
