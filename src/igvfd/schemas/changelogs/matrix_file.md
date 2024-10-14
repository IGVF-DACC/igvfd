## Changelog for *`matrix_file.json`*

### Minor changes since schema version 7

* Add property `derived_manually`.
* Extend `collections` enum list to include `VarChAMP`.

### Schema version 7

* Extend `secondary_dimensions` enum list to include `gene expression`.
* Extend `secondary_dimensions` enum list to include `CRISPR guide capture`.
* Extend `secondary_dimensions` enum list to include `antibody capture`.
* Change type of `secondary_dimensions` to be an array.
* Rename `dimension2` to `secondary_dimensions`.
* Rename `dimension1` to `principal_dimension`.

### Minor changes since schema version 6

* Add calculated property `assay_titles`.
* Extend `content_type` enum list to include `raw feature barcode matrix`.
* Extend `content_type` enum list to include `filtered feature barcode matrix`.
* Update calculation of `summary`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 6

* Require `derived_from` to contain at least one value.
* Require `file_format_specifications` to contain at least one value.

### Schema version 5

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 4

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `hic` to `file_format`.
* Add `genomic position` to `dimension1` and `dimension2`.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 4

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 3

* Disallow empty strings in `description`.

### Minor changes since schema version 2

* Expand `file_format` enum list to include `tar`.

### Schema version 2

* Require a minimum of 1 item for `dbxrefs`.

### Minor changes since schema version 1

* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
