## Changelog for *`analysis_step.json`*

### Schema version 6

* Reduce `input_content_types` enum list to exclude `sequence barcodes`.
* Reduce `output_content_types` enum list to exclude `sequence barcodes`.

### Minor changes since schema version 5

* Extend `input_content_types` enum list to include `machine learning model features`.
* Extend `output_content_types` enum list to include `machine learning model features`.
* Extend `input_content_types` enum list to include `feature weights`.
* Extend `output_content_types` enum list to include `feature weights`.
* Extend `input_content_types` enum list to include `element to gene predictions`.
* Extend `output_content_types` enum list to include `element to gene predictions`.
* Extend `input_content_types` enum list to include `primer sequences`.
* Extend `output_content_types` enum list to include `primer sequences`.
* Extend `input_content_types` enum list to include `index`.
* Extend `output_content_types` enum list to include `index`.
* Extend `input_content_types` enum list to include `differential peak quantifications`.
* Extend `output_content_types` enum list to include `differential peak quantifications`.
* Extend `input_content_types` enum list to include `protein language model`.
* Extend `output_content_types` enum list to include `protein language model`.
* Extend `input_content_types` enum list to include `genome index`.
* Extend `output_content_types` enum list to include `genome index`.
* Extend `analysis_step_types` enum list to include `genome index generation`.
* Extend `output_content_types` enum list to include `nascent transcriptome index`.
* Extend `input_content_types` enum list to include `nascent transcriptome index`.
* Extend `output_content_types` enum list to include `transcriptome index`.
* Extend `input_content_types` enum list to include `transcriptome index`.
* Extend `analysis_step_types` enum list to include `transcriptome index generation`.
* Extend `analysis_step_types` enum list to include `computational model training`.
* Extend `analysis_step_types` enum list to include `computational model prediction`.
* Extend `output_content_types` enum list to include `sample barcode count matrix`.
* Extend `input_content_types` enum list to include `sample barcode count matrix`.
* Extend `output_content_types` enum list to include `neural network architecture`.
* Extend `input_content_types` enum list to include `neural network architecture`.
* Extend `analysis_step_types` enum list to include `read trimming`.
* Extend `analysis_step_types` enum list to include `fastq concatenation`.
* Extend `analysis_step_types` enum list to include `fragment generation`.
* Extend `analysis_step_types` enum list to include `UMI deduplication`.
* Extend `analysis_step_types` enum list to include `matrix generation`.
* Extend `output_content_types` enum list to include `DNA footprint scores`.
* Extend `input_content_types` enum list to include `DNA footprint scores`.
* Extend `output_content_types` enum list to include `sequence attributes`.
* Extend `input_content_types` enum list to include `sequence attributes`.
* Extend `output_content_types` enum list to include `TF binding scores`.
* Extend `input_content_types` enum list to include `TF binding scores`.
* Extend `output_content_types` enum list to include `cell hashing barcodes`.
* Extend `input_content_types` enum list to include `cell hashing barcodes`.
* Extend `output_content_types` enum list to include `unfiltered local differential expression`.
* Extend `input_content_types` enum list to include `unfiltered local differential expression`.
* Extend `output_content_types` enum list to include `unfiltered global differential expression`.
* Extend `input_content_types` enum list to include `unfiltered global differential expression`.
* Extend `analysis_step_types` enum list to include `differential expression analysis`.
* Extend `analysis_step_types` enum list to include `demultiplexing`.
* Extend `analysis_step_types` enum list to include `cell to feature barcode mapping`.
* Extend `analysis_step_types` enum list to include `UMI quantification`.
* Extend `analysis_step_types` enum list to include `barcode counting`.
* Extend `status` enum list to include `preview`.
* Extend `output_content_types` enum list to include `barcode onlist`.
* Extend `input_content_types` enum list to include `barcode onlist`.
* Extend `output_content_types` enum list to include `differential chromatin contact quantifications`.
* Extend `input_content_types` enum list to include `differential chromatin contact quantifications`.
* Extend `output_content_types` enum list to include `variant functional predictions`.
* Extend `input_content_types` enum list to include `variant functional predictions`.
* Extend `output_content_types` enum list to include `bin paired count`.
* Extend `input_content_types` enum list to include `bin paired count`.
* Extend `analysis_step_types` enum list to include `base calling`.
* Add calculated property `analysis_step_versions`.
* Extend `output_content_types` enum list to include `reporter elements`.
* Extend `input_content_types` enum list to include `reporter elements`.
* Extend `output_content_types` enum list to include `reporter experiment`.
* Extend `input_content_types` enum list to include `reporter experiment`.
* Extend `output_content_types` enum list to include `reporter variants`.
* Extend `input_content_types` enum list to include `reporter variants`.
* Extend `output_content_types` enum list to include `reporter genomic element effects`.
* Extend `input_content_types` enum list to include `reporter genomic element effects `.
* Extend `output_content_types` enum list to include `reporter genomic variant effects`.
* Extend `input_content_types` enum list to include `reporter genomic variant effects`.
* Extend `input_content_types` enum list to include `differential element quantifications`.
* Extend `output_content_types` enum list to include `differential element quantifications`.
* Extend `input_content_types` enum list to include `model parameters`.
* Extend `output_content_types` enum list to include `model parameters`.
* Extend `analysis_step_types` enum list to include `counts normalization`.
* Extend `input_content_types` enum list to include `barcode to TF overexpression mapping`.
* Extend `output_content_types` enum list to include `barcode to TF overexpression mapping`.
* Extend `input_content_types` enum list to include `coding variant effects`.
* Extend `output_content_types` enum list to include `coding variant effects`.
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
