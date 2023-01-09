## Changelog for *`differentiated_tissue.json`*

### Schema version 8

* Rename `aliases` to `alias`.
* Rename `alternate_accessions` to `alternate_accession`.
* Rename `collections` to `collection`.
* Rename `documents` to `document`.
* Rename `treatments` to `treatment`.
* Rename `disease_terms` to `disease_term`.
* Rename `differentiation_treatments` to `differentiation_treatment`.
* Rename `dbxrefs` to `dbxref`.
* Change `part_of` type from `string` to `array`.

### Minor changes since schema version 7
* Add `revoke_detail`.
* Make required properties `lab`, `source`, and `award` not submittable. No further submission of differentiated_tissue are accepted.
* Rename `donors` to `donor`.

### Schema version 7

* Remove `stage` from `post_differentiation_time_units`.
* Change `post_differentiation_time` type from `integer` to `number`.

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

* Restrict `treatments`, `donors`, `differentiation_treatments`, `dbxrefs`, `aliases`, `collections`, and `alternate_accessions` to be a non-empty array with at least one item.

### Schema version 3

* Restrict `part_of` property to link only to `differentiated_tissue`.

### Schema version 2

* Add `donors` and `taxa` to requirements.

### Minor changes since schema version 1

* Rename `organism` to `taxa`.
* Convert `sex` to be calculated and not submittable.
* Add `differentiated_from` and `differentiation_treatments`.
* Rename schema `organoid.json` to `differentiated_tissue.json`.
