## Changelog for *`rodent_donor.json`*

### Minor changes since schema version 14

* Extend `strain_background` enum list to include `B6129S1F1/J`.
* Extend `strain_background` enum list to include `B6AF1/J`.
* Extend `strain_background` enum list to include `B6CASTF1/J`.
* Extend `strain_background` enum list to include `B6NODF1/J`.
* Extend `strain_background` enum list to include `B6NZOF1/J`.
* Extend `strain_background` enum list to include `B6PWKF1/J`.
* Extend `strain_background` enum list to include `B6WSBF1/J`.
* Extend `collections` enum list to include `VarChAMP`.

### Schema version 14

* Remove `publication_identifiers`.

### Schema version 13

* Require `sources` if `product_id` is specified.

### Minor changes since schema version 12

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Update calculation of `summary`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 12

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 11

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 11

* Disallow empty strings in `description`.

### Minor changes since schema version 10
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 10

* Rename `source` to `sources`.

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
