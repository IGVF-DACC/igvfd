## Changelog for *`measurement_set.json`*

### Minor changes since schema version 5

* Add `publication_identifiers`.
* Expand `preferred_assay_title` enum list to include `MPRA (scQer)`, `CRISPR FlowFISH`, `AAV-MPRA`, `lentiMPRA`, `semi-qY2H`, `yN2H`, `mN2H`.
* Add `readout`.
* Expand `preferred_assay_title` enum list to include `Parse Split-seq`.
* Add `auxiliary_sets`.
* Restrict `nucleic_acid_delivery`, `moi`, and `construct_libraries` to submittable by admins only. These properties will be moved to Sample objects.
* Expand `preferred_assay_title` enum list to include `10x multiome with MULTI-seq` and `snMCT-seq`.

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
