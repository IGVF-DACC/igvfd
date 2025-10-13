## Changelog for *`model_file.json`*

### Minor changes since schema version 2

* Add `catalog_class`.
* Add `catalog_notes`.
* Add `catalog_collections`.
* Extend `content_type` enum list to include `neural network architecture and edge weights`.
* Extend `file_format` enum list to include `zip`.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Add calculated property `workflows`.
* Remove calculated property `workflow`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.
* Extend `content_type` enum list to include `covariance matrix`.

### Schema version 2

* Add calculated property `preferred_assay_titles`
* Adjust `derived_manually` to have default value `False`.

### Minor changes since schema version 1

* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `file_format` enum list to include `pkl`.
* Extend `content_type` enum list to include `feature weights`.
* Allow `controlled_access` files to be released without `anvil_url`.
* Add `catalog_adapters`.
* Extend `content_type` enum list to include `protein language model`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Add `workflow`.
* Extend `content_type` enum list to include `neural network architecture`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Add `checkfiles_version`.
* Extend `file_format` enum list to include `pt`.
* Extend `upload_status` enum list to include `validation exempted`.
* Extend `status` enum list to include `preview`.
* Update `dbxrefs` regex to add `Kipoi` as a namespace.
* Add `external_host_url`.
* Add `externally_hosted`.
* Add `derived_manually`.
* Extend `collections` enum list to include `VarChAMP`.
* Extend `content_type` enum list to include `SNP effect matrix`.
* Add calculated property `assay_titles`.
* Update calculation of `summary`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.
