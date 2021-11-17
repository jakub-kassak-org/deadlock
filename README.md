# deadlock-application

### How to run
This application is containerized using Docker. Build with command:
```commandline
docker compose build
```
To run download docker and run from terminal:
```commandline
docker compose up
```
Stop with CTR + C, then run:
```commandline
docker compose down
```

### Ports 
Front-end server is currently listening on port `8080`, back-end on port `8081` and database on port `5433`.  

### Volumes / mounts
Directory `./back-end/` is bind-mounted into python server for in-container development.

### Password
To sign into front-end or back-end use username `stlpik`, password `secret`. Database has user `test` with password `test`.