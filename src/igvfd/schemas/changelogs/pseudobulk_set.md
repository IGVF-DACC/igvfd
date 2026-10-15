## Changelog for *`pseudobulk_set.json`*

### Schema version 3

* Extend `file_set_type` enum list to include `gene expression pseudobulk`.
* Extend `file_set_type` enum list to include `demultiplexed pseudobulk`.
* Extend `file_set_type` enum list to include `accessibility pseudobulk`.
* Adjust `file_set_type` enum list to remove `pseudobulk analysis`.

### Minor changes since schema version 2

* Update `aliases` regex to add `jacob-schreiber` as a namespace.
* Extend `collections` enum list to include `IGVF_catalog_v1.3`.
* Extend `collections` enum list to include `10x V2F`.
* Extend `collections` enum list to include `SHARE CIRM Villages`.
* Extend `collections` enum list to include `SHARE DepMap`.
* Extend `collections` enum list to include `IGVF_catalog_v2.0`.
* Add `url`.
* Extend `collections` enum list to include `Cross-Disorder CNVs`.
* Extend `collections` enum list to include `Coronary Artery Disease`.
* Update `samples` to allow linking to MultiplexedSample.

### Schema version 2

* Add `merged`.

### Minor changes since schema version 1

* Add calculated property `donors`.
* Add calculated property `preferred_assay_slims`.
* Update `aliases` regex to add `hongbo-liu` as a namespace.
* Add `is_on_anvil`.
* Extend `input_file_sets` to include curated sets.
