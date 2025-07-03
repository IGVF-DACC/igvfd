## Changelog for *`image_file.json`*

### Schema version 5

* Add calculative property `preferred_assay_titles`
* Adjust `derived_manually` to have default value `False`.

### Minor changes since schema version 4

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
* Add `workflow`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Add `checkfiles_version`.
* Extend `upload_status` enum list to include `validation exempted`.
* Add `derived_manually`.
* Extend `collections` enum list to include `VarChAMP`.
* Add calculated property `assay_titles`.
* Allow submission of `fiducial alignment` to non-admin users.
* Update calculation of `summary`.
* Add `analysis_step_version`.
* Add calculated property `input_file_for`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 4

* Require `derived_from` to contain at least one value.
* Require `file_format_specifications` to contain at least one value.

### Schema version 3

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 2

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.

### Schema version 2

* Restrict submission of `fiducial alignment` to admin users.

### Minor changes since schema version 1

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.
