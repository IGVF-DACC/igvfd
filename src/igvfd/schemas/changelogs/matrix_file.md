## Changelog for *`matrix_file.json`*

### Minor changes since schema version 9

* Add calculated property `superseded_by`.
* Add `supersedes`.
* Add `catalog_class`.
* Add `catalog_notes`.
* Add `anvil_url`.
* Add `catalog_collections`.
* Extend `file_format` enum list to include `h5mu`.
* Extend `content_type` enum list to include `annotated multimodal CRISPR matrix`.
* Extend `principal_dimension` enum list to include `CRISPR guide capture`.
* Extend `principal_dimension` enum list to include `mitochondrial variants`.
* Extend `content_type` enum list to include `mitochondrial DNA heteroplasmy`.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Add calculated property `workflows`.
* Remove calculated property `workflow`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.
* Add calculated property `preferred_assay_titles`
* Extend `file_format` enum list to include `rds`.
* Add calculated property `transcriptome_annotation`.
* Add calculated property `assembly`.

### Schema version 9

* Adjust `derived_manually` to have default value `False`.

### Schema verion 8

* Adjust `content_type` enum list to replace `comprehensive gene count matrix` with `kallisto single cell RNAseq output`.

### Minor changes since schema version 7

* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `content_type` enum list to include `comprehensive gene count matrix`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 22`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `principal_dimension` enum list to include `spot barcode`.
* Extend `file_format` enum list to include `Robj`.
* Add `filtered`.
* Extend `secondary_dimensions` enum list to include `barcode count`.
* Extend `content_type` enum list to include `sample barcode count matrix`.
* Add `workflow`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Add `checkfiles_version`.
* Extend `secondary_dimensions` enum list to include `UMI count`.
* Extend `file_format` enum list to include `pkl`.
* Extend `secondary_dimensions` enum list to include `peak`.
* Extend `upload_status` enum list to include `validation exempted`.
* Extend `status` enum list to include `preview`.
* Update calculation of `summary`.
* Extend `file_format` enum list to include `cool`.
* Extend `file_format` enum list to include `mcool`.
* Add `derived_manually`.
* Extend `collections` enum list to include `VarChAMP`.

### Schema version 7

* Extend `secondary_dimensions` enum list to include `gene expression`.
* Extend `secondary_dimensions` enum list to include `CRISPR guide capture`.
* Extend `secondary_dimensions` enum list to include `antibody capture`.
* Change type of `secondary_dimensions` to be an array.
* Rename `dimension2` to `secondary_dimensions`.
* Rename `dimension1` to `principal_dimension`.

### Minor changes since schema version 6

* Add calculated property `assay_titles`.
* Extend `content_type` enum list to include `raw feature barcode matrix`.
* Extend `content_type` enum list to include `filtered feature barcode matrix`.
* Update calculation of `summary`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 6

* Require `derived_from` to contain at least one value.
* Require `file_format_specifications` to contain at least one value.

### Schema version 5

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 4

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `hic` to `file_format`.
* Add `genomic position` to `dimension1` and `dimension2`.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 4

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 3

* Disallow empty strings in `description`.

### Minor changes since schema version 2

* Expand `file_format` enum list to include `tar`.

### Schema version 2

* Require a minimum of 1 item for `dbxrefs`.

### Minor changes since schema version 1

* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
