## Changelog for *`measurement_set.json`*


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
