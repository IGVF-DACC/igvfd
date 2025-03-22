## Changelog for *`auxiliary_set.json`*

### Minor changes since schema version 12

* Add calculated property `data_use_limitation_summaries`.
* Add calculated property `controlled_access`.
* Add calculated property `construct_library_sets`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.

### Schema version 12

* Adjust `file_set_type` enum list to remove `variant sequencing`.

### Minor changes since schema version 11

* Extend `status` enum list to include `preview`.
* Rename calculated property `input_file_set_for` to `input_for`.
* Extend `collections` enum list to include `VarChAMP`.
* Add `barcode_map`.
* Extend `file_set_type` enum list to include `MORF barcode sequencing`.
* Add `control_type`.

### Schema version 11

* Rename `file_set_type` enum `cell hashing` to `cell hashing barcode sequencing`.
* Rename `file_set_type` enum `oligo-conjugated lipids` to `lipid-conjugated oligo sequencing`.

### Schema version 10

* Remove `library_construction_platform`.

### Schema version 9

* Remove `publication_identifiers`.

### Schema version 8

* Rename `file_set_type` enum `circularized barcode detection` to `circularized RNA barcode detection`.
* Rename `file_set_type` enum `quantification barcode sequencing` to `quantification DNA barcode sequencing`.

### Minor changes since schema version 7

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Extend `file_set_type` enum list to include `cell sorting`.
* Extend `file_set_type` enum list to include `variant sequencing`.
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
* Add calculated `submitted_files_timestamp`.

### Schema version 6

* Remove `oligo-conjugated antibodies` from `file_set_type` property.

### Schema version 5

* Disallow empty strings in `description`.

### Schema version 4

* Remove `moi` and `construct_libraries` properties.

### Minor changes since schema version 3

* Restrict `moi` and `construct_libraries` to submittable by admins only. These properties will be moved to Sample objects.
* Convert `donors` to be calculated from `samples`.

### Schema version 3

* Rename `auxiliary_type` to `file_set_type`.

### Minor changes since schema version 2

* Add `circularized barcode detection`, `quantification barcode sequencing` enum to `auxiliary_type` property.
* Add `measurement_sets`.

### Schema version 2

* Rename `references` to `publication_identifiers`.

### Minor changes since schema version 1

* Add `cell hashing` enum to `auxiliary_type` property.
