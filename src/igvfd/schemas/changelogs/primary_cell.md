## Changelog for *`primary_cell.json`*


### Schema version 11

* Remove `saccharomyces`.

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
