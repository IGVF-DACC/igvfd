## Changelog for *`analysis_step.json`*

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
