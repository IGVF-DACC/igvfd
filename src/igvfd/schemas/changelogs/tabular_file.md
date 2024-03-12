## Changelog for *`tabular_file.json`*

### Schema version 7

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.
* Add calculated property `integrated_in`.

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
* Add `integrated_in`.

### Schema version 5

* Require `assembly` if `file_format` is one of `bam`, `bed`, `bedpe`, `bigWig`, `bigBed`, `bigInteract`, `tabix`, or `vcf`.

### Schema version 4

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Require a minimum of 1 item for `dbxrefs`.
