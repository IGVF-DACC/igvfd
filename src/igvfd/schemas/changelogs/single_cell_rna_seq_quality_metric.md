## Changelog for *`single_cell_rna_seq_quality_metric.json`*

### Schema version 2

* Remove `frac_dup`.
* Remove `frac_mito`.
* Remove `frac_mito_genes`.
* Remove `frac_reads_in_genes_barcode`.
* Remove `frac_reads_in_genes_library`.
* Remove `joint_barcodes_passing`.
* Remove `median_genes_per_barcode`.
* Remove `n_genes`.
* Remove `pct_duplicates`.

### Minor changes since schema version 1

* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Add `rnaseq_kb_info`.
* Add `n_targets`.
* Add `n_bootstraps`.
* Add `n_processed`.
* Add `n_pseudoaligned`.
* Add `n_unique`.
* Add `p_pseudoaligned`.
* Add `p_unique`.
* Add `index_version`.
* Add `k-mer length`.
* Adjust `quality_metric_of` to allow usage by all users.
