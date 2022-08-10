## Changelog for *`differentiated_cell.json`*

### Schema version 6
* Remove `life_stage`.
* Add `lower_bound_age`.
* Add `upper_bound_age`.
* Convert `age` to be calculated from `lower_bound_age` and `upper_bound_age` and not submittable.

### Schema version 5

* Rename `disease_term` to `disease_terms`.
* Allow `disease_terms` to be an array of `phenotype_terms`.

### Minor changes since schema version 4

* Add `description`.

### Schema version 4

* Restrict `treatments`, `donors`, `differentiation_treatments`, `dbxrefs`, `aliases`, `collections`, and `alternate_accessions` to be a non-empty array with at least one item.

### Schema version 3

* Restrict `part_of` property to link only to `differentiated_cell`.

### Schema version 2

* Add `donors` and `taxa` to requirements.

### Minor changes since schema version 1

* Rename `organism` to `taxa`.
* Convert `sex` to be calculated and not submittable.
* Add `differentiated_from` and `differentiation_treatments`.
* Rename schema `in_vitro.json` to `differentiated_cell.json`.
