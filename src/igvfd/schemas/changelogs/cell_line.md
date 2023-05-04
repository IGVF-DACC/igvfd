## Changelog for *`cell_line.json`*

### Minor changes since schema version 8

* Add `cellular_sub_pool`.

### Schema version 8

* Rename `biomarker` to `biomarkers`.
* Deprecate `cell_line` schema.

### Schema version 7

* Rename `donor` to `donors`.

### Minor changes since schema version 6
* Add `revoke_detail`.
* Make required properties `lab`, `source`, and `award` not submittable. No further submission of cell_line are accepted.
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

* Restrict `part_of` property to link only to `cell_line`.

### Schema version 2

* Add `donors` and `taxa` to requirements.

### Minor changes since schema version 1

* Rename `organism` to `taxa`.
* Convert `sex` to be calculated and not submittable.
