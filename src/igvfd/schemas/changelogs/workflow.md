## Changelog for *`workflow.json`*

### Schema version 5

* Remove `publication_identifiers`.

### Minor changes since schema version 4

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Add `workflow_version`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 4

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 3

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Rename `references` to `publication_identifiers`.
