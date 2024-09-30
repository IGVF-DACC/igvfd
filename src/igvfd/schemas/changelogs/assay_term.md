## Changelog for *`assay_term.json`*
### Schema version 8

* Extend `preferred_assay_titles` enum list to include `Variant painting via immunostaining`.
* Extend `preferred_assay_titles` enum list to include `Variant painting via fluorescence`.
* Adjust `preferred_assay_title` enum list to remove `Variant painting`.

### Minor changes since schema version 7

* Extend `preferred_assay_titles` enum list to include `VAMP-seq (MultiSTEP)`.
* Extend `preferred_assay_titles` enum list to include `STARR-seq`.
* Extend `preferred_assay_titles` enum list to include `scCRISPR screen`.

### Schema version 7

* Adjust `preferred_assay_titles` enum list to replace `CRISPR FlowFISH` with `CRISPR FlowFISH screen`.
* Extend `preferred_assay_titles` enum list to include `Proliferation CRISPR screen`.
* Extend `preferred_assay_titles` enum list to include `Growth CRISPR screen`.
* Extend `preferred_assay_titles` enum list to include `Migration CRISPR screen`.
* Extend `preferred_assay_titles` enum list to include `CRISPR FACS screen`.
* Extend `preferred_assay_titles` enum list to include `CRISPR mCherry screen`.
* Extend `preferred_assay_titles` enum list to include `HCR-FlowFISH screen`.

### Minor changes since schema version 6

* Extend `preferred_assay_titles` enum list to include `Spatial transcriptomics`.
* Update calculation of `summary`.
* Extend `preferred_assay_titles` enum list to include `scNT-seq2`.

### Schema version 6

* Require `preferred_assay_titles` to contain at least one value.

### Schema version 5

* Adjust `preferred_assay_titles` enum list to replace `histone ChIP-seq` with `Histone ChIP-seq`.
* Adjust `preferred_assay_titles` enum list to replace `Parse Split-seq` with `Parse SPLiT-seq`.
* Adjust `preferred_assay_titles` enum list to replace `Saturation genome editing` with `SGE`.
* Adjust `preferred_assay_titles` enum list to replace `SHARE-Seq` with `SHARE-seq`.
* Adjust `preferred_assay_titles` enum list to replace `Yeast two-hybrid` with `Y2H`.

### Schema version 4

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 3

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `preferred_assay_titles`.
* Add `release_timestamp`.
* Add `ATAC-seq`, `RNA-seq`, `TF ChIP-seq`, `histone ChIP-seq`, `snRNA-seq`, `scRNA-seq`, `snATAC-seq` and `scATAC-seq` to `preferred_assay_titles`.
* Add `archived` to `status`.

### Schema version 3

* Disallow empty strings in `description`.

### Minor changes since schema version 2

* Add calculated property `ontology`.
* Add `description`.
* Add `is_a`.

### Schema version 2

* Restrict `aliases` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add calculated property `ancestors`.
* Rename schema `assay_ontology_term.json` to `assay_term.json`.
* Add `submitter_comment`, `submitted_by` and `creation_timestamp`.
