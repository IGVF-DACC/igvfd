## Changelog for *`in_vitro_system.json`*

### Minor changes since schema version 27

* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.

### Schema version 27

* Remove `cell_fate_change_treatments`.

### Schema version 26

* Restrict `pooled cell specimen` to specify an additional `classifications`.

### Minor changes since schema version 25

* Add `annotated_from`.
* Extend `nucleic_acid_delivery` enum list to include `nucleofection`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `nucleic_acid_delivery` enum list to include `lipofectamine`.
* Extend `nucleic_acid_delivery` enum list to include `electroporation`.

### Schema version 25

* Adjust `biosample_qualifiers` enum list to remove `calcified`.
* Extend `biosample_qualifiers` enum list to include `6 days calcified`.
* Extend `biosample_qualifiers` enum list to include `10 days calcified`.

### Schema version 24

* Require `targeted_sample_term`, `time_post_change`, `time_post_change_units` and one of `cell_fate_change_treatments` or `cell_fate_change_protocols`  if `classification` is `gastruloid`.

### Minor changes since schema version 23

* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Extend `biosample_qualifiers` enum list to include `calcified`.
* Extend `status` enum list to include `preview`.
* Extend `collections` enum list to include `VarChAMP`.
* Add `biosample_qualifiers`.

### Schema version 23

* Remove `publication_identifiers`.

### Schema version 22

* Require `sources` if `product_id` is specified.

### Minor changes since schema version 21

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.

### Schema version 21

* Remove `nih_institutional_certification`.

### Minor changes since schema version 20

* Allow `modifications` to link to `Crispr Modifications`.
* Add `protocols`.
* Allow `modifications` to contain a maximum of 2 items.
* Add calculated property `upper_bound_age_in_hours`.
* Add calculated property `lower_bound_age_in_hours`.
* Add `growth_medium`.
* Add `demultiplexed_from`.
* Add calculated property `demultiplexed_to`.
* Update `dbxrefs` regex to allow ENCODE sample accessions.

### Schema version 20

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 19

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `MPRAbase` to `collections`.

### Schema version 19

* Replace `classification` with `classifications`.

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
