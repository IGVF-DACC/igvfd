## Changelog for *`configuration_file.json`*

### Minor changes since schema version 7

* Extend `status` enum list to include `preview`.
* Add `derived_manually`.
* Extend `file_format` enum list to include `tsv`.
* Extend `content_type` enum list to include `model parameters`.
* Extend `collections` enum list to include `VarChAMP`.
* Add calculated property `assay_titles`.
* Extend `content_type` enum list to include `scale factors`.
* Extend `file_format` enum list to include `json`.
* Update calculation of `summary`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 7

* Require `seqspec_of` to contain at least one value.
* Require `derived_from` to contain at least one value.
* Require `file_format_specifications` to contain at least one value.

### Schema version 6

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Schema version 5

* Change `seqspec_of` from a calculated property to a submittable property.

### Minor changes since schema version 4

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 4

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Require a minimum of 1 item for `dbxrefs`.

### Minor changes since schema version 1

* Add `seqspec_of`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
