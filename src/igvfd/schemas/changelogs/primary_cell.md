## Changelog for *`primary_cell.json`*

### Schema version 17

* Disallow empty strings in `description`.

### Schema version 16

* Rename `sorted_fraction` to `sorted_from`.
* Rename `sorted_fraction_detail` to `sorted_from_detail`.

### Minor changes since schema version 15

* Add `construct_library_sets`, `moi`, `nucleic_acid_delivery`, `time_post_library_delivery`, and `time_post_library_delivery_units`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 15

* Mutually require `starting_amount` and `starting_amount_units`.

### Schema version 14

* Rename `source` to `sources`, `biosample_term` to `sample_terms`, and `modification` to `modifications`.

### Minor changes since schema version 13

* Add `publication_identifiers`.

### Schema version 13

* Add `virtual`.

### Minor changes since schema version 12

* Add `cellular_sub_pool`.

### Schema version 12

* Remove `taxa` from `required` and make it calculated.

### Schema version 11

* Remove taxa `Saccharomyces`.

### Schema version 10

* Add `sorted_fraction_detail`.

### Minor changes since schema version 8

* Add `sorted_fraction`.
* Add `file_sets`.
* Add `modification`.

### Schema version 8

* Rename `biomarker` to `biomarkers`.

### Schema version 7

* Rename `donor` to `donors`.

### Minor changes since schema version 6
* Add `revoke_detail`.
* Rename `donors` to `donor`.

### Schema version 6

* Remove `life_stage`.
* Add `lower_bound_age`.
* Add `upper_bound_age`.
* Add `embryonic`.
* Convert `age` to be calculated from `lower_bound_age` and `upper_bound_age` and not submittable.
* Require `biosample_term`.

### Schema version 5

* Rename `disease_term` to `disease_terms`.
* Allow `disease_terms` to be an array of `phenotype_terms`.

### Minor changes since schema version 4

* Add `description`.

### Schema version 4

* Restrict `treatments`, `donors`, `dbxrefs`, `aliases`, `collections`, and `alternate_accessions` to be a non-empty array with at least one item.

### Schema version 3

* Restrict `part_of` property to link only to `primary_cell`, `tissue` and `whole organism`.

### Schema version 2

* Add `donors` and `taxa` to requirements.

### Minor changes since schema version 1

* Rename `organism` to `taxa`.
* Convert `sex` to be calculated and not submittable.
