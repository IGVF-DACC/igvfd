## Changelog for *`human_donor.json`*

### Schema version 6

* Remove `external_resource`.

### Minor changes since schema version 4

* Add `African Caribbean`, `Colombian`, `Dai Chinese`, `Kinh Vietnamese`, `Puerto Rican` to `ethnicities`.

### Schema version 4

* Rename `ethnicity` to `ethnicities`.

### Schema version 3

* Remove `health_status_history`.
* Add `phenotypic_features`.

### Minor changes since schema version 2

* Add `description`.
* Add `Pacific Islander` to `ethnicity` enum.
* Add `revoke_detail`.

### Schema version 2

* Restrict `parents`, `external_resources`, `aliases`, `collections`, `alternate_accessions`, `documents`, and `references` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add `traits`.
* Rename `organism` to `taxa`.
* Require `sex`, set default to:
    ```json
    "unspecified"
    ```
* Rename `taxon_id` to `organism`.
* Restrict `taxon_id` to NCBI taxonomy ids that start with NCBI:txid followed by numbers.
