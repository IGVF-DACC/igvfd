## Changelog for *`tabular_file.json`*

### Minor changes since schema version 5

* Add `fold over change control`, `guide quantifications`, `variant to element mapping`, `element quantifications`, `elements reference`, and `quantified variant effects` to `content_type` to `content_type`.
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
