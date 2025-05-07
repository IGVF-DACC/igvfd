## Changelog for *`publication.json`*

### Minor changes since schema version 6

* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `status` enum list to include `preview`.
* Add calculated property `samples`.
* Add calculated property `file_sets`.
* Add calculated property `donors`.
* Add calculated property `workflows`.
* Add calculated property `software`.
* Add calculated property `software_versions`.

### Schema version 6

* Require `published_by` to have a minimum of one value.

### Schema version 5

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 4

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 4

* Disallow empty strings in `description`.

### Schema version 3

* Replace `identifiers` with `publication_identifiers` from mixins.

### Minor changes since schema version 2

* Add `description`.
* Add `aliases` to `identifyingProperties`.

### Schema version 2

* Restrict `aliases` to be a non-empty array with at least one item.
