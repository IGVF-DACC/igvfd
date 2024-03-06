## Changelog for *`prediction_set.json`*

### Schema version 7

* Objects with released, archived or revoked status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

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
