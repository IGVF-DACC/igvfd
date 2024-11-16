## Changelog for *`alignment_file.json`*

### Schema version 11

* Reduce `file_format` enum list to exclude `bai`.

### Minor changes since schema version 10

* Update calculation of `summary`.
* Extend `file_format` enum list to include `bai`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 32`.
* Extend `assembly` enum list to include `custom`.
* Add `read_count`.
* Add `derived_manually`.
* Extend `collections` enum list to include `VarChAMP`.
* Extend `assembly` enum list to include `Cast - GRCm39`.
* Extend `transcriptome_annotation` enum list to include `GENCODE Cast - M32`.
* Add calculated property `assay_titles`.
* Update calculation of `summary`.
* Add calculated property `input_file_for`.
* Add `analysis_step_version`.

### Schema version 10

* Reduce `upload_status` enum list to exclude `deposited`.
* Remove `anvil_source_url`.
* Add `anvil_url`.
* Require `controlled_access`.

### Minor changes since schema version 9

* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 9

* Extend `upload_status` enum list to include `deposited`.
* Add `controlled_access`.
* Add `anvil_source_url`.
* Add calculated property `anvil_destination_url`.

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
