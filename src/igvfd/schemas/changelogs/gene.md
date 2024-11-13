## Changelog for *`gene.json`*

### Minor changes since schema version 8

* Extend `transcriptome_annotation` enum list to include `GENCODE 32`.
* Extend `locations.assembly` enum list to include `custom`.
* Update calculation of `summary`.

### Schema version 8

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 7

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.

### Schema version 7

* Remove `hg19`, `mm10`, and `mm9` from `assembly` on `locations`.

### Minor changes since schema version 6

* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 6

* Disallow empty strings in `description`.

### Schema version 5

* Rename `annotation_version` to `transcriptome_annotation`. Add two new enums `GENCODE 40` and `GENCODE 41`.

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
