## Changelog for *`ontology_term.json`*

### Schema version 3

* Rename `aliases` to `alias`.
* Rename `synonyms` to `synonym`.
* Rename `deprecated_ntr_terms` to `deprecated_ntr_term`.

### Minor changes since schema version 2

* Add `description`.

### Schema version 2

* Restrict `aliases` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add calculated properties `assay_slims` and `objective_slims`.
* Rename schema `term.json` to `ontology_term.json`.
* Rename schema `ontology_term.json` to `term.json`.
* Add `submitter_comment`, `submitted_by` and `creation_timestamp`.
