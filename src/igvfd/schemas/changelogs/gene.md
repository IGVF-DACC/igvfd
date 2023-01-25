## Changelog for *`gene.json`*

### Minor changes since schema version 3

* Add `GRCM39` to `locations` assemblies

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
