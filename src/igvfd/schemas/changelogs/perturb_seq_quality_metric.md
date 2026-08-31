## Changelog for *`perturb_seq_quality_metric.json`*

### Schema version 2

* Rename `pct_cells_assigned_guide` to `frac_cells_with_guide`.
* Rename `avg_cells_per_target` to `avg_cells_per_guide`.
* Rename `mean_mitochondrial_reads` to `mean_percent_mitochondrial`.
* Remove `total_targets`.
* Add `n_targets`.
* Add `n_unique`.
* Add `p_unique`.
* Add `percentage_barcodes_on_onlist`.
* Add `percentage_reads_on_onlist`.
* Add `mean_umis_per_barcode`.
* Add `umi_median`.
* Add `genes_median`.
* Add `n_cells_with_guide`.
* Add `n_cells_exactly_1_guide`.
* Add `guide_umi_mean`.
* Remove `guide_diversity`.

### Minor changes since schema version 1

* Update `aliases` regex to add `hongbo-liu` as a namespace.
* Update `aliases` regex to add `yang-li` as a namespace.
* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Adjust `quality_metric_of` to allow usage by all users.
