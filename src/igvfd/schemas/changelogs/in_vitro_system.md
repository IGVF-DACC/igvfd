## Changelog for *`in_vitro_system.json`*


### Minor changes since schema version 10

* remove `permissions` from `classification`.

### Schema version 10

* Require `targeted_sample_term`, `introduced_factors`, `time_post_factors_introduction` and `time_post_factors_introduction_units` if `classification` is `organoid`, `differentiated cell specimen`, or `reprogrammed cell specimen`.
* Mutually require `introduced_factors` with `time_post_factors_introduction` and `time_post_factors_introduction_units`.

### Schema version 9

* Remove `taxa` from `required` and make it calculated.

### Minor changes since schema version 8

* Add `cellular_sub_pool`.

### Schema version 8

* Rename `differentiated cell` to `differentiated cell specimen`.
* Rename `reprogrammed cell` to `reprogrammed cell specimen`.
* Add `pooled cell specimen`.

### Schema version 7

* Remove taxa `Saccharomyces`.

### Schema version 6

* Add `sorted_fraction_detail`.

### Minor changes since schema version 5

* Add `sorted_fraction`.
* Add `targeted_sample_term`.
* Add `modification`.

### Schema version 5

* Remove `differentiated_tissue` from `classification`.

### Minor changes since schema version 3

* Add `file_sets`.

### Schema version 3

* Rename `biomarker` to `biomarkers`.

### Schema version 2

* Rename `donor` to `donors`.
