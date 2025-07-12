## Changelog for *`whole_organism.json`*

### Minor changes since schema version 25

* Allow `originated_from` to link to Multiplexed Sample or Technical Sample.

### Schema version 25

* Adjust `embryonic` to have default value `False`.

### Minor changes since schema version 24

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
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Extend `status` enum list to include `preview`.
* Extend `collections` enum list to include `VarChAMP`.

### Schema version 24

* Remove `publication_identifiers`.

### Schema version 23

* Require `sources` if `product_id` is specified.

### Minor changes since schema version 22

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.

### Schema version 22

* Remove `nih_institutional_certification`.

### Minor changes since schema version 21

* Allow `modifications` to link to `Crispr Modifications`.
* Add `protocols`.
* Allow `modifications` to contain a maximum of 2 items.
* Add calculated property `upper_bound_age_in_hours`.
* Add calculated property `lower_bound_age_in_hours`.
* Update `dbxrefs` regex to allow ENCODE sample accessions.
* Add `originated_from`.

### Schema version 21

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 20

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 20

* Disallow empty strings in `description`.

### Schema version 19

* Rename `sorted_fraction` to `sorted_from`.
* Rename `sorted_fraction_detail` to `sorted_from_detail`.

### Minor changes since schema version 18

* Add `construct_library_sets`, `moi`, `nucleic_acid_delivery`, `time_post_library_delivery`, and `time_post_library_delivery_units`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 18

* Mutually require `starting_amount` and `starting_amount_units`.

### Schema version 17

* Rename `source` to `sources`, `biosample_term` to `sample_terms`, and `modification` to `modifications`.

### Schema version 16

* Rename `references` to `publication_identifiers`.

### Schema version 15

* Disallow `part_of` and `pooled_from`.

### Schema version 14

* Add `virtual`.

### Schema version 13

* Remove `taxa` from `required` and make it calculated.

### Schema version 12

* Restrict `biosample_term` to `whole organism`.

### Minor changes since schema version 11

* Add `cellular_sub_pool`.

### Schema version 11

* Disallow `part_of` and `pooled_from` properties.

### Schema version 10

* Remove taxa `Saccharomyces`.

### Schema version 9

* Add `sorted_fraction_detail`.

### Minor changes since schema version 7

* Add `sorted_fraction`.
* Add `file_sets`.
* Add `modification`.

### Schema version 7

* Rename `biomarker` to `biomarkers`.

### Schema version 6

* Rename `donor` to `donors`.

### Minor changes since schema version 5
* Add `revoke_detail`.
* Rename `donors` to `donor`.

### Schema version 5

* Remove `life_stage`.
* Add `lower_bound_age`.
* Add `upper_bound_age`.
* Add `embryonic`.
* Convert `age` to be calculated from `lower_bound_age` and `upper_bound_age` and not submittable.
* Require `biosample_term`.

### Schema version 4

* Rename `disease_term` to `disease_terms`.
* Allow `disease_terms` to be an array of `phenotype_terms`.

### Minor changes since schema version 3

* Add `description`.

### Schema version 3

* Restrict `treatments`, `donors`, `dbxrefs`, `aliases`, `collections`, and `alternate_accessions` to be a non-empty array with at least one item.

### Schema version 2

* Add `donors` and `taxa` to requirements.
