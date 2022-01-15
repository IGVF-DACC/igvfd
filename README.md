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

Use `docker compose build` to rebuild images.

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