## Changelog for *`image_file.json`*

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
