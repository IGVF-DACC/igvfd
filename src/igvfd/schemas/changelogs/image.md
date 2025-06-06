## Changelog for *`image.json`*

### Minor changes since schema version 4

* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Remove calculated property `thumb_nail`.
* Extend `status` enum list to include `preview`.
* Change default value of `status` to `in progress`.
* Update calculation of `summary`.

### Schema version 4

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 3

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 3

* Disallow empty strings in `description`.

### Minor changes since schema version 2

* Add `description`.
* Add `aliases` to `identifyingProperties`.

### Schema version 2

* Restrict `aliases` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add `aliases`.
