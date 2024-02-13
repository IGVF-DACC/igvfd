## Changelog for *`assay_term.json`*

### Minor changes since schema version 3

* Add `preferred_assay_titles`.
* Add `release_timestamp`.
* Add `ATAC-seq`, `RNA-seq`, `TF ChIP-seq`, `histone ChIP-seq`, `snRNA-seq`, `scRNA-seq`, `snATAC-seq` and `scATAC-seq` to `preferred_assay_title`.

### Schema version 3

* Disallow empty strings in `description`.

### Minor changes since schema version 2

* Add calculated property `ontology`.
* Add `description`.
* Add `is_a`.

### Schema version 2

* Restrict `aliases` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add calculated property `ancestors`.
* Rename schema `assay_ontology_term.json` to `assay_term.json`.
* Add `submitter_comment`, `submitted_by` and `creation_timestamp`.
