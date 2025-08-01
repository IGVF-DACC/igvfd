## Changelog for *`tabular_file.json`*

### Minor changes since schema version 17

* Extend `file_format` enum list to include `gvcf`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.
* Add calculated property `preferred_assay_titles`
* Extend `content_type` enum list to include `read count`.
* Extend `content_type` enum list to include `fold change of post-selection and pre-selection`.
* Extend `content_type` enum list to include `functional impact score`.
* Extend `file_format` enum list to include `bigBed`.

### Schema version 17

* Adjust `content_type` enum list to replace `variant functional predictions` with `variant functions`.
* Adjust `content_type` enum list to replace `element to gene predictions` with `element to gene interactions`.

### Minor changes since schema version 16

* Extend `content_type` enum list to include `derived barcode mapping`.
* Extend `base_modifications` enum list to include `Nm`.
* Extend `content_type` enum list to include `gene programs`.
* Extend `content_type` enum list to include `gene program regulators`.
* Extend `file_format` enum list to include `tar`.
* Extend `content_type` enum list to include `pipeline inputs`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 24`.
* Extend `file_format_type` enum list to include `mpra_element`.
* Extend `file_format_type` enum list to include `mpra_variant`.

### Schema version 16

* Adjust `derived_manually` to have default value `False`.

### Minor changes since schema version 15

* Extend `content_type` enum list to include `variant pathogenicity`.
* Add `base_modifications`.
* Extend `content_type` enum list to include `minus strand modification state`.
* Extend `content_type` enum list to include `plus strand modification state`.
* Add `preview_timestamp`.
* Extend `content_type` enum list to include `primers table`.
* Extend `content_type` enum list to include `primers track`.
* Extend `content_type` enum list to include `target transcripts`.
* Extend `content_type` enum list to include `barcode replacement`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Add calculated property `primer_design_for`.
* Extend `file_format` enum list to include `bedpe`.
* Extend `content_type` enum list to include `machine learning model features`.
* Extend `content_type` enum list to include `element to gene predictions`.

### Schema version 15

* Reduce `content_type` enum list to exclude `sequence barcodes`.

### Schema version 14

* Adjust `transcriptome_annotation` enum list to replace `GENCODE 28, GENCODE M17` with `GENCODE 32, GENCODE M23`.

### Minor changes since schema version 13

* Allow `controlled_access` files to be released without `anvil_url`.
* Extend `content_type` enum list to include `primer sequences`.
* Add `catalog_adapters`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 28`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M25`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M17`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 28, GENCODE M17`.
* Extend `assembly` enum list to include `hg19`.
* Extend `assembly` enum list to include `mm10`.
* Extend `assembly` enum list to include `GRCh38, mm10`.
* Extend `content_type` enum list to include `differential peak quantifications`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 22`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 47`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M36`.
* Add `filtered`.
* Add `workflow`.
* Extend `content_type` enum list to include `reporter experiment barcode`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Add `checkfiles_version`.
* Extend `content_type` enum list to include `DNA footprint scores`.
* Extend `content_type` enum list to include `cell hashing barcodes`.
* Extend `content_type` enum list to include `unfiltered local differential expression`.
* Extend `content_type` enum list to include `unfiltered global differential expression`.
* Extend `upload_status` enum list to include `validation exempted`.
* Extend `status` enum list to include `preview`.
* Extend `content_type` enum list to include `barcode onlist`.
* Update calculation of `summary`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 32`.
* Extend `content_type` enum list to include `differential chromatin contact quantifications`.
* Extend `content_type` enum list to include `variant functional predictions`.
* Extend `assembly` enum list to include `custom`.
* Extend `content_type` enum list to include `bin paired count`.

### Schema version 13

* Adjust `file_format` enum list to remove `txt`.

### Minor changes since schema version 12

* Extend `content_type` enum list to include `reporter elements`.
* Extend `content_type` enum list to include `reporter experiment`.
* Extend `content_type` enum list to include `reporter variants`.
* Extend `content_type` enum list to include `reporter genomic element effects`.
* Extend `content_type` enum list to include `reporter genomic variant effects`.
* Extend `content_type` enum list to include `differential element quantifications`.
* Add `derived_manually`.
* Adjust `file_format` enum list to restrict usage of `txt` to admin users.
* Extend `collections` enum list to include `VarChAMP`.
* Extend `content_type` enum list to include `barcode to TF overexpression mapping`.
* Extend `content_type` enum list to include `coding variant effects`.
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
