## Changelog for *`whole_organism.json`*


### Schema version 13

* Remove `taxa` from `required` and make it calculated.

### Schema version 12

* Restrict `biosample_term` to `whole organism`.

### Minor changes since schema version 11

* Add `cellular_sub_pool`.

# Schema version 11

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

* Restrict `treatments`, `donors`, `dbxrefs`, `aliases`, `collections`, and `alternate_accessions` to be a non - empty array with at least one item.

### Schema version 2

* Add `donors` and `taxa` to requirements.
