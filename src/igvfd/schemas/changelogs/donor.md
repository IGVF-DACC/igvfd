## Changelog for *`donor.json`*

* Add `release_timestamp`. (01/31/2024)
* Allow ENCODE donors in `dbxrefs`. (11/28/2023)
* Rename `references` to `publication_identifiers`. (08/02/2023)
* Add `virtual`. (06/05/2023)
* Add `dbxrefs`. (03/01/2023)
* Remove `parents`. (03/01/2023)
* Remove `traits`. (02/08/2023)
* Remove `external_resource`. (02/08/2023)
* Add `description`. (02/08/2023)
* Add `revoke_detail`. (02/08/2023)
* Add `phenotypic_features`. (02/08/2023)
* Restrict `parents`, `external_resources`, `aliases`, `collections`, `alternate_accessions`, `documents`, and `references` to be a non-empty array with at least one item. (02/08/2023)
* Add `traits`. (02/08/2023)
* Rename `organism` to `taxa`. (02/08/2023)
* Require `sex`, set default to:  (02/08/2023)
    ```json
    "unspecified"
    ```
