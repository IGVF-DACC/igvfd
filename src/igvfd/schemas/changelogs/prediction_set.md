## Changelog for *`prediction_set.json`*

### Schema version 8

* Remove `publication_identifiers`.

### Minor changes since schema version 7

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Extend `file_set_type` enum list to include `binding effect`.
* Add `input_file_sets`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.
* Add calculated property `input_file_set_for`.

### Schema version 7

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 6

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.

### Schema version 6

* Remove `hg19`, `mm10`, and `mm9` from `assembly` on `small_scale_loci_list`.

### Schema version 5

* Remove `genes` and `loci`.

### Minor changes since schema version 4

* Add `MPRAbase` to `collections`.
* Add ReferenceFile linkTo to `large_scale_gene_list` and `large_scale_loci_list`.
* Add calculated `submitted_files_timestamp`.

### Schema version 4

* Rename `targeted_genes` to `genes`.
* Rename `targeted_loci` to `loci`.
* Add `small_scale_gene_list`, `large_scale_gene_list`, `small_scale_loci_list`, and `large_scale_loci_list`.
* Restrict `genes` and `loci` to submittable by admins only.


### Minor changes since schema version 3

* Add `release_timestamp`.

### Schema version 3

* Disallow empty strings in `description`.
* Allow underscores in the pattern for `chromosome` in `targeted_loci`.

### Minor changes since schema version 2

* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 2

* Require `samples` or `donors`.
