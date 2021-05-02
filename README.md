# Noyo

## Setup

### Prerequisites

1. [Python 3.8 or higher](https://www.python.org/downloads/release/python-380/)
2. [postgresql installed](https://www.codementor.io/@engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb)
3. Two Postgres databases for development and testing. (The databases names assumed below are "noyo" for development and "noyo_test" for testing)

### Steps

-   Make a new python virtualenv `python3 -m venv ENV_NOYO`
-   Activate it `source ENV_NOYO/bin/activate`
-   Update pip `pip3 install --upgrade pip`
-   Install dependencies `pip3 install -r requirements.txt`
-   Export environment variables

```
export DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/noyo
export TESTING_DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/noyo_test
export FLASK_APP=run.py
export APP_SETTINGS=development
export FLASK_ENV=development
```

-   Run app `python3 run.py`
-   To test app `python3 test_app.py`

## Endpoints

### GET /api/person

Fetch a list of all persons (latest version)

URI: `http://localhost:5000/api/person`
Sample Output

```
[
    {
        "email": "email1@email.com",
        "age": 20,
        "first_name": "Valerie",
        "id": "29544879-eb5d-4272-a36e-62085e0e0a97",
        "version": 1,
        "middle_name": "",
        "last_name": "Vasquez",
        "latest": true
    },
    {
        "email": "email2@email.com",
        "age": 5,
        "first_name": "Angela",
        "id": "a8f238a7-bec8-4ceb-8268-a61a6c9ac45b",
        "version": 1,
        "middle_name": "Jay",
        "last_name": "Simone",
        "latest": true
    }
]
```

### GET /api/person/id

Fetch the latest version of a single person using their id

URI: `http://localhost:5000/api/person/29544879-eb5d-4272-a36e-62085e0e0a97`
Sample Output

```
    {
        "email": "email1@email.com",
        "age": 20,
        "first_name": "Valerie",
        "id": "29544879-eb5d-4272-a36e-62085e0e0a97",
        "version": 1,
        "middle_name": "",
        "last_name": "Vasquez",
        "latest": true
    }
```

### GET /api/person/id?version=\<version\>

Fetch a single person using their id and a specified version

URI: `http://localhost:5000/api/person/29544879-eb5d-4272-a36e-62085e0e0a97?version=2`
Sample Output

```
    {
        "email": "email1@email.com",
        "age": 25,
        "first_name": "Valerie",
        "id": "29544879-eb5d-4272-a36e-62085e0e0a97",
        "version": 2,
        "middle_name": "",
        "last_name": "Vasquez",
        "latest": true
    }
```

### POST /api/person

Create a new person

Data for the new person is required. JSON body required

```
{
    "first_name": String | Required,
    "last_name": String | Required,
    "middle_name": String,
    "age": Integer | Required,
    "email": String | Required
}
```

URI: `http://localhost:5000/api/person`
Sample JSON Payload

```
{
    "first_name": "claire",
    "last_name": "zhang",
    "middle_name": "",
    "age": 20,
    "email": "claire@claire.com"
}
```

Sample Output

```
{
    "message": "Person successfully created!",
    "id": "ee52f855-0705-4d3c-8140-646b2951f224"
}
```

### PATCH /api/person/id

JSON body of the request contains the fields and values to update the Person
JSON body required

```
{
    "first_name": String,
    "last_name": String,
    "middle_name": String,
    "age": Integer,
    "email": String
}
```

Update a single person using their id

URI: `http://localhost:5000/api/person/ee52f855-0705-4d3c-8140-646b2951f224`
Sample JSON Payload

```
{
	"email": "email2@email.com"
}
```

Sample Output

```
{
    "message": "Successfully updated person with id: ee52f855-0705-4d3c-8140-646b2951f224"
}
```

### DELETE /api/person/id

Delete a single person using their id

URI: `http://localhost:5000/api/person/ee52f855-0705-4d3c-8140-646b2951f224`
Sample Output

```
{
    "message": "Successfully deleted person with id: ee52f855-0705-4d3c-8140-646b2951f224 and version: 2"
}
```

## Postman

Postman collection URL to import: https://www.getpostman.com/collections/ea5f1ae86ab9b7bf66b3
