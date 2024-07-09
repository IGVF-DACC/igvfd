## Changelog for *`genome_browser_annotation_file.json`*

### Minor changes since schema version 8

* Update calculation of `summary`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.
* Extend `file_format_type` enum list to include `mpra_starr`.
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

* Add `GENCODE 44`, `GENCODE 45`, `GENCODE M33`, and `GENCODE M34` to `transcriptome_annotation`.
* Remove `hg19` and `mm10` from `assembly`.

### Minor changes since schema version 5

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 5

* Require `assembly` if `file_format` is one of `bam`, `bed`, `bedpe`, `bigWig`, `bigBed`, `bigInteract`, `tabix`, or `vcf`.

### Schema version 4

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Require a minimum of 1 item for `dbxrefs`.
