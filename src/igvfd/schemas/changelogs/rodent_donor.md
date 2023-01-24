## Changelog for *`rodent_donor.json`*

<<<<<<< HEAD
### Schema version 5
=======
### Schema version 3
>>>>>>> 7eee2ecc (changelogs)

* Add `rodent_identifier`.
* Add `individual_rodent`.

<<<<<<< HEAD
### Schema version 4

* Remove `external_resource`.

=======
>>>>>>> 7eee2ecc (changelogs)
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
