# igvfd
Metadata database for IGVF project

### Run locally on Mac

Prerequisites:
* Python
* Postgres

1. Clone repository and activate new virtual environment
2. Install `igvfd` with `$ pip install -e .`
3. Run `nginx` and `postgres` and load test data:
```
$ run-local --clear --init --load
```
4. In separate terminal (with virtual environment active) run `pyramid`:
```
$ pserve config/pyramid/ini/development.ini
```
5. Browse at `localhost:8000`