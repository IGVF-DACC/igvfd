## Changelog for *`measurement_set.json`*

### Schema version 34

* Extend `preferred_assay_title` enum list to include `scNT-seq3`.
* Adjust `preferred_assay_title` enum list to replace `10X ATAC with Scale pre-indexing` with `10x with Scale pre-indexing`.
* Adjust `preferred_assay_title` enum list to replace `10X RNA with Scale pre-indexing` with `10x with Scale pre-indexing`.

### Schema version 33

* Add `control_types`.
* Remove `control_type`.
* Extend `control_type` enum list to include `wildtype`.

### Schema version 32

* Adjust `control_type` enum list to remove `pre-selection`.

### Minor changes since schema version 31

* Extend `preferred_assay_title` enum list to include `CUT&RUN`.
* Extend `preferred_assay_title` enum list to include `Bisulfite-seq`.

### Schema version 31

* Adjust `preferred_assay_title` enum list to replace `mN2H` with `Arrayed mN2H`.
* Adjust `preferred_assay_title` enum list to replace `semi-qY2H` with `Arrayed semi-qY2H v1`.
* Adjust `preferred_assay_title` enum list to replace `Y2H` with `Arrayed Y2H v1`.
* Adjust `preferred_assay_title` enum list to replace `yN2H` with `Arrayed yN2H`.
* Extend `preferred_assay_title` enum list to include `Arrayed Y2H v2`.
* Extend `preferred_assay_title` enum list to include `Arrayed Y2H v3`.
* Extend `preferred_assay_title` enum list to include `Pooled Y2H v1`.
* Extend `preferred_assay_title` enum list to include `Pooled Y2H v2`.
* Extend `preferred_assay_title` enum list to include `Pooled Y2H v3`.
* Extend `preferred_assay_title` enum list to include `Arrayed semi-qY2H v2`.
* Extend `preferred_assay_title` enum list to include `Arrayed semi-qY2H v3`.

### Schema version 30

* Adjust `preferred_assay_title` enum list to remove `CERES-seq`.

### Minor changes since schema version 29

* Extend `preferred_assay_title` enum list to include `Parse Perturb-seq`.

### Schema version 29

* Adjust `preferred_assay_title` enum list to replace `10x multiome with scMito-seq` with `mtscMultiome`.

### Schema version 28

* Adjust `preferred_assay_title` enum list to remove `SUPERSTARR`.

### Schema version 27

* Adjust `control_type` enum list to replace `control transduction` with `reference transduction`.

### Minor changes since schema version 26

* Add `preview_timestamp`.
* Extend `control_type` enum list to include `baseline`.
* Add `barcode_replacement_file`.
* Extend `preferred_assay_title` enum list to include `scMultiome-NT-seq`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Add `primer_designs`.
* Extend `preferred_assay_title` enum list to include `10X ATAC with Scale pre-indexing`.
* Extend `preferred_assay_title` enum list to include `10X RNA with Scale pre-indexing`.

### Schema version 26

* Adjust `strand_specificity` enum list to replace `5' to 3'` with `5 prime to 3 prime`.
* Adjust `strand_specificity` enum list to replace `3' to 5'` with `3 prime to 5 prime`.

### Minor changes since schema version 25

* Add calculated property `data_use_limitation_summaries`.
* Add calculated property `controlled_access`.
* Add `strand_specificity`.

### Schema version 25

* Adjust `preferred_assay_title` enum list to remove `Growth CRISPR screen`.

### Schema version 24

* Adjust `preferred_assay_title` enum list to replace `scMito-seq` with `10x multiome with scMito-seq`.

### Minor changes since schema version 23

* Extend `control_type` enum list to include `untreated`.
* Extend `control_type` enum list to include `non-targeting`.
* Add calculated property `construct_library_sets`.
* Extend `preferred_assay_title` enum list to include `ACCESS-ATAC`.
* Extend `preferred_assay_title` enum list to include `scACCESS-ATAC`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `preferred_assay_title` enum list to include `CRISPR MACS screen`.
* Extend `preferred_assay_title` enum list to include `scMito-seq`.
* Extend `preferred_assay_title` enum list to include `WGS`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Add `onlist_files`.
* Add `onlist_method`.
* Extend `preferred_assay_title` enum list to include `electroporated MPRA`.
* Extend `preferred_assay_title` enum list to include `varACCESS`.
* Update calculation of `summary`.

### Schema version 23

* Adjust `preferred_assay_title` enum list to replace `Variant FlowFISH` with `Variant-EFFECTS`.

### Minor changes since schema version 22

* Extend `status` enum list to include `preview`.
* Extend `control_type` enum list to include `control transduction`.
* Rename calculated property `input_file_set_for` to `input_for`.
* Add calculated property `externally_hosted`.
* Extend `preferred_assay_title` enum list to include `HiCAR`.
* Extend `preferred_assay_title` enum list to include `ONT dRNA`.
* Extend `preferred_assay_title` enum list to include `ONT Fiber-seq`.
* Extend `preferred_assay_title` enum list to include `ONT direct WGS`.
* Extend `collections` enum list to include `VarChAMP`.

### Schema version 22

* Extend `preferred_assay_title` enum list to include `Variant painting via immunostaining`.
* Extend `preferred_assay_title` enum list to include `Variant painting via fluorescence`.
* Adjust `preferred_assay_title` enum list to remove `Variant painting`.

