[![CircleCI](https://circleci.com/gh/IGVF-DACC/igvfd/tree/dev.svg?style=svg)](https://circleci.com/gh/IGVF-DACC/igvfd/tree/dev)
[![Coverage Status](https://coveralls.io/repos/github/IGVF-DACC/igvfd/badge.svg?branch=dev)](https://coveralls.io/github/IGVF-DACC/igvfd?branch=dev)
[![CodeBuild Status](https://codebuild.us-west-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiM04wWmZ5MlB0SlRVRWZpYjVOZFV5Y0hvU0FTRStlR0d5SDFjS0k0byt2ekxhK3NzYk1yTStEN1kycWppR1RRVHh0UlVBdllvZk4rSkdrdTB4UGVpdmpzPSIsIml2UGFyYW1ldGVyU3BlYyI6Img2aXJEOVY0emxRYndiVFIiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=dev)](https://us-west-2.codebuild.aws.amazon.com/project/eyJlbmNyeXB0ZWREYXRhIjoiRkduanVzYVRjSXFJY0N1T0dpQm5YNGowK09PSUVWdndycDR6Qm42RE5OUkY3Qy9ON0tLL0MvMmFjcHZFckJZUE80VU92dkFTMFp3dzNHSFBXYjJiMzZaL000d00wdmV2THBIWHNqYVNMU2NraVo2bDcyeUlIeTZ4RmhRSERFYlZSNEFadzI4SnVMNXYiLCJpdlBhcmFtZXRlclNwZWMiOiJRcWtkN3pRRUJLMThST05QIiwibWF0ZXJpYWxTZXRTZXJpYWwiOjF9)
# igvfD
Metadata database for IGVF project.

## Run with Docker Compose
1. Clone repository and make sure Docker is running.
2. Start services and load data inserts:
```bash
# From repository.
$ docker compose up
# Note if any dependencies have changed (e.g. switching between branches that
# rely on different versions of snovault) use the build flag as well
# to rebuild the underlying Docker image:
$ docker compose up --build
```
3. Browse at `localhost:8000`.
4. Stop services and remove data volume:
```bash
$ docker compose down -v
```

## Test with Docker Compose
Run all unit tests automatically and clean up:
```bash
$ docker compose -f docker-compose.test.yml up --exit-code-from pyramid
....
$ docker compose -f docker-compose.test.yml down -v
```

Run all indexer tests automatically and clean up:
```bash
$ docker compose -f docker-compose.test-indexer.yml up --exit-code-from indexer-tests
....
$ docker compose -f docker-compose.test-indexer.yml down -v
```

Or run tests interactively:
1. Start `postgres` and `localstack` services (for use as fixtures).
```bash
$ docker compose -f docker-compose.test.yml up postgres localstack
```
2. Connect to testing environment.
```bash
# In another terminal (starts interactive container).
$ docker compose -f docker-compose.test.yml run --service-ports pyramid /bin/bash
```
3. Run tests.
```bash
# In interactive container (modify pytest command as needed).
$ pytest
```
4. Stop and clean.
```bash
docker compose down -v
```

## Automatic linting
This repo includes configuration for pre-commit hooks. To use pre-commit, install pre-commit, and activate the hooks:
```bash
pip install pre-commit==2.17.0
pre-commit install
```
Now every time you run `git commit` the automatic checks are run to check the changes you made.
