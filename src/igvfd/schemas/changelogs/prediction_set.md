## Changelog for *`prediction_set.json`*

### Schema version 4

* Replace `genes` with `small_scale_gene_list` and `large_scale_gene_list`.
* Add `small_scale_gene_list` and `large_scale_gene_list`.
* Rename `targeted_genes` to `genes`.
* Rename `targeted_loci` to `loci`.


### Minor changes since schema version 3

* Add `release_timestamp`.

### Schema version 3

* Disallow empty strings in `description`.
* Allow underscores in the pattern for `chromosome` in `targeted_loci`.

### Minor changes since schema version 2

* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 2

* Require `samples` or `donors`.
