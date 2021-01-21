# deadlock-server

This API is developed using [FastAPI](https://fastapi.tiangolo.com/).

### How to setup locally

#### Python version and requirements
Create a `python3.7` virtual enviroment and activate it.
Install requirements using `pip install -r requirements.txt`. 

#### Starting a DB and providing testing data
Start a Postgres server locally. Create a database called `test` owned by user `test`.
Now let's fill the data from `fixtures.sql` into the database. Run those from terminal:
```
su test
psql
```
The Postgres console should start up. Execute those commands in it to reset it:
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```
Exit Postgres console.
Now run `python main.py` to let it create tables.
After a few seconds, `main.py` should finish creating tables. Let's fill testing
data into the database:
```
psql -f fixtures.sql
```

#### Run the server
```
uvicorn main:app --reload
```

### How to print logs
```python
import logging
logger = logging.getLogger(__name__)
logger.warning("Hi")
```

## Interaction with API

### Superuser

Most endpoints require superuser rights. There is a staff user with username
`stlpik` and password `secret`. It was inserted into the database from `fixtures.sql`.
This user should be allowed to fully interact with the API. 

### How to get access token (jwt)
Send `POST` request to `/token` with body like:
```json
{
        "username": "name",
        "password": "verysecretpassword"
}
```

### Other endpoints

There is and interactive documentation generated by `FastAPI` accessible on `http://localhost:8000/docs`.
It is possible to send requests and receive responses directly from the docs for testing
and debugging purposes. 

#### `[GET] /users`
Returns list of users in json format:
```json
{
  "users": [
    {
      "username": "stlpik",
      "first_name": "Meno",
      "is_staff": true,
      "disabled": false,
      "updated": "2020-12-18T18:27:34.783243",
      "id": 1,
      "card": "1234567891011",
      "last_name": "Priezvisko",
      "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
      "created": "2020-12-18T18:27:34.783243"
    },
    {
      "username": "stud",
      "first_name": "Meno",
      "is_staff": false,
      "disabled": false,
      "updated": "2020-12-18T18:27:34.783243",
      "id": 2,
      "card": "1234567891011",
      "last_name": "Priezvisko",
      "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
      "created": "2020-12-18T18:27:34.783243"
    }
  ]
}
```

#### `[POST] /users`
Adds a new user to the database. Fields username and card are unique.
Request body example:
```json
{
  "card": "9876543210",
  "username": "newusername",
  "first_name": "SomeFirst",
  "last_name": "SomeLast",
  "is_staff": true
}
```
Corresponding response body example:
```json
{
  "card": "9876543210",
  "username": "newusername",
  "first_name": "SomeFirst",
  "last_name": "SomeLast",
  "is_staff": true,
  "id": "6",
  "disabled": false,
  "groups": [],
  "created": "2021-01-21T14:32:53.699616",
  "updated": "2021-01-21T14:32:53.699616"
}
```

#### `[GET] /users/me`
Gets current user.

#### `[GET] /groups`
Returns list of all groups like this:
```json
{
  "groups": [
    {
      "name": "LinuxPP",
      "updated": "2021-01-21T14:05:28.812339",
      "created": "2021-01-21T14:05:28.812339",
      "id": 1
    },
    {
      "name": "SkupinaNejaka",
      "updated": "2021-01-21T16:01:27.324223",
      "created": "2021-01-21T16:01:27.324223",
      "id": 2
    }
  ]
}
```

#### `[POST] /groups`
Creates a group.
Request example:
```json
{
  "name": "newgroup"
}
```
Response example:
```json
{
  "id": 0,
  "name": "newgroup",
  "rules": []
}
```
where `rules` contains ids of rules that are applied for this group, which is initially
empty after creating the group.

#### `[GET] /groups/{group_id}`
Gets list of users belonging to group with id `{group_id}`.
Example response to `GET` from `/groups/2`:
```json
{
  "group_id": 2,
  "users": [
    {
      "username": "stlpik",
      "first_name": "Meno",
      "is_staff": true,
      "disabled": false,
      "updated": "2021-01-21T14:05:28.795202",
      "id": 1,
      "card": "1234567891011",
      "last_name": "Priezvisko",
      "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
      "created": "2021-01-21T14:05:28.795202"
    },
    {
      "username": "stud",
      "first_name": "Meno",
      "is_staff": false,
      "disabled": false,
      "updated": "2021-01-21T14:05:28.795202",
      "id": 2,
      "card": "1234567891012",
      "last_name": "Priezvisko",
      "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
      "created": "2021-01-21T14:05:28.795202"
    }
  ]
}
```

#### `[POST] /usergroup/add`
Adds a user with with id `user_id` to the group with id `group_id`.
Just make `POST` request to address like `/usergroup/add/?user_id=3&group_id=1`.

Success response looks like:
```json
{
  "id": 5,
  "user_id": 3,
  "group_id": 1
}
```

#### `[POST] /rules/add`
Adds a rule. Does not assign it to groups yet.
Example request:
```json
{
  "name": "somerulename",
  "allow": true,
  "time_spec_id": 7,
  "ap_type_id": 1,
  "priority": 6
}
```

Success response example: TODO
