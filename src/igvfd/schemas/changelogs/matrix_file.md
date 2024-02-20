## Changelog for *`matrix_file.json`*

### Minor changes since schema version 4

* Expand `file_format` enum list to include `hic`.
* Expand `dimension1` and `dimension2` enum lists to include `genomic position`.
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
