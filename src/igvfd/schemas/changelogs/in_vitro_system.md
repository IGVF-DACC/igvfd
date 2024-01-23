## Changelog for *`in_vitro_system.json`*

### Minor changes since schema version 18

* Add `release_timestamp`.

### Schema version 18

* Restrict specification of `cell_fate_change_protocol`, `cell_fate_change_treatments`, `targeted_sample_term`, `time_post_change`, and `time_post_change_units` if `classification` is `cell line`.

### Schema version 17

* Restrict linking of `cell_fate_change_treatments` to Treatment.
* Add `cell_fate_change_protocol`.

### Schema version 16

* Disallow empty strings in `description`.

### Schema version 15

* Rename `sorted_fraction` to `sorted_from`.
* Rename `sorted_fraction_detail` to `sorted_from_detail`.

### Minor changes since schema version 14

* Add `construct_library_sets`, `moi`, `nucleic_acid_delivery`, `time_post_library_delivery`, and `time_post_library_delivery_units`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 14

* Mutually require `starting_amount` and `starting_amount_units`.

### Schema version 13

* Rename `source` to `sources`, `biosample_term` to `sample_terms`, and `modification` to `modifications`.

### Minor changes since schema version 12

* Add `publication_identifiers`.

### Schema version 12

* Rename `introduced_factors` to `cell_fate_change_treatments`.
* Rename `time_post_factors_introduction` to `time_post_change`.
* Rename `time_post_factors_introduction_units` to `time_post_change_units`.

### Schema version 11

* Add `virtual`.

### Minor changes since schema version 10

* remove `permissions` from `classification`.

### Schema version 10

* Require `targeted_sample_term`, `introduced_factors`, `time_post_factors_introduction` and `time_post_factors_introduction_units` if `classification` is `organoid`, `differentiated cell specimen`, or `reprogrammed cell specimen`.
* Mutually require `introduced_factors` with `time_post_factors_introduction` and `time_post_factors_introduction_units`.

### Schema version 9

* Remove `taxa` from `required` and make it calculated.

### Minor changes since schema version 8

* Add `cellular_sub_pool`.

### Schema version 8

* Rename `differentiated cell` to `differentiated cell specimen`.
* Rename `reprogrammed cell` to `reprogrammed cell specimen`.
* Add `pooled cell specimen`.

### Schema version 7

* Remove taxa `Saccharomyces`.

### Schema version 6

* Add `sorted_fraction_detail`.

### Minor changes since schema version 5

* Add `sorted_fraction`.
* Add `targeted_sample_term`.
* Add `modification`.

### Schema version 5

* Remove `differentiated_tissue` from `classification`.

### Minor changes since schema version 3

* Add `file_sets`.

### Schema version 3

* Rename `biomarker` to `biomarkers`.

### Schema version 2

* Rename `donor` to `donors`.
