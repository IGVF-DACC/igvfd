# igvfD
Metadata database for IGVF project.

## Run with Docker Compose (recommended)
1. Clone repository and make sure Docker is running.
2. Start services and load data inserts:
```
# From repository.
$ docker compose up
```
3. Browse at `localhost:8000`.
4. Stop services and remove data volume:
```
$ docker compose down -v
```

## Testing with Docker Compose

Run all tests automatically and clean up:
```
$ docker compose -f docker-compose.test.yml up --exit-code-from pyramid
....
$ docker compose -f docker-compose.test.yml down -v
```

Or run tests interactively:
1. Start `postgres` service (for use as fixture).
```
$ docker compose -f docker-compose.test.yml up postgres
```
2. Connect to testing environment.
```
# In another terminal (starts interactive container).
$ docker compose -f docker-compose.test.yml run --service-ports pyramid /bin/bash
```
3. Run tests.
```
# In interactive container (modify pytest command as needed).
$ pytest
```
4. Stop and clean.
```
docker compose down -v
```

## Run locally on Mac
1. Install NGINX, Python, and Postgres.
2. Clone repository and activate new virtual environment.
3. Install `igvfd` from repository:
```
$ pip install -e .
```
4. Run application:
```
# Start NGINX and Postgres and load data inserts.
$ run-local --clear --init --load
# In separate terminal (with virtual environment) serve Pyramid application.
$ pserve config/pyramid/ini/local.ini
```
5. Browse at `localhost:8000`.

## Testing locally on Mac
```
$ pytest --ini config/pyramid/ini/local.ini
```