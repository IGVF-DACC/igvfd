## Changelog for *`model_set.json`*

### Minor changes since schema version 6

* Add calculated property `is_on_anvil`.
* Extend `preferred_assay_titles` enum list to include `MAVE`.
* Extend `collections` enum list to include `E2G Pillar Project`.
* Extend `collections` enum list to include `Bridge Sample`.
* Update `dbxrefs` regex to allow MaveDB score set URNs.
* Extend `preferred_assay_titles` enum list to include `Multiome Perturb-seq`.
* Add calculated property `superseded_by`.
* Add `supersedes`.

### Schema version 6

* Extend `preferred_assay_titles` enum list to include `DUAL-IPA`.
* Extend `preferred_assay_titles` enum list to include `10x snATAC-seq with Scale pre-indexing`.
* Extend `preferred_assay_titles` enum list to include `snRNA-seq with Scale pre-indexing`.
* Adjust `preferred_assay_titles` enum list to remove `10x Scale pre-indexing`.

### Minor changes since schema version 5

* Extend `preferred_assay_titles` enum list to include `DNase-seq`.
* Add `preferred_assay_titles`.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.
* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `file_set_type` enum list to include `logistic regression`.
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
