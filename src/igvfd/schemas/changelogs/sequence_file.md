## Changelog for *`sequence_file.json`*

### Schema version 12

* Add `upload_status` of `deposited`.
* Add `controlled_access`.

### Minor changes since schema version 11

* Add `sequencing_kit`.

### Schema version 11

* Require `derived_from` to contain at least one value.
* Require `file_format_specifications` to contain at least one value.

### Schema version 10

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Schema version 9

* Remove `seqspec`.
* Add calculated property `seqspecs`.

### Minor changes since schema version 8

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.

### Schema version 8

* Replace `subreads` with `PacBio subreads` in `content_type`.
* Expand `content_type` enum list to include `Nanopore reads`.

### Minor changes since schema version 7

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 7

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 6

* Disallow empty strings in `description`.

### Minor changes since schema version 5

* Allow hyphens in `dbxrefs`.

### Schema version 5

* Require a minimum of 1 item for `dbxrefs`.

### Minor changes since schema version 4

* Add `index`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 4

* Restrict `minimum_read_length` to a maximum value of 300000000.
* Restrict `maximum_read_length` to a maximum value of 300000000.
* Restrict `mean_read_length` to a maximum value of 300000000.
* Change `mean_read_length` type to number.

### Minor changes since schema version 3

* Add `seqspec`.

### Schema version 3

* Require `sequencing_platform`.
* Add `flowcell_id` and `lane`.
