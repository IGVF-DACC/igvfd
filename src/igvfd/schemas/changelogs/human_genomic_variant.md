## Changelog for human_genomic_variant.json

### Schema version 4

* Objects with released or archived status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

### Minor changes since schema version 3

* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Restrict `refseq_id` string pattern to "." at the 10th position.
