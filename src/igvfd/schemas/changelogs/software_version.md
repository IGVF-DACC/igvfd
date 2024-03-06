## Changelog for *`software_version.json`*

### Schema version 5

* Objects with released or archived status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

### Minor changes since schema version 4

* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 4

* Disallow empty strings in `description`.

### Schema version 3

* Restrict `version` pattern to `v#.#.#`.

### Schema version 2

* Rename `references` to `publication_identifiers`.
