# igvfD
Metadata database for IGVF project.

## Run locally on Mac
1. Install Python and Postgres.
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
$ pserve config/pyramid/ini/development.ini
```
5. Browse at `localhost:8000`