## Changelog for *`sequence_file.json`*

### Minor changes since schema version 14

* Extend `base_modifications` enum list to include `inosine`.
* Extend `base_modifications` enum list to include `pseudouridine`.
* Add `external_host_url`.
* Add `externally_hosted`.
* Add `derived_manually`.
* Extend `collections` enum list to include `VarChAMP`.
* Add calculated property `assay_titles`.
* Extend `sequencing_kit` enum list to include `Singular G4 F2 Reagent Kit`.
* Add `base_modifications`.
* Extend `sequencing_kit` enum list to include `NovaSeq X Series 1.5B Reagent Kit`.
* Extend `sequencing_kit` enum list to include `NovaSeq X Series 25B Reagent Kit`.
* Update calculation of `summary`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.

### Schema version 14

* Reduce `upload_status` enum list to exclude `deposited`.
* Remove `anvil_source_url`.
* Add `anvil_url`.
* Require `controlled_access`.

### Schema version 13

* Adjust `sequencing_kit` enum list to replace `NovaSeq 6000 S4 Reagent Kit V1.5` with `NovaSeq 6000 S4 Reagent Kit v1.5`.

### Minor changes since schema version 12

* Extend `sequencing_kit` enum list to include `ONT Ligation Sequencing Kit V14`.
* Extend `sequencing_kit` enum list to include `NovaSeq X Series 10B Reagent Kit`.
* Extend `sequencing_kit` enum list to include `MiSeq Reagent Kit v2`.
* Extend `sequencing_kit` enum list to include `NextSeq 1000/2000 P1 Reagent Kit`.
* Extend `sequencing_kit` enum list to include `NextSeq 1000/2000 P2 Reagent Kit`.
* Extend `sequencing_kit` enum list to include `NextSeq 1000/2000 P3 Reagent Kit`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 12

* Extend `upload_status` enum list to include `deposited`.
* Add `controlled_access`.
* Add `anvil_source_url`.
* Add calculated property `anvil_destination_url`.

### Minor changes since schema version 11

* Add `sequencing_kit`.

### Schema version 11

* Require `derived_from` to contain at least one value.
* Require `file_format_specifications` to contain at least one value.

### Schema version 10

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Schema version 9

* Remove `seqspec`.
* Add calculated property `seqspecs`.

### Minor changes since schema version 8

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.

### Schema version 8

* Replace `subreads` with `PacBio subreads` in `content_type`.
* Expand `content_type` enum list to include `Nanopore reads`.

### Minor changes since schema version 7

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 7

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 6

* Disallow empty strings in `description`.

### Minor changes since schema version 5

* Allow hyphens in `dbxrefs`.

### Schema version 5

* Require a minimum of 1 item for `dbxrefs`.

### Minor changes since schema version 4

* Add `index`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 4

* Restrict `minimum_read_length` to a maximum value of 300000000.
* Restrict `maximum_read_length` to a maximum value of 300000000.
* Restrict `mean_read_length` to a maximum value of 300000000.
* Change `mean_read_length` type to number.

### Minor changes since schema version 3

* Add `seqspec`.

### Schema version 3

* Require `sequencing_platform`.
* Add `flowcell_id` and `lane`.
