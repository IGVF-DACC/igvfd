## Changelog for *`analysis_set.json`*

### Minor changes since schema version 10

* Add `doi`.
* Extend `collections` enum list to include `E2G Pillar Project`.
* Extend `collections` enum list to include `Bridge Sample`.
* Update `dbxrefs` regex to allow MaveDB score set URNs.
* Add calculated property `superseded_by`.
* Add `supersedes`.
* Update `protocols` regex to `^https://www\\.protocols\\.io/(private|view)/(\\S+)$`.
* Add calculated property `primer_designs`.
* Add `pipeline_parameters`.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.
* Add `uniform_pipeline_status`.
* Add calculated property `preferred_assay_titles`
* Add calculated property `targeted_genes`.

### Schema version 10

* Rename `demultiplexed_sample` to `demultiplexed_samples`.

### Minor changes since schema version 9

* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Add calculated property `data_use_limitation_summaries`.
* Add calculated property `controlled_access`.
* Update calculation of `summary`.
* Update calculation of `assay_titles`.
* Add calculated property `construct_library_sets`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Extend `status` enum list to include `preview`.
* Rename calculated property `input_file_set_for` to `input_for`.

### Schema version 9

* Convert `samples` to be calculated from `input_file_sets` and `demultiplexed_sample`.
* Add `demultiplexed_sample`.

### Minor changes since schema version 8

* Add calculated property `workflows`.
* Extend `collections` enum list to include `VarChAMP`.
* Add calculated property `sample_summary`.
* Add calculated property `functional_assay_mechanisms`.
* Add calculated property `protocols`.
* Add `control_type`.
* Add `external_image_data_url`.

### Schema version 8

* Remove `publication_identifiers`.

### Minor changes since schema version 7

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.

### Schema version 7

* Adjust `file_set_type` enum list to replace `primary analysis` with `principal analysis`.

### Minor changes since schema version 6

* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.
* Add calculated property `input_file_set_for`.

### Schema version 6

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 5

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.
* Add calculated `submitted_files_timestamp`.

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
