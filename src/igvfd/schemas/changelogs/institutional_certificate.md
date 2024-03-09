## Changelog for *`institutional_certificate.json`*

### Schema version 3

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Schema version 2

* Objects with released or archived status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

### Minor changes since schema version 1

* Add `release_timestamp`.
* Add `archived` to `status`.
