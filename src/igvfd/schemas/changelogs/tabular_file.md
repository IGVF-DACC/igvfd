## Changelog for *`tabular_file.json`*

### Minor changes since schema version 12

* Extend `collections` enum list to include `VarChAMP`.
* Extend `content_type` enum list to include `peak quantifications`.
* Extend `content_type` enum list to include `variant localization impacts`.

### Schema version 12

* Extend `content_type` enum list to include `external source data`.
* Extend `content_type` enum list to include `fragments`.
* Extend `content_type` enum list to include `gene quantifications`.
* Adjust `content_type` enum list to remove `SNP effect matrix`.

### Minor changes since schema version 11

* Extend `assembly` enum list to include `Cast - GRCm39`.
* Extend `transcriptome_annotation` enum list to include `GENCODE Cast - M32`.
* Extend `content_type` enum list to include `genes`.
* Extend `content_type` enum list to include `loci`.
* Add calculated property `assay_titles`.
* Add calculated property `barcode_map_for`.
* Extend `content_type` enum list to include `transcript quantifications`.
* Extend `content_type` enum list to include `barcode to hashtag mapping`.
* Extend `content_type` enum list to include `barcode to variant mapping`.
* Add `cell_type_annotation`.
* Extend `content_type` enum list to include `variant binding effects`.
* Extend `content_type` enum list to include `SNP effect matrix`.
* Extend `content_type` enum list to include `tissue positions`.
* Extend `content_type` enum list to include `prime editing guide RNA sequences`.
* Update calculation of `summary`.
* Extend `content_type` enum list to include `editing templates`.
* Extend `content_type` enum list to include `variants`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.
* Extend `content_type` enum list to include `sample sort parameters`.
* Extend `content_type` enum list to include `differential gene expression quantifications`.
* Extend `content_type` enum list to include `differential transcript expression quantifications`.
* Extend `content_type` enum list to include `MPRA sequence designs`.

### Schema version 11

* Adjust `content_type` enum list to replace `fold over change control` with `fold change over control`.

### Schema version 10

* Reduce `upload_status` enum list to exclude `deposited`.
* Remove `anvil_source_url`.
* Add `anvil_url`.
* Require `controlled_access`.

### Minor changes since schema version 9

* Extend `file_format_type` enum list to include `mpra_starr`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.
* Extend `content_type` enum list to include `barcode to element mapping`.

### Schema version 9

* Extend `upload_status` enum list to include `deposited`.
* Add `controlled_access`.
* Add `anvil_source_url`.
* Add calculated property `anvil_destination_url`.

### Schema version 8

* Require `derived_from` to contain at least one value.
* Require `file_format_specifications` to contain at least one value.

### Minor changes since schema version 7

* Add calculated property `integrated_in`.

### Schema version 7

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 6

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.

### Schema version 6

* Add `GENCODE 44`, `GENCODE 45`, `GENCODE M33`, and `GENCODE M34` to `transcriptome_annotation`.
* Remove `hg19` and `mm10` from `assembly`.

### Minor changes since schema version 5

* Add `fold over change control`, `guide quantifications`, `protein to protein interaction score`, `variant to element mapping`, `element quantifications`, `elements reference`, and `variant effects` to `content_type`.
* Add `sequence barcodes` to `content_type`.
* Add `barcode to sample mapping` to `content_type`.
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
