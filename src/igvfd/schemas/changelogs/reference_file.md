## Changelog for *`reference_file.json`*

### Schema version 16

* Adjust `content_type` enum list to remove `regulatory_regions`.
* Adjust `content_type` enum list to remove `regulatory_regions_genes`.
* Adjust `content_type` enum list to remove `regulatory_regions_genes_biosamples`.
* Adjust `content_type` enum list to remove `regulatory_regions_genes_biosamples_donors`.
* Adjust `content_type` enum list to remove `regulatory_regions_genes_biosamples_treatments_chebi`.
* Adjust `content_type` enum list to remove `regulatory_regions_genes_biosamples_treatments_proteins`.
* Adjust `content_type` enum list to remove `regulatory_regions_regulatory_regions`.
* Adjust `content_type` enum list to remove `variants_regulatory_regions`.
* Extend `content_type` enum list to include `genomic_elements` for admins.
* Extend `content_type` enum list to include `genomic_elements_genes` for admins.
* Extend `content_type` enum list to include `genomic_elements_genes_biosamples` for admins.
* Extend `content_type` enum list to include `genomic_elements_genes_biosamples_donors` for admins.
* Extend `content_type` enum list to include `genomic_elements_genes_biosamples_treatments_chebi` for admins.
* Extend `content_type` enum list to include `genomic_elements_genes_biosamples_treatments_proteins` for admins.
* Extend `content_type` enum list to include `genomic_elements_genomic_elements` for admins.
* Extend `content_type` enum list to include `variants_genomic_elements` for admins.

### Minor changes since schema version 15

* Extend `transcriptome_annotation` enum list to include `GENCODE 22`.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `content_type` enum list to include `genome index`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 47`.
* Extend `transcriptome_annotation` enum list to include `GENCODE M36`.
* Extend `content_type` enum list to include `transcriptome index`.
* Extend `content_type` enum list to include `nascent transcriptome index`.
* Add `workflow`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Add `checkfiles_version`.
* Extend `upload_status` enum list to include `validation exempted`.
* Extend `status` enum list to include `preview`.
* Update calculation of `summary`.
* Extend `transcriptome_annotation` enum list to include `GENCODE 32`.

### Schema version 15

* Remove `external_id`.
* Update `dbxrefs` regex to add `ENCODE` as a namespace.

### Minor changes since schema version 14

* Extend `assembly` enum list to include `custom`.
* Add `derived_manually`.
* Extend `collections` enum list to include `VarChAMP`.
* Extend `assembly` enum list to include `Cast - GRCm39`.
* Extend `transcriptome_annotation` enum list to include `GENCODE Cast - M32`.
* Adjust `content_type` enum list to allow usage of `transcriptome reference` for all users.
* Add calculated property `assay_titles`.
* Adjust `content_type` enum list to restrict usage of `biological_context` to admin users.
* Adjust `content_type` enum list to restrict usage of `coding_variants` to admin users.
* Adjust `content_type` enum list to restrict usage of `complexes` to admin users.
* Adjust `content_type` enum list to restrict usage of `complexes_complexes` to admin users.
* Adjust `content_type` enum list to restrict usage of `complexes_proteins` to admin users.
* Adjust `content_type` enum list to restrict usage of `complexes_terms` to admin users.
* Adjust `content_type` enum list to restrict usage of `diseases_genes` to admin users.
* Adjust `content_type` enum list to restrict usage of `documentation (readme)` to admin users.
* Adjust `content_type` enum list to restrict usage of `drugs` to admin users.
* Adjust `content_type` enum list to restrict usage of `elements_genes` to admin users.
* Adjust `content_type` enum list to restrict usage of `genes` to admin users.
* Adjust `content_type` enum list to restrict usage of `genes_genes` to admin users.
* Adjust `content_type` enum list to restrict usage of `genes_pathways` to admin users.
* Adjust `content_type` enum list to restrict usage of `genes_terms` to admin users.
* Adjust `content_type` enum list to restrict usage of `genes_transcripts` to admin users.
* Adjust `content_type` enum list to restrict usage of `go_terms_proteins` to admin users.
* Adjust `content_type` enum list to restrict usage of `motifs` to admin users.
* Adjust `content_type` enum list to restrict usage of `motifs_proteins` to admin users.
* Adjust `content_type` enum list to restrict usage of `ontology_terms` to admin users.
* Adjust `content_type` enum list to restrict usage of `ontology_terms_ontology_terms` to admin users.
* Adjust `content_type` enum list to restrict usage of `pathways` to admin users.
* Adjust `content_type` enum list to restrict usage of `pathways_pathways` to admin users.
* Adjust `content_type` enum list to restrict usage of `proteins` to admin users.
* Adjust `content_type` enum list to restrict usage of `proteins_proteins` to admin users.
* Adjust `content_type` enum list to restrict usage of `regulatory_regions` to admin users.
* Adjust `content_type` enum list to restrict usage of `regulatory_regions_genes` to admin users.
* Adjust `content_type` enum list to restrict usage of `regulatory_regions_genes_biosamples` to admin users.
* Adjust `content_type` enum list to restrict usage of `regulatory_regions_genes_biosamples_donors` to admin users.
* Adjust `content_type` enum list to restrict usage of `regulatory_regions_genes_biosamples_treatments_chebi` to admin users.
* Adjust `content_type` enum list to restrict usage of `regulatory_regions_genes_biosamples_treatments_proteins` to admin users.
* Adjust `content_type` enum list to restrict usage of `regulatory_regions_regulatory_regions` to admin users.
* Adjust `content_type` enum list to restrict usage of `studies` to admin users.
* Adjust `content_type` enum list to restrict usage of `studies_variants` to admin users.
* Adjust `content_type` enum list to restrict usage of `studies_variants_phenotypes` to admin users.
* Adjust `content_type` enum list to restrict usage of `transcriptome reference` to admin users.
* Adjust `content_type` enum list to restrict usage of `transcripts` to admin users.
* Adjust `content_type` enum list to restrict usage of `transcripts_proteins` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_coding_variants` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_diseases` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_diseases_genes` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_drugs` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_drugs_genes` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_genes` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_genes_terms` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_phenotypes` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_phenotypes_studies` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_proteins` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_proteins_terms` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_proteins_biosamples` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_proteins_phenotypes` to admin users.
* Adjust `content_type` enum list to restrict usage of `variants_regulatory_regions` to admin users.
* Extend `content_type` enum list to include `coding_variants`.
* Extend `content_type` enum list to include `documentation (readme)`.
* Extend `content_type` enum list to include `variants_coding_variants`.
* Extend `content_type` enum list to include `variants_diseases`.
* Extend `content_type` enum list to include `variants_diseases_genes`.
* Extend `content_type` enum list to include `variants_phenotypes`.
* Extend `content_type` enum list to include `variants_phenotypes_studies`.
* Update calculation of `summary`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.

