## Changelog for *`software.json`*

### Minor changes since schema version 6

* Update calculation of `summary`.

### Schema version 6

* Remove `publication_identifiers`.

### Minor changes since schema version 5

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.

### Schema version 5

* Require `used_by` to contain at least one value.

### Schema version 4

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 3

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Rename `references` to `publication_identifiers`.
