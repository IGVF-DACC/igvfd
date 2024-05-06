## Changelog for *`platform_term.json`*

### Schema version 4

* Adjust `sequencing_kit` enum list to replace `NovaSeq 6000 S4 Reagent Kit V1.5` with `NovaSeq 6000 S4 Reagent Kit v1.5`.

### Minor changes since schema version 3

* Add `sequencing_kits`.

### Schema version 3

* Require `release_timestamp` for any objects with `released` or `archived` status

### Minor changes since schema version 2

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 2

* Disallow empty strings in `description`.

### Minor changes since schema version 1

* Add calculated property `ontology`.
* Add `company`.
