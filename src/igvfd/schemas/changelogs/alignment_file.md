## Changelog for *`alignment_file.json`*

### Minor changes since schema version 16

* Extend `transcriptome_annotation` enum list to include `GENCODE 24`.

### Schema version 16

* Adjust `redacted` to have default value `False`.

### Schema version 15

* Adjust `derived_manually` to have default value `False`.

### Minor changes since schema version 14

* Extend `base_modifications` enum list to include `m5C`.
* Extend `base_modifications` enum list to include `m6A`.
* Extend `content_type` enum list to include `alignments with modifications`.
* Add `preview_timestamp`.
* Add `base_modifications`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `content_type` enum list to include `methylated reads`.
* Extend `file_format` enum list to include `cram`.

### Schema version 14

* Adjust `transcriptome_annotation` enum list to replace `GENCODE 28, GENCODE M17` with `GENCODE 32, GENCODE M23`.

### Minor changes since schema version 13

* Allow `controlled_access` files to be released without `anvil_url`.
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

### Schema version 13

* Coerce `read_count` float integer (e.g. 28.0) to int (28).

### Minor changes since schema version 12

* Extend `transcriptome_annotation` enum list to include `GENCODE 47`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M36`.
* Add `workflow`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Add `checkfiles_version`.

### Schema version 12

* Require `assembly`.

### Minor changes since schema version 11

* Extend `upload_status` enum list to include `validation exempted`.
* Extend `status` enum list to include `preview`.

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
