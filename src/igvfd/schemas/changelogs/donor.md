## Changelog for *`donor.json`*

### Release v5

* Add `dbxrefs`.
* Remove `parents`.

### Release v2

* Remove `traits`.
* Remove `external_resource`.
* Add `description`.
* Add `revoke_detail`.
* Add `phenotypic_features`.
* Restrict `parents`, `external_resources`, `aliases`, `collections`, `alternate_accessions`, `documents`, and `references` to be a non-empty array with at least one item.
* Add `traits`.
* Rename `organism` to `taxa`.
* Require `sex`, set default to:
    ```json
    "unspecified"
    ```
