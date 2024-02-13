## Changelog for *`technical_sample.json`*

### Minor changes since schema version 11

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
