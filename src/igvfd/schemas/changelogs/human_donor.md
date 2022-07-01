## Changelog for *`human_donor.json`*

### Minor changes since schema version 1

* Add `traits`.
* Rename `organism` to `taxa`.
* Require `sex`, set default to:
    ```json
    "unspecified"
    ```
* Rename `taxon_id` to `organism`.
* Restrict `taxon_id` to NCBI taxonomy ids that start with NCBI:txid followed by numbers.
* Added type to parents property. This was missing and will cause an error when patching.
