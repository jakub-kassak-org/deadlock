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

### How to log
Logging configuration is in `logging.conf`.
There are 3 loggers in `main.py`.

First of them is `access_logger`, which is used
for access logs into a file (`access.log`).

Access logging happens in `/entry/eval/` endpoint. Log file shows a pair
`(card_number, access_point_id)` in every log.

Second of them, `root_logger` can be used to print to `stdout`. One can use
`root_logger.info('message to print to stdout')` for this.

Third of them is `runtime_logger`, which is used
for runtime logs, such as runtime exceptions. It
logs into a file (`runtime.log`).

## Interaction with API

### Superuser

Most endpoints require superuser rights. There is a staff user with username
`stlpik` and password `secret`. It was inserted into the database from `fixtures.sql`.
This user should be allowed to fully interact with the API. 

### How to get access token (jwt)
Send `POST` request to `/token/` with body like:
```json
{
        "username": "name",
        "password": "verysecretpassword"
}
```

### Other endpoints

There is an interactive documentation generated by `FastAPI` accessible on `http://localhost:8000/docs`.
It is possible to send requests and receive responses directly from the docs for testing
and debugging purposes. 

#### `[GET] /users/`
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

#### `[POST] /users/`
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

#### `[DELETE] /users/delete/{user_id}/`
Deletes user with `id = user_id`. Example response:
```json
{
  "was_deleted": true,
  "detail": "success",
  "id": 2
}
```

#### `[GET] /users/me/`
Gets current user:
```json
{
  "first_name": "Meno",
  "username": "stlpik",
  "is_staff": true,
  "disabled": false,
  "updated": "2021-03-12T19:30:41.255382",
  "id": 1,
  "card": "1234567891011",
  "last_name": "Priezvisko",
  "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
  "created": "2021-03-12T19:30:41.255382"
}
```

#### `[GET] /groups/`
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

#### `[POST] /groups/`
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

#### `[GET] /groups/{group_id}/`
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

#### `[DELETE] /groups/delete/{group_id}/`
Deleted a group with `id = group_id`. Response similar to the one described
in `/users/delete/{user_id}/`

#### `[POST] /usergroup/add/`
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

#### `[DELETE] /usergroup/delete/{user_id}/{group_id}/`
Removes a user with `id = user_id` from the group with `id = group_id`.
Success response example:
```json
{
  "id": 1,
  "user_id": 1,
  "group_id": 1,
  "was_deleted": true
}
```

#### `[POST] /rules/add/`
Adds a rule. Does not assign it to groups yet.

Example request:
```json
{
  "name": "1INFComputerRooms",
  "allow": true,
  "time_spec_id": 1,
  "ap_type_id": 2,
  "priority": 6
}
```

Example response:
```json
{
  "name": "1INFComputerRooms",
  "allow": true,
  "time_spec_id": 1,
  "ap_type_id": 2,
  "priority": 6
}
```

#### `[DELETE] /rules/delete/{rule_id}/`
Deletes a rule with `id = rule_id`. Success response similar to the one
described in `/usergroup/delete/{user_id}/{group_id}/`.

#### `[POST] /timespec/add/`
Adds a time specification. Attribute `weekday_mask` works as follows.
Days are numbered `0` through `6` inclusively, where `0` is Monday and `6` is Sunday.
If day number `i` should be affected by this time specification, then it needs to be
set using `weekday_mask`. Day number `i` is affected iff `weekday_mask & (1 << i)`.
For example, time specification affecting Tuesday and Friday has `weekday_mask` of
`0010010` in binary, where least significant bit is last. This needs to be converted to
decimal, therefore, value of `weekday_mask` for Tuesday and Friday should be `18`.
Attributes `date_from` and `date_to` mark the beginning and the end of time period during
which this time specification is valid. Attributes `time_from` and `time_to` express
time period during which this time specification si valid during days specified by
`weekday_mask`.

Example request body:
```json
{
  "title": "MondayMorning",
  "weekday_mask": 1,
  "time_from": "06:00:00.000",
  "time_to": "09:00:00.000",
  "date_from": "2021-01-22 00:00:00.000",
  "date_to": "2022-01-22 00:00:00.000"
}
```

Example response:
```json
{
  "title": "MondayMorning",
  "weekday_mask": 1,
  "time_from": "06:00:00",
  "time_to": "09:00:00",
  "date_from": "2021-01-22T00:00:00",
  "date_to": "2022-01-22T00:00:00",
  "id": 4
}
```

#### `[DELETE] /timespec/delete/{time_spec_id}/`
Deletes the `TimeSpec` with `id = time_spec_id`.
Success response example:
```json
{
  "was_deleted": true,
  "detail": "success",
  "id": 2
}
```

#### `[POST] /aptype/add/`
Adds access point type. This is good for rules that need to affect multiple doors that need
similar level of security.

Example request:
```json
{
  "name": "ComputerRooms",
}
```

Example response:
```json
{
  "name": "ComputerRooms",
  "id": 2,
  "created": "2021-01-22T18:27:28.322909",
  "updated": "2021-01-22T18:27:28.322909"
}
```

#### `[DELETE] /aptype/delete/{ap_type_id}/`
Deletes an `AccessPointType` with `id = ap_type_id`.
Success response is similar to the one in `/timespec/delete/{time_spec_id}/`.
