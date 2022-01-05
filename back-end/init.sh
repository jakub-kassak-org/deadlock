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

echo "initialization successful"

if [ -n "$STAGE" ]; then
  if [ "$STAGE" = "dev" ]; then
    echo "starting scheduled tasks"
    python scripts/my_schedule.py
  elif [ "$STAGE" = "test"  ]; then
    echo "starting server"
    uvicorn main:app --host 0.0.0.0 --port 80 &
    PID=$!
    sleep 2
    echo "running users"
    python scripts/users.py
    wait $PID
  elif [ "$STAGE" = "prod" ]; then
    echo "starting scheduled tasks"
    python scripts/my_schedule.py &
    echo "starting server"
    uvicorn main:app --host 0.0.0.0 --port 80
  else
    echo "stage $STAGE is unknown"
  fi
else
  echo "no stage set"
fi
