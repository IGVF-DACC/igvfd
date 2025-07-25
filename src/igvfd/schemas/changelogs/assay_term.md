## Changelog for *`assay_term.json`*

### Schema version 18

* Adjust `preferred_assay_titles` enum list to replace `Parse Perturb-seq` with `CC-Perturb-seq`.

### Minor changes since schema version 17

* Extend `preferred_assay_titles` enum list to include `Immune-SGE`.
* Extend `preferred_assay_titles` enum list to include `LABEL-seq`.

### Schema version 17

* Extend `preferred_assay_titles` enum list to include `scNT-seq3`.
* Adjust `preferred_assay_titles` enum list to replace `10X ATAC with Scale pre-indexing` with `10x with Scale pre-indexing`.
* Adjust `preferred_assay_titles` enum list to replace `10X RNA with Scale pre-indexing` with `10x with Scale pre-indexing`.

### Minor changes since schema version 16

* Extend `preferred_assay_titles` enum list to include `CUT&RUN`.
* Extend `preferred_assay_titles` enum list to include `Bisulfite-seq`.

### Schema version 16

* Adjust `preferred_assay_titles` enum list to replace `mN2H` with `Arrayed mN2H`.
* Adjust `preferred_assay_titles` enum list to replace `semi-qY2H` with `Arrayed semi-qY2H v1`.
* Adjust `preferred_assay_titles` enum list to replace `Y2H` with `Arrayed Y2H v1`.
* Adjust `preferred_assay_titles` enum list to replace `yN2H` with `Arrayed yN2H`.
* Extend `preferred_assay_titles` enum list to include `Arrayed Y2H v2`.
* Extend `preferred_assay_titles` enum list to include `Arrayed Y2H v3`.
* Extend `preferred_assay_titles` enum list to include `Pooled Y2H v1`.
* Extend `preferred_assay_titles` enum list to include `Pooled Y2H v2`.
* Extend `preferred_assay_titles` enum list to include `Pooled Y2H v3`.
* Extend `preferred_assay_titles` enum list to include `Arrayed semi-qY2H v2`.
* Extend `preferred_assay_titles` enum list to include `Arrayed semi-qY2H v3`.


### Schema version 15

* Adjust `preferred_assay_titles` enum list to remove `CERES-seq`.

### Minor changes since schema version 14

* Extend `preferred_assay_titles` enum list to include `Parse Perturb-seq`.

### Schema version 14

* Adjust `preferred_assay_titles` enum list to replace `10x multiome with scMito-seq` with `mtscMultiome`.

### Schema version 13

* Adjust `preferred_assay_titles` enum list to remove `SUPERSTARR`.

### Minor changes since schema version 12

* Add `preview_timestamp`.

### Schema version 12

* Add calculated `comments`.
* Add calculated `definition`.
* Remove `comment`.
* Remove `definition`.

### Minor changes since schema version 11

* Extend `preferred_assay_titles` enum list to include `scMultiome-NT-seq`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.

### Schema version 11

* Extend `preferred_assay_titles` enum list to include `10X ATAC with Scale pre-indexing`.
* Extend `preferred_assay_titles` enum list to include `10X RNA with Scale pre-indexing`.
* Adjust `preferred_assay_titles` enum list to remove `Growth CRISPR screen`.

### Schema version 10

* Adjust `preferred_assay_titles` enum list to replace `scMito-seq` with `10x multiome with scMito-seq`.

### Minor changes since schema version 9

* Add `comment`.
* Add `definition`.
* Extend `preferred_assay_titles` enum list to include `ACCESS-ATAC`.
* Extend `preferred_assay_titles` enum list to include `scACCESS-ATAC`.
* Extend `preferred_assay_titles` enum list to include `CRISPR MACS screen`.
* Extend `preferred_assay_titles` enum list to include `scMito-seq`.
* Extend `preferred_assay_titles` enum list to include `WGS`.
* Extend `preferred_assay_titles` enum list to include `electroporated MPRA`.
* Extend `preferred_assay_titles` enum list to include `varACCESS`.

### Schema version 9

* Adjust `preferred_assay_titles` enum list to replace `Variant FlowFISH` with `Variant-EFFECTS`.

### Minor changes since schema version 8

* Extend `status` enum list to include `preview`.
* Extend `preferred_assay_titles` enum list to include `HiCAR`.
* Extend `preferred_assay_titles` enum list to include `ONT dRNA`.
* Extend `preferred_assay_titles` enum list to include `ONT Fiber-seq`.
* Extend `preferred_assay_titles` enum list to include `ONT direct WGS`.

### Schema version 8

* Extend `preferred_assay_titles` enum list to include `Variant painting via immunostaining`.
* Extend `preferred_assay_titles` enum list to include `Variant painting via fluorescence`.
* Adjust `preferred_assay_titles` enum list to remove `Variant painting`.

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