### Minor changes since schema version 21

* Extend `preferred_assay_title` enum list to include `VAMP-seq (MultiSTEP)`.
* Add `functional_assay_mechanisms`.
* Extend `preferred_assay_title` enum list to include `STARR-seq`.

### Schema version 21

* Require `preferred_assay_title`.
* Extend `preferred_assay_title` enum list to include `scCRISPR screen`.

### Schema version 20

* Adjust `preferred_assay_title` enum list to replace `CRISPR FlowFISH` with `CRISPR FlowFISH screen`.
* Extend `preferred_assay_title` enum list to include `Proliferation CRISPR screen`.
* Extend `preferred_assay_title` enum list to include `Growth CRISPR screen`.
* Extend `preferred_assay_title` enum list to include `Migration CRISPR screen`.
* Extend `preferred_assay_title` enum list to include `CRISPR FACS screen`.
* Extend `preferred_assay_title` enum list to include `CRISPR mCherry screen`.
* Extend `preferred_assay_title` enum list to include `HCR-FlowFISH screen`.

### Minor changes since schema version 19

* Add `control_type`.

### Schema version 19

* Remove `library_construction_platform`.

### Minor changes since schema version 18

* Extend `preferred_assay_title` enum list to include `Spatial transcriptomics`.

### Schema version 18

* Remove `publication_identifiers`.

### Minor changes since schema version 17

* Extend `preferred_assay_title` enum list to include `HT-recruit`.
* Extend `preferred_assay_title` enum list to include `Hi-C`.
* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Add `targeted_genes`.
* Add `external_image_url`.

### Schema version 17

* Remove `readout`.

### Schema version 16

* Restrict `samples` to 1 item.

### Minor changes since schema version 15

* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.
* Add calculated property `input_file_set_for`.
* Extend `preferred_assay_title` enum list to include `scNT-seq2`.

### Schema version 15

* Require `auxiliary_sets` to contain at least one value.
* Require `control_file_sets` to contain at least one value.
* Require `protocols` to contain at least one value.
* Require `sequencing_library_types` to contain at least one value.

### Schema version 14

* Adjust `preferred_assay_title` enum list to replace `histone ChIP-seq` with `Histone ChIP-seq`.
* Adjust `preferred_assay_title` enum list to replace `Parse Split-seq` with `Parse SPLiT-seq`.
* Adjust `preferred_assay_title` enum list to replace `Saturation genome editing` with `SGE`.
* Adjust `preferred_assay_title` enum list to replace `SHARE-Seq` with `SHARE-seq`.
* Adjust `preferred_assay_title` enum list to replace `Yeast two-hybrid` with `Y2H`.
* Extend `preferred_assay_title` enum list to include `MPRA`.

### Schema version 13

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 12

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.
* Add `ATAC-seq`, `RNA-seq`, `TF ChIP-seq`, `histone ChIP-seq`, `snRNA-seq`, `scRNA-seq`, `snATAC-seq` and `scATAC-seq` to `preferred_assay_title`.
* Add calculated `submitted_files_timestamp`.

### Schema version 12

* Replace `protocol` with `protocols`.

### Schema version 11

* Add `file_set_type`.

### Schema version 10

* Disallow empty strings in `description`.

### Minor changes since schema version 9

* Expand `preferred_assay_title` enum list to include `snM3C-seq`.

### Schema version 9

* Rename `sequencing_library_type` to `sequencing_library_types`.

### Schema version 8

* Change `multiome_size` to integer type.

### Schema version 7

* Remove `nucleic_acid_delivery`, `moi`, and `construct_libraries` properties.

### Schema version 6

* Require `samples`.
* Convert `donors` to be calculated from `samples`.

### Minor changes since schema version 5

* Add `publication_identifiers`.
* Expand `preferred_assay_title` enum list to include `MPRA (scQer)`, `CRISPR FlowFISH`, `AAV-MPRA`, `lentiMPRA`, `semi-qY2H`, `variant FlowFISH`, `yN2H`, `mN2H`, `CERES-seq`, and `SUPERSTARR`.
* Add `readout`.
* Expand `preferred_assay_title` enum list to include `Parse Split-seq`.
* Add `auxiliary_sets`.
* Restrict `nucleic_acid_delivery`, `moi`, and `construct_libraries` to submittable by admins only. These properties will be moved to Sample objects.
* Expand `preferred_assay_title` enum list to include `10x multiome with MULTI-seq` and `snMCT-seq`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 5

* Remove `seqspec`.

### Minor changes since schema version 4

* Expand `preferred_assay_title` enum list to include `10x multiome` and `MULTI-seq`.
* Add `nucleic_acid_delivery`.
* Add `files`.
* Add `control_file_sets`.
* Add `control_for`.
* Add `sequencing_library_type`.
* Expand `sequence_library_type` enum list to include `polyA depleted` and `polyA enriched`.

### Schema version 4

* Restrict `protocols` from linking to "https://www.protocols.io/".

### Minor changes since schema version 3

* Add `seqspec`.
* Add `related_multiome_datasets`.
* Add `multiome_size`.
* Add `dbxrefs`.
* Add `construct_libraries`.

### Schema version 3

* Change `accessionType` to `DS`

### Schema version 2

* Rename `sample` to `samples`.
* Rename `donor` to `donors`.
