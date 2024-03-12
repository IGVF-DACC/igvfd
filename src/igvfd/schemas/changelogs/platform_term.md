## Changelog for *`platform_term.json`*

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
