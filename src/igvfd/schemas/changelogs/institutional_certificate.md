## Changelog for *`institutional_certificate.json`*

### Minor changes since schema version 2

* Add `partner_awards`.
* Add `partner_labs`.
* Add calculated property `data_use_limitation_summary`.
* Extend `status` enum list to include `preview`.

### Schema version 2

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 1

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.
