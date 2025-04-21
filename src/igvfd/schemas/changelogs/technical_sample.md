## Changelog for *`technical_sample.json`*

### Minor changes since schema version 14

* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `nucleic_acid_delivery` enum list to include `nucleofection`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `nucleic_acid_delivery` enum list to include `lipofectamine`.
* Extend `nucleic_acid_delivery` enum list to include `electroporation`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Extend `status` enum list to include `preview`.
* Extend `collections` enum list to include `VarChAMP`.

### Schema version 14

* Remove `publication_identifiers`.

### Schema version 13

* Require `sources` if `product_id` is specified.

### Minor changes since schema version 12

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Add `protocols`.
* Update `dbxrefs` regex to allow ENCODE sample accessions.

### Schema version 12

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 11

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 11

* Disallow empty strings in `description`.

### Schema version 10

* Rename `sorted_fraction` to `sorted_from`.
* Rename `sorted_fraction_detail` to `sorted_from_detail`.

### Minor changes since schema version 9

* Add `construct_library_sets`, `moi`, `nucleic_acid_delivery`, `time_post_library_delivery`, and `time_post_library_delivery_units`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
* Add `taxa`.

### Schema version 9

* Mutually require `starting_amount` and `starting_amount_units`.

### Schema version 8

* Rename `source` to `sources` and `technical_sample_term` to `sample_terms`.

### Minor changes since schema version 7

* Add `publication_identifiers`.

### Schema version 7

* Add `virtual`.

### Minor changes since schema version 6

* Add `cellular_sub_pool`.

### Schema version 6

* Add `sorted_fraction_detail`.

### Minor changes since schema version 4

* Add `sorted_fraction`.
* Add `file_sets`.

### Schema version 4

* Change `technical_sample_term` to link to `Sample Term`.
* Require `technical_sample_term`.

### Minor changes since schema version 3

* Add `description`.
* Add `revoke_detail`.

### Schema version 3

* Remove `additional_description`.

### Schema version 2

* Restrict `dbxrefs`, `aliases`, and `alternate_accessions` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Rename `date` to `date_obtained`.
