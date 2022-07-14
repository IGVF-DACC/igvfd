## Changelog for *`tissue.json`*

### Schema version 4

* Restrict `treatments`, `donors`, and `dbxrefs` to be a non-empty array with at least one item.

### Schema version 3

* Restrict `part_of` property to link only to `tissue` and `whole organism`.

### Schema version 2

* Add `donors` and `taxa` to requirements.

### Minor changes since schema version 1

* Rename `organism` to `taxa`.
* Convert `sex` to be calculated and not submittable.
