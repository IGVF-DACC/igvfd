## Changelog for *`phenotypic_feature.json`*

### Schema version 4

* Adjust `quality` enum list to replace `2/2` with `E2/E2`.
* Adjust `quality` enum list to replace `2/3` with `E2/E3`.
* Adjust `quality` enum list to replace `2/4` with `E2/E4`.
* Adjust `quality` enum list to replace `3/3` with `E3/E3`.
* Adjust `quality` enum list to replace `3/4` with `E3/E4`.
* Adjust `quality` enum list to replace `4/4` with `E4/E4`.

### Minor changes since schema version 3

* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `quantity_units` enum list to include `UPDRS`.
* Extend `quantity_units` enum list to include `MMSE`.
* Extend `status` enum list to include `preview`.
* Add `quality`.
* Update calculation of `summary`.

### Schema version 3

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 2

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 2

* Disallow empty strings in `description`.
