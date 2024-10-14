## Changelog for *`award.json`*

### Minor changes since schema version 4

* Extend `project` enum list to include `IGVF affiliate`.
* Update calculation of `summary`.
* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.

### Schema version 4

* Disallow empty strings in `description`.

### Schema version 3

* Rename `pi` to `pis`.

### Minor changes since schema version 2

* Add `aliases` to `identifyingProperties`.
* Add `contact_pi`.

### Schema version 2

* Restrict `aliases` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Restrict `start_date` and `end_date` format to *date*.
* Add `submitter_comment`, `submitted_by` and `creation_timestamp`.
