## Changelog for *`workflow.json`*

### Minor changes since schema version 6

* Add `preferred_assay_titles`.
* Update `source_url` regex to include `https://support.parsebiosciences.com/`.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.

### Schema version 6

* Change `workflow_version` from an integer to a string.

### Minor changes since schema version 5

* Add `analysis_step_versions`.
* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Extend `status` enum list to include `preview`.
* Add `uniform_pipeline`.
* Extend `collections` enum list to include `VarChAMP`.

### Schema version 5

* Remove `publication_identifiers`.

### Minor changes since schema version 4

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Add `workflow_version`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 4

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 3

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Rename `references` to `publication_identifiers`.
