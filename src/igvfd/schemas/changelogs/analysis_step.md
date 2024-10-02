## Changelog for *`analysis_step.json`*

### Minor changes since schema version 5

* Extend `input_content_types` enum list to include `model parameters`.
* Extend `output_content_types` enum list to include `model parameters`.
* Extend `analysis_step_types` enum list to include `counts normalization`.
* Extend `input_content_types` enum list to include `peak quantifications`.
* Extend `output_content_types` enum list to include `peak quantifications`.
* Extend `input_content_types` enum list to include `variant localization impacts`.
* Extend `output_content_types` enum list to include `variant localization impacts`.
* Extend `input_content_types` enum list to include `external source data`.
* Extend `input_content_types` enum list to include `fragments`.
* Extend `input_content_types` enum list to include `gene quantifications`.
* Extend `output_content_types` enum list to include `external source data`.
* Extend `output_content_types` enum list to include `fragments`.
* Extend `output_content_types` enum list to include `gene quantifications`.
* Extend `input_content_types` enum list to include `genes`.
* Extend `input_content_types` enum list to include `loci`.
* Extend `output_content_types` enum list to include `genes`.
* Extend `output_content_types` enum list to include `loci`.
* Extend `input_content_types` enum list to include `transcript quantifications`.
* Extend `input_content_types` enum list to include `barcode to hashtag mapping`.
* Extend `input_content_types` enum list to include `barcode to variant mapping`.
* Extend `output_content_types` enum list to include `transcript quantifications`.
* Extend `output_content_types` enum list to include `barcode to hashtag mapping`.
* Extend `output_content_types` enum list to include `barcode to variant mapping`.
* Extend `analysis_step_types` enum list to include `barcode mapping generation`.
* Extend `analysis_step_types` enum list to include `filtering`.
* Extend `analysis_step_types` enum list to include `interaction calling`.
* Extend `analysis_step_types` enum list to include `merging`.
* Extend `analysis_step_types` enum list to include `peak calling`.
* Extend `analysis_step_types` enum list to include `quantification`.
* Extend `analysis_step_types` enum list to include `signal normalization`.
* Extend `analysis_step_types` enum list to include `spatial feature detection`.
* Extend `analysis_step_types` enum list to include `variant annotation`.
* Extend `input_content_types` enum list to include `peaks`.
* Extend `input_content_types` enum list to include `detected tissue`.
* Extend `input_content_types` enum list to include `low resolution tissue`.
* Extend `input_content_types` enum list to include `high resolution tissue`.
* Extend `input_content_types` enum list to include `fiducial alignment`.
* Extend `input_content_types` enum list to include `edge weights`.
* Extend `input_content_types` enum list to include `graph structure`.
* Extend `input_content_types` enum list to include `position weight matrix`.
* Extend `input_content_types` enum list to include `barcode to element mapping`.
* Extend `input_content_types` enum list to include `barcode to sample mapping`.
* Extend `input_content_types` enum list to include `differential gene expression quantifications`.
* Extend `input_content_types` enum list to include `differential transcript expression quantifications`.
* Extend `input_content_types` enum list to include `editing templates`.
* Extend `input_content_types` enum list to include `element quantifications`.
* Extend `input_content_types` enum list to include `elements reference`.
* Extend `input_content_types` enum list to include `fold change over control`.
* Extend `input_content_types` enum list to include `guide quantifications`.
* Extend `input_content_types` enum list to include `guide RNA sequences`.
* Extend `input_content_types` enum list to include `MPRA sequence designs`.
* Extend `input_content_types` enum list to include `prime editing guide RNA sequences`.
* Extend `input_content_types` enum list to include `protein to protein interaction score`.
* Extend `input_content_types` enum list to include `tissue positions`.
* Extend `input_content_types` enum list to include `sample sort parameters`.
* Extend `input_content_types` enum list to include `sequence barcodes`.
* Extend `input_content_types` enum list to include `SNP effect matrix`.
* Extend `input_content_types` enum list to include `variants`.
* Extend `input_content_types` enum list to include `variant effects`.
* Extend `input_content_types` enum list to include `variant to element mapping`.
* Extend `output_content_types` enum list to include `peaks`.
* Extend `output_content_types` enum list to include `detected tissue`.
* Extend `output_content_types` enum list to include `low resolution tissue`.
* Extend `output_content_types` enum list to include `high resolution tissue`.
* Extend `output_content_types` enum list to include `fiducial alignment`.
* Extend `output_content_types` enum list to include `edge weights`.
* Extend `output_content_types` enum list to include `graph structure`.
* Extend `output_content_types` enum list to include `position weight matrix`.
* Extend `output_content_types` enum list to include `barcode to element mapping`.
* Extend `output_content_types` enum list to include `barcode to sample mapping`.
* Extend `output_content_types` enum list to include `differential gene expression quantifications`.
* Extend `output_content_types` enum list to include `differential transcript expression quantifications`.
* Extend `output_content_types` enum list to include `editing templates`.
* Extend `output_content_types` enum list to include `element quantifications`.
* Extend `output_content_types` enum list to include `elements reference`.
* Extend `output_content_types` enum list to include `fold change over control`.
* Extend `output_content_types` enum list to include `guide quantifications`.
* Extend `output_content_types` enum list to include `guide RNA sequences`.
* Extend `output_content_types` enum list to include `MPRA sequence designs`.
* Extend `output_content_types` enum list to include `prime editing guide RNA sequences`.
* Extend `output_content_types` enum list to include `protein to protein interaction score`.
* Extend `output_content_types` enum list to include `tissue positions`.
* Extend `output_content_types` enum list to include `sample sort parameters`.
* Extend `output_content_types` enum list to include `sequence barcodes`.
* Extend `output_content_types` enum list to include `SNP effect matrix`.
* Extend `output_content_types` enum list to include `variants`.
* Extend `output_content_types` enum list to include `variant effects`.
* Extend `output_content_types` enum list to include `variant to element mapping`.

### Schema version 5

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 4

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 4

* Disallow empty strings in `description`.

### Schema version 3

* Require `lab` and `award`.

### Schema version 2

* Require a minimum of 1 item for `analysis_step_types`, `parents`, `input_content_types`, and `output_content_types`.

### Minor changes since schema version 1

* Add `seqspec`, `contact matrix`, `sparse gene count matrix`, `sparse peak count matrix`, `sparse transcript count matrix`, and `transcriptome annotations` to `input_content_types` and `output_content_types`.
