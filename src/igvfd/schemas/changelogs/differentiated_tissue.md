## Changelog for *`differentiated_tissue.json`*

### Schema version 3

* Restrict `part_of` property to link only to `differentiated_tissue`.

### Schema version 2

* Add `donors` and `taxa` to requirements.

### Minor changes since schema version 1

* Rename `organism` to `taxa`.
* Convert `sex` to be calculated and not submittable.
* Add `differentiated_from` and `differentiation_treatments`.
* Rename schema `organoid.json` to `differentiated_tissue.json`.
