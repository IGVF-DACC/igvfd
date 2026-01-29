## Changelog for *`gene.json`*

### Minor changes since schema version 10

* Add `allele`.
* Extend `collections` enum list to include `E2G Pillar Project`.
* Extend `collections` enum list to include `Bridge Sample`.
* Extend `locations.assembly` enum list to include `C57BL_6J_T2T_v1 + GRCm39_X`.
* Extend `locations.assembly` enum list to include `CAST_EiJ_T2T_v1`.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 24`.
* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.

### Schema version 10

* Adjust `transcriptome_annotation` enum list to replace `GENCODE 28, GENCODE M17` with `GENCODE 32, GENCODE M23`.

### Minor changes since schema version 9

* Update required properties to remove `dbxrefs`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 28`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M25`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M17`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 28, GENCODE M17`.
* Extend `locations.assembly` enum list to include `hg19`.
* Extend `locations.assembly` enum list to include `mm10`.
* Extend `locations.assembly` enum list to include `GRCh38, mm10`.
* Update `chromosome` regex in `locations` to allow genes not on standard chromosomes.
* Extend `transcriptome_annotation` enum list to include `GENCODE 22`.
* Add `collections`.
* Add `study_sets`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 47`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M36`.
* Extend `status` enum list to include `preview`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 32`.
* Extend `locations.assembly` enum list to include `custom`.
* Update calculation of `summary`.

### Schema version 9

* Require `synonyms` to have a minimum of one value.

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
