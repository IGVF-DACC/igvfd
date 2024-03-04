## Changelog for *`genome_browser_annotation_file.json`*

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
