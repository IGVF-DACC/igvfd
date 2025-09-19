## Changelog for *`multiplexed_sample.json`*

### Minor changes since schema version 10

* Restrict `moi` to submission by admins only.
* Restrict `nucleic_acid_delivery` to submission by admins only.
* Restrict `time_post_library_delivery` to submission by admins only.
* Restrict `time_post_library_delivery_units` to submission by admins only.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.
* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `nucleic_acid_delivery` enum list to include `nucleofection`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `nucleic_acid_delivery` enum list to include `lipofectamine`.
* Extend `nucleic_acid_delivery` enum list to include `electroporation`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Extend `status` enum list to include `preview`.
* Add calculated property `taxa`.
* Extend `collections` enum list to include `VarChAMP`.

### Schema version 10

* Add required property `multiplexing_methods`.

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
