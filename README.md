# deadlock-server


### How to run
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

### How to get access token (jwt)
Send `POST` request to `/token` with body like:
```json
{
        "username": "peter",
        "password": "verysecretpassword"
}
```

### Endpoints

####`/users`
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


