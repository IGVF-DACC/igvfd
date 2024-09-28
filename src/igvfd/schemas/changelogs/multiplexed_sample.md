## Changelog for *`multiplexed_sample.json`*

### Schema version 10

* Add required property `multiplexing_method`.

### Schema version 9

* Rename `barcode_sample_map` to `barcode_map`.

### Schema version 8

* Remove `publication_identifiers`.

### Minor changes since schema version 7

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Allow calculated property `modifications` to link to `Crispr Modifications`.
* Add `protocols`.
* Update `dbxrefs` regex to allow ENCODE sample accessions.

### Schema version 7

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 6

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `barcode_sample_map`.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 6

* Disallow empty strings in `description`.

### Schema version 5

* Rename `sorted_fraction` to `sorted_from`.
* Rename `sorted_fraction_detail` to `sorted_from_detail`.

### Minor changes since schema version 4

* Add `summary`.
* Add `construct_library_sets`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 4

* Mutually require `starting_amount` and `starting_amount_units`.

### Schema version 3

* Rename `biosample_terms` to `sample_terms`.

### Schema version 2

* Remove `product_id`, `lot_id`, and convert `sources` to a calculated property.

### Minor changes since schema version 1

* Add `publication_identifiers`.
