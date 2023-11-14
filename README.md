[![CircleCI](https://circleci.com/gh/IGVF-DACC/igvfd/tree/dev.svg?style=svg)](https://circleci.com/gh/IGVF-DACC/igvfd/tree/dev)
[![Coverage Status](https://coveralls.io/repos/github/IGVF-DACC/igvfd/badge.svg?branch=dev)](https://coveralls.io/github/IGVF-DACC/igvfd?branch=dev)
[![CodeBuild Status](https://codebuild.us-west-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiK3gyS2EyeWtwU1JPUUh3ZHZKYjlzcU1qTENuREUzc3F4NGc2L0F3SXNUMUZpTkVGZ2lXWnB1SHJsdUlLNml5WEtFOUZhdkZqdzhvVktzdC9IRVFBbDZjPSIsIml2UGFyYW1ldGVyU3BlYyI6ImlJRFlrQWY2SWVxRC9tbTIiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=dev)](https://us-west-2.codebuild.aws.amazon.com/project/eyJlbmNyeXB0ZWREYXRhIjoibnN1SXV1Y0xWZVB1YTlIYlJTTnhjYkRGRTk2UmhzVHBYbG9OcjEyc1lib2htOGxIWlF1bXJIQ0V2RGxEbmxkNmkwU2xpRzExNHQ1VG5WZTNRa0I4aXFqNm5mZmR0VGpIblBrRTB2aVFEZUFlTndzU3JSUHVTRmF5Qm1BZWdEQTVRVUNFNGdxVnhFMGMiLCJpdlBhcmFtZXRlclNwZWMiOiJNdExjcWRadW9HcHhFajBSIiwibWF0ZXJpYWxTZXRTZXJpYWwiOjF9)
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

Or run unit tests interactively:
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

Or run indexer tests interactively:
1. Start the services (for use as fixtures): `postgres`, `localstack`, `opensearch`, `pyramid`, `nginx`, `invalidation-service` and `indexing-service`.
```bash
$ docker compose -f docker-compose.test-indexer.yml up localstack postgres opensearch pyramid nginx invalidation-service indexing-service
```
2. Connect to testing environment.
```bash
# In another terminal (starts interactive container).
$ docker compose -f docker-compose.test-indexer.yml run --service-ports indexer-tests /bin/bash
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


## Generate Opensearch mappings

The `igvfd-check-opensearch-mappings` test on CircleCI will fail if the mappings haven't been updated after changing schemas, calculated properties, or embedded fields.

```bash
$ docker compose down -v && docker compose build
$ docker compose run pyramid /scripts/pyramid/generate-opensearch-mappings.sh
```

This will regenerate the mappings and allow you to see any differences with `git diff`. Commit the changes and push.

Note if you are adding a new item type, you must add a template JSON file to the `mappings/` folder with the same name as the new type (e.g. `access_key.json`). The template file requires the `index_name` and `item_type` keys, but the values can be empty:

```bash
$ echo '{"index_name": "", "item_type": ""}' > src/igvfd/mappings/new_type.json
```

Once the JSON template exists the correct values will be filled in by the `generate-opensearch-mappings.sh` script.
