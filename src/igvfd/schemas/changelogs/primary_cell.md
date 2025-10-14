## Changelog for *`primary_cell.json`*

### Schema version 24

* Update `protocols` regex to `^https://www\\.protocols\\.io/(private|view)/(\\S+)$`.

### Minor changes since schema version 23

* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.
* Allow `originated_from` to link to Multiplexed Sample or Technical Sample.

### Schema version 23

* Adjust `embryonic` to have default value `False`.

### Minor changes since schema version 22

* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
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

### Schema version 22

* Adjust `biosample_qualifiers` enum list to remove `calcified`.
* Extend `biosample_qualifiers` enum list to include `6 days calcified`.
* Extend `biosample_qualifiers` enum list to include `10 days calcified`.

### Minor changes since schema version 21

* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Extend `biosample_qualifiers` enum list to include `calcified`.
* Extend `status` enum list to include `preview`.
* Extend `collections` enum list to include `VarChAMP`.
* Add `biosample_qualifiers`.

### Schema version 21

* Remove `publication_identifiers`.

### Schema version 20

* Require `sources` if `product_id` is specified.

### Minor changes since schema version 19

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.

### Schema version 19

* Remove `nih_institutional_certification`.

### Minor changes since schema version 18

* Allow `modifications` to link to `Crispr Modifications`.
* Add `protocols`.
* Allow `modifications` to contain a maximum of 2 items.
* Add calculated property `upper_bound_age_in_hours`.
* Add calculated property `lower_bound_age_in_hours`.
* Update `dbxrefs` regex to allow ENCODE sample accessions.
* Add `originated_from`.

### Schema version 18

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 17

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

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
