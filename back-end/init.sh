#!/bin/bash

echo "starting initialization"

if python main.py; then
    echo "table initialization success"
else
    echo "table initialization fail"
    exit 1
fi

if python db/db_seeder.py; then
    echo "db_seeder success"
else
    echo "db_seeder fail"
fi

echo "initialization successfull"

if [ -n "$STAGE" ] && [ "$STAGE" = "dev" ]; then
  echo "starting scheduled tasks"
  python scripts/my_schedule.py
else
  echo "starting scheduled tasks"
  python scripts/my_schedule.py &
  echo "starting server"
  uvicorn main:app --host 0.0.0.0 --port 80
fi
