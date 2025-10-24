## Changelog for *`prediction_set.json`*

### Minor changes since schema version 9

* Extend `collections` enum list to include `E2G Pillar Project`.
* Extend `collections` enum list to include `Bridge Sample`.
* Update `dbxrefs` regex to allow MaveDB score set URNs.
* Add calculated property `superseded_by`.
* Add `supersedes`.
* Add calculated property `software_versions`.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.

### Schema version 9

* Reduce `file_set_type` enum list to exclude `pathogenicity`.

### Minor changes since schema version 8

* Add `associated_phenotypes`.
* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
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
* Extend `status` enum list to include `preview`.
* Rename calculated property `input_file_set_for` to `input_for`.
* Extend `collections` enum list to include `VarChAMP`.
* Add `control_type`.
* Add `assessed_genes`.

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
