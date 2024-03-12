## Changelog for human_genomic_variant.json

### Schema version 4

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 3

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Restrict `refseq_id` string pattern to "." at the 10th position.
