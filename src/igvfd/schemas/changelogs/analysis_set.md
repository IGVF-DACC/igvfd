## Changelog for *`analysis_set.json`*

### Minor changes since schema version 5

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 5

* Disallow empty strings in `description`.

### Schema version 4

* Add `file_set_type`.
* Require `file_set_type`.

### Minor changes since schema version 3

* Add `files`.
* Add `dbxrefs`.
* Add `control_for`.
* Add `publication_identifiers`.
* Convert `donors` to be calculated from `samples`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
* Rename `assay_title` to `assay_titles`.

### Schema version 3

* Change `accessionType` to `DS`

### Schema version 2

* Rename `sample` to `samples`.
* Rename `donor` to `donors`.
* Rename `input_file_set` to `input_file_sets`.
