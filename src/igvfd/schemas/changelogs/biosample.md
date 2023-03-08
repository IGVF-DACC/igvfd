## Changelog for *`biosample.json`*

### Release v6

* Add `file_sets`.

### Release v2

* Rename `biomarker` to `biomarkers`.
* Deprecate `differentiated_tissue`, `differentiated_cell`, `cell_line` schemas.
* Rename `donor` to `donors`.
* Add `revoke_detail`.
* Rename `donors` to `donor`.
* Remove `life_stage`.
* Add `lower_bound_age`.
* Add `upper_bound_age`.
* Add `embryonic`.
* Convert `age` to be calculated from `lower_bound_age` and `upper_bound_age` and not submittable.
* Require `biosample_term`.
* Rename `disease_term` to `disease_terms`.
* Allow `disease_terms` to be an array of `phenotype_terms`.
* Add `description`.
* Restrict `treatments`, `donors`, `dbxrefs`, `aliases`, `collections`, and `alternate_accessions` to be a non-empty array with at least one item.
* Add `donors` and `taxa` to requirements.
* Rename `organism` to `taxa`.
* Remove `related_biosamples` and `related_biosamples_relationship`.
* Add `pooled_from` and `part_of`.
