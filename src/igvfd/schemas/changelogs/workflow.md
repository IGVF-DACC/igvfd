## Changelog for *`workflow.json`*

### Schema version 4

* Objects with released, archived or revoked status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

### Minor changes since schema version 3

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Rename `references` to `publication_identifiers`.
