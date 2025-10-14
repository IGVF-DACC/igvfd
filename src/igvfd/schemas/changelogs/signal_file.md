## Changelog for *`signal_file.json`*

### Minor changes since schema version 13

* Add `catalog_class`.
* Add `catalog_notes`.
* Add `anvil_url`.
* Add `catalog_collections`.
* Add calculated property `workflows`.
* Remove calculated property `workflow`.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Add calculated property `transcriptome_annotation`.
* Add calculated property `assembly`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.

### Schema version 13

* Remove `assembly`.
* Remove `transcriptome_annotation`.

### Minor changes since schema version 12

* Add calculated property `preferred_assay_titles`
* Extend `transcriptome_annotation` enum list to include `GENCODE 24`.

### Schema version 12

* Adjust `normalized` to have default value `False`.

### Schema version 11

* Adjust `derived_manually` to have default value `False`.

### Minor changes since schema version 10

* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.

### Schema version 10

* Adjust `transcriptome_annotation` enum list to replace `GENCODE 28, GENCODE M17` with `GENCODE 32, GENCODE M23`.

### Minor changes since schema version 9

* Extend `transcriptome_annotation` enum list to include `GENCODE 28`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M25`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M17`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 28, GENCODE M17`.
* Extend `assembly` enum list to include `hg19`.
* Extend `assembly` enum list to include `mm10`.
* Extend `assembly` enum list to include `GRCh38, mm10`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 22`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 47`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M36`.
* Add `workflow`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Add `checkfiles_version`.
* Extend `content_type` enum list to include `sequence attributes`.
* Extend `content_type` enum list to include `TF binding scores`.
* Extend `file_format` enum list to include `npz`.
* Extend `upload_status` enum list to include `validation exempted`.
* Extend `status` enum list to include `preview`.
* Update calculation of `summary`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 32`.
* Extend `assembly` enum list to include `custom`.
* Add `derived_manually`.
* Extend `collections` enum list to include `VarChAMP`.
* Extend `assembly` enum list to include `Cast - GRCm39`.
* Extend `transcriptome_annotation` enum list to include `GENCODE Cast - M32`.
* Add calculated property `assay_titles`.
* Add `cell_type_annotation`.
* Update calculation of `summary`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.

### Schema version 9

* Adjust `content_type` enum list to replace `fold over change control` with `fold change over control`.

### Minor changes since schema version 8

* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 8

* Require `derived_from` to contain at least one value.
* Require `file_format_specifications` to contain at least one value.

### Schema version 7

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 6

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.

### Schema version 6

* Add `transcriptome_annotation`.
* Remove `hg19` and `mm10` from `assembly`.

### Minor changes since schema version 5

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 5

* Require `assembly` if `file_format` is one of `bam`, `bed`, `bedpe`, `bigWig`, `bigBed`, `bigInteract`, `tabix`, or `vcf`.

### Minor changes since schema version 4

* Add `assembly`.

### Schema version 4

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Require a minimum of 1 item for `dbxrefs`.

### Minor changes since schema version 1

* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
