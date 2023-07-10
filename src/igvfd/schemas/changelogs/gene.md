## Changelog for *`gene.json`*

### Schema version 5

* Add `transcriptome_annotation`.
* Remove `annotation_version`.

### Schema version 4

* Change regex pattern of  `geneid`.
* Add `version_number`.
* Add `annotation_version`.

### Minor changes since schema version 3

* Add `GRCm39` to `locations.assembly`

### Schema version 3

* Remove `ncbi_entrez_status`.
* Change `geneID` to use ENSEMBL ID instead of NCBI Entrez ID.

### Minor changes since schema version 2

* Add `description`.
* Add `aliases` to `identifyingProperties`.

### Schema version 2

* Restrict `aliases` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add `submitter_comment`, `submitted_by`, `creation_timestamp` and `aliases`.
* Rename `organism` to `taxa`.
