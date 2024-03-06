## Changelog for *`analysis_step.json`*

### Schema version 5

* Objects with released or archived status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

### Minor changes since schema version 4

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