### Schema version 14

* Reduce `upload_status` enum list to exclude `deposited`.
* Remove `anvil_source_url`.
* Add `anvil_url`.
* Require `controlled_access`.

### Minor changes since schema version 13

* Extend `content_type` enum list to include `regulatory_regions_regulatory_regions`.
* Extend `file_format_type` enum list to include `mpra_starr`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 13

* Extend `upload_status` enum list to include `deposited`.
* Add `controlled_access`.
* Add `anvil_source_url`.
* Add calculated property `anvil_destination_url`.

### Schema version 12

* Require `derived_from` to contain at least one value.
* Require `file_format_specifications` to contain at least one value.

### Minor changes since schema version 11

* Add calculated property `integrated_in`.

### Schema version 11

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 10

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `elements reference` to `content_type`.
* Add `GENCODE 44`, `GENCODE 45`, `GENCODE M33`, and `GENCODE M34` to `transcriptome_annotation`.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.
* Add `proteins_proteins`, `regulatory_regions_genes`, `regulatory_regions_genes_biosamples`, `regulatory_regions_genes_biosamples_donors`, `regulatory_regions_genes_biosamples_treatments_chebi`, `regulatory_regions_genes_biosamples_treatments_proteins`, and `variants_genes_terms` to `content_type`.
* Adjust `content_type` enum list to restrict usage of `guide RNA sequences`, `sequence barcodes`, `vector sequences` to admin users.

### Schema version 10

* Require `assembly` if `file_format` is one of `bam`, `bed`, `bedpe`, `bigWig`, `bigBed`, `bigInteract`, `tabix`, or `vcf`.

### Schema version 9

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 8

* Disallow empty strings in `description`.

### Schema version 7

* Add a default value for `external`.

### Minor changes since schema version 6
* Add `tsv` to `file_format`.
* Add `variants_proteins_biosamples` and `variants_proteins_phenotypes` to `content_type`.
* Add `sources`.
* Add `external`.
* Add `external_id`.

### Schema version 6

* Enable submission of GENCODE, ENSEMBL, and GRC database references to `dbxrefs`.
* Require a minimum of 1 item for `dbxrefs`.

### Schema version 5

* Add `file_format_type`.

### Minor changes since schema version 4

* Add `vcf` to `file_format`.
* Add `variants` to `content_type`.
* Add `bed`, `csv`, `dat`, `gaf`, `gds`, `obo`, `owl`, `PWM` and `xml` to `file_format`.
* Add `biological_context`, `complexes`, `complexes_complexes`, `complexes_proteins`, `complexes_terms`, `diseases_genes`, `drugs`, `elements_genes`, `genes`, `genes_genes`, `genes_pathways`, `genes_terms`, `genes_transcripts`, `go_terms_proteins`, `motifs`, `motifs_proteins`, `ontology_terms`, `ontology_terms_ontology_terms`, `pathways`, `pathways_pathways`, `proteins`, `regulatory_regions`, `studies`, `studies_variants`, `studies_variants_phenotypes`, `transcriptome reference`, `transcripts`, `transcripts_proteins`, `variants`, `variants_drugs`, `variants_drugs_genes`, `variants_genes`, `variants_proteins`, `variants_proteins_terms`, `variants_regulatory_regions`, `variants_variants` to `content_type`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 4

* Update enums in `transcriptome_annotation` to include `GENCODE` prefix.

### Schema version 3

* Rename `source` to `source_url`.
* Add `format` to `source_url`.
