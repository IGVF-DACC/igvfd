## Changelog for *`construct_library_set.json`*

### Minor changes since schema version 4

* Add ReferenceFile linkTo to `large_scale_gene_list` and `large_scale_loci_list`.

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
