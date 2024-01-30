## Changelog for *`auxiliary_set.json`*

### Minor changes since schema version 6

* Add `release_timestamp`.

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
