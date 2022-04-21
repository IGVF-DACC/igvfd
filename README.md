[![CircleCI](https://circleci.com/gh/IGVF-DACC/igvfd/tree/dev.svg?style=svg)](https://circleci.com/gh/IGVF-DACC/igvfd/tree/dev)
[![Coverage Status](https://coveralls.io/repos/github/IGVF-DACC/igvfd/badge.svg?branch=dev)](https://coveralls.io/github/IGVF-DACC/igvfd?branch=dev)
[![CodeBuild Status](https://codebuild.us-west-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiWlR0TjZxSmNiaWR6UXpYNmgvMWpVNjZPaUhmZm9HTjY4Uzd6MEJpTGd1L3hMelVYQlZ4VHB4YmxSN1JTTlZzZVNhR0gyY3hmb3JGRTFML1hRVWE3dkpNPSIsIml2UGFyYW1ldGVyU3BlYyI6IlBHaWJoLzRqZUlwQXFMckYiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=cdk)](https://us-west-2.codebuild.aws.amazon.com/project/eyJlbmNyeXB0ZWREYXRhIjoiV1AvUDlNU1JnNXdZWTVzbjMyQVVFcFJ1OG9JcVkxanZtTEJvaVJyR05HU2VQdnVVdWo3YW41VGdYRHpFblIyb1BvUXZ0aFZxQVppUjJibnpqZytSZ0o1aWovS2ZBSTBJa1UzQWJ6Tm9SREpYRjIvV0NsNU82SmtrdUJNR2RxMWM2bFVuZ3pxbU5MWFQiLCJpdlBhcmFtZXRlclNwZWMiOiJwVVBPdFlGYUttR2ZQbmhFIiwibWF0ZXJpYWxTZXRTZXJpYWwiOjF9)
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
Run all tests automatically and clean up:
```bash
$ docker compose -f docker-compose.test.yml up --exit-code-from pyramid
....
$ docker compose -f docker-compose.test.yml down -v
```

Or run tests interactively:
1. Start `postgres` service (for use as fixture).
```bash
$ docker compose -f docker-compose.test.yml up postgres
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
