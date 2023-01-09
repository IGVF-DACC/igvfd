## Changelog for *`biosample.json`*

### Schema version 6

* Rename `aliases` to `alias`.
* Rename `alternate_accessions` to `alternate_accession`.
* Rename `collections` to `collection`.
* Rename `documents` to `document`.
* Rename `treatments` to `treatment`.
* Rename `disease_terms` to `disease_term`.
* Rename `dbxrefs` to `dbxref`.
* Change `part_of` type from `string` to `array`.

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

### Minor changes since schema version 1

* Rename `organism` to `taxa`.
* Remove `related_biosamples` and `related_biosamples_relationship`.
* Add `pooled_from` and `part_of`.
