## Changelog for *`differentiated_tissue.json`*

### Schema version 4

* Remove `stage` from `post_differentiation_time_units` enumerated value.
* Change `post_differentiation_time` type from `integer` to `number`.

### Schema version 4

* Restrict `treatments`, `donors`, `differentiation_treatments`, and `dbxrefs` to be a non-empty array with at least one item.

### Schema version 3

* Restrict `part_of` property to link only to `differentiated_tissue`.

### Schema version 2

* Add `donors` and `taxa` to requirements.

### Minor changes since schema version 1

* Rename `organism` to `taxa`.
* Convert `sex` to be calculated and not submittable.
* Add `differentiated_from` and `differentiation_treatments`.
* Rename schema `organoid.json` to `differentiated_tissue.json`.
