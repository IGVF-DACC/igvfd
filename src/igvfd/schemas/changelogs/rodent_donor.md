## Changelog for *`rodent_donor.json`*

### Schema version 9

* Rename `references` to `publication_identifiers`.

### Schema version 8

* Add `virtual`.

### Schema version 7

* Remove `parents`.

### Minor changes since schema version 6

* Add `dbxrefs`.

### Schema version 6

* Remove `traits`.

### Schema version 5

* Add `rodent_identifier`.
* Add `individual_rodent`.

### Schema version 4

* Remove `external_resource`.

### Minor changes since schema version 2

* Add `description`.
* Add `revoke_detail`.
* Add `phenotypic_features`.

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
