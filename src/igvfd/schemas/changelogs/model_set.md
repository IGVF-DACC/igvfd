## Changelog for *`model_set.json`*

### Minor changes since schema version 5

* Add calculated property `data_use_limitation_summaries`.
* Add calculated property `controlled_access`.
* Add calculated property `construct_library_sets`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.

### Schema version 5

* Add calculated property `software_versions`.
* Remove `software_version`.

### Minor changes since schema version 4

* Allow submission of `donors`.
* Allow submission of `samples`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Rename calculated property `input_file_set_for` to `input_for`.
* Add calculated property `externally_hosted`.
* Add `external_input_data`.
* Extend `collections` enum list to include `VarChAMP`.
* Update calculation of `summary`.
* Add `control_type`.

### Schema version 4

* Remove `publication_identifiers`.

### Minor changes since schema version 3

* Add `assessed_genes`.
* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Extend `file_set_type` enum list to include `variant binding effect`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.
* Add calculated property `input_file_set_for`.

### Schema version 3

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 2

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.
* Add calculated `submitted_files_timestamp`.

### Schema version 2

* Disallow empty strings in `description`.

### Minor changes since schema version 1
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
