## Changelog for *`phenotypic_feature.json`*

### Minor changes since schema version 3

* Extend `quantity_units` enum list to include `UPDRS` and `MMSE`.
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
