Automatically generated. Do not edit this folder manually.

Anytime you change something that affects the Opensearch mapping for a type (e.g. JSON schemas, calculated properties, embedded fields), you must regenerate the mappings and commit the latest changes to Github.

A failing `igvfd-check-opensearch-mappings` test on CircleCI is a sign that you need to regenerate the mappings.

To generate latest Opensearch mappings (run in top-level `igvfd` folder):
```bash
$ docker compose down -v
$ docker compose run pyramid /scripts/pyramid/generate-opensearch-mappings.sh --build
```
This cleans up old Docker containers first, then writes the lastest Opensearch mappings to the `mappings/` folder.

You can see generated differences with `git diff`. Commit these and push. CircleCI `igvfd-check-opensearch-mappings` test should pass.
