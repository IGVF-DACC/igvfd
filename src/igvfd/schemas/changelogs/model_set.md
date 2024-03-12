## Changelog for *`model_set.json`*

### Schema version 3

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 2

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.
* Add calculated `submitted_files_timestamp`.

### Schema version 2

* Disallow empty strings in `description`.

### Minor changes since schema version 1
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
