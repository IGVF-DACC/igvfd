## Changelog for *`curated_set.json`*

### Minor changes since schema version 8

* Add `control_type`.

### Schema version 8

* Remove `publication_identifiers`.

### Minor changes since schema version 7

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Extend `file_set_type` enum list to include `editing templates`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.
* Add calculated property `input_file_set_for`.

### Schema version 7

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 6

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.
* Add `barcodes` to `file_set_type`.

### Schema version 6

* Disallow empty strings in `description`.

### Minor changes since schema version 5

* Rename `assembly` to `assemblies`.
* Rename `transcriptome_annotation` to `transcriptome_annotations`.
* Expand `file_set_type` enum list to include `external data for catalog`.

### Schema version 5

* Rename `curated_set_type` to `file_set_type`.
* Make `samples` and `donors` mutually exclusive.

### Minor changes since schema version 4

* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 4

* Rename `references` to `publication_identifiers`.

### Minor changes since schema version 3

* Add `files`.
* Add `dbxrefs`.
* Add `guide RNAs` to `curated_set_type`.
* Add `control_for`.

### Schema version 3

* Change `accessionType` to `DS`

### Schema version 2

* Rename `sample` to `samples`.
* Rename `donor` to `donors`.
