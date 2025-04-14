## Changelog for *`software_version.json`*

### Minor changes since schema version 7

* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `status` enum list to include `preview`.

### Schema version 7

* Rename `downloaded_url` to `source_url`.

### Minor changes since schema version 6

* Update calculation of `summary`.

### Schema version 6

* Remove `publication_identifiers`.

### Minor changes since schema version 5

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.

### Schema version 5

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 4

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 4

* Disallow empty strings in `description`.

### Schema version 3

* Restrict `version` pattern to `v#.#.#`.

### Schema version 2

* Rename `references` to `publication_identifiers`.
