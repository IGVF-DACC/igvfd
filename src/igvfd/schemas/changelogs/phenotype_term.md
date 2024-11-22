## Changelog for *`phenotype_term.json`*

### Minor changes since schema version 4

* Extend `status` enum list to include `preview`.
* Update calculation of `summary`.

### Schema version 4

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 3

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 3

* Disallow empty strings in `description`.

### Minor changes since schema version 2

* Add calculated property `ontology`.
* Add `description`.
* Add `is_a`.

### Schema version 2

* Restrict `aliases` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add calculated property `ancestors`.
* Rename schema `phenotype_ontology_term.json` to `phenotype_term.json`.
* Add `submitter_comment`, `submitted_by` and `creation_timestamp`.
