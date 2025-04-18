## Changelog for *`single_cell_atac_seq_quality_metric.json`*

### Minor changes since schema version 2

* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.

### Schema version 2

* Remove `n_fragment`.
* Remove `frac_dup`.
* Remove `frac_mito`.
* Remove `tsse`.
* Remove `duplicate`.
* Remove `unmapped`.
* Remove `lowmapq`.

### Minor changes since schema version 1

* Add `atac_fragments_alignment_stats`.
* Add `atac_bam_summary_stats`.
* Add `atac_fragment_summary_stats`.
* Adjust `quality_metric_of` to allow usage by all users.
* Add `uni_mappings`.
* Add `multi_mappings`.
