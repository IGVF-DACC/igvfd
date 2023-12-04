## Changelog for *`construct_library_set.json`*

### Schema version 3

* Disallow empty strings in `description`.

### Minor changes since schema version 2

* Add a `title` property to the `tile` property to prevent a UI crash.

### Schema version 2

* Add `tile` enum to `file_set_type` and descriptive `tile` property.
* Disallow empty strings in `exon` property.

### Minor changes since schema version 1

* Add `summary` and `applied_to_samples`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
