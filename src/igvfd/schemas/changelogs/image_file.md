## Changelog for *`image_file.json`*

### Schema version 3

* Objects with released, archived or revoked status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

### Schema version 2

* Restrict submission of `fiducial alignment` to admin users.

### Minor changes since schema version 1

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.
