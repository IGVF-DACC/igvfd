## Changelog for *`platform_term.json`*

### Schema version 3

* Objects with released or archived status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

### Minor changes since schema version 2

* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 2

* Disallow empty strings in `description`.

### Minor changes since schema version 1

* Add calculated property `ontology`.
* Add `company`.
