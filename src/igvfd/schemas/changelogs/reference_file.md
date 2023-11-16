## Changelog for *`reference_file.json`*

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
