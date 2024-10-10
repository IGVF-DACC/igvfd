## Changelog for *`construct_library_set.json`*

### Schema version 10

* Fully restrict linkTo for `integrated_content_files` to ReferenceFile and TabularFile.

### Minor changes since schema version 9

* Extend `collections` enum list to include `VarChAMP`.
* Add `control_type`.

### Schema version 9

* Remove `publication_identifiers`.

### Minor changes since schema version 8

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Extend `scope` enum list to include `alleles`.
* Extend `scope` enum list to include `targeton`.
* Extend `file_set_type` enum list to include `editing template library`.
* Add `targeton`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.
* Add calculated property `input_file_set_for`.
* Add `orf_list`.
* Extend `scope` enum list to include `interactors`.

### Schema version 8

* Restrict linkTo for `integrated_content_files` to ReferenceFile and TabularFile, other file types are submittable by admins only.

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

* Add `small_scale_gene_list`, `large_scale_gene_list`, `small_scale_loci_list`, and `large_scale_loci_list`.
* Restrict `genes` and `loci` to submittable by admins only.

### Minor changes since schema version 3

* Add a `title` property to `tile`.
* Allow underscores in the pattern for `chromosome` in `loci`.
* Add `release_timestamp`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Add `tile` enum to `file_set_type` and descriptive `tile` property.
* Disallow empty strings in `exon` property.

### Minor changes since schema version 1

* Add `summary` and `applied_to_samples`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
