## Changelog for *`modification.json`*

### Minor changes since schema version 6

* Add calculated property `samples_modified`.

### Schema version 6

* Adjust `fused_domain` enum list to remove `KRAB`.
* Adjust `fused_domain` enum list to replace `VPR` with `VP64-p65-Rta (VPR)`.
* Adjust `fused_domain` enum list to replace `ZIM3` with `ZIM3-KRAB`.

### Minor changes since schema version 5

* Restrict submission of `Modifications` to admin only.
* Add `activating_agent_term_id`.
* Add `activating_agent_term_name`.
* Add `activated`.

### Schema version 5

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 4

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `archived` to `status`.

### Schema version 4

* Disallow empty strings in `description`.

### Minor changes since schema version 3

* Add `M-MLV RT (PE2)`, `TdCBE`, `TdCGBE`, and `TdDE` to `fused_domain`.
* Add `nCas9` to `cas`.

### Schema version 3

* Rename `source` to `sources`.
* Remove `accession` and `alternate_accessions` from identifying properties.

### Minor changes since schema version 2

* Add `ZIM3` to `fused_domain`.
* Add `SpG` to `cas`.
* Add `BE4max`, `eA3A`, and `eA3A-T44D-S45A` to `fused_domain`.

### Schema version 2

* Add required property `cas_species`.
* Add `2xVP64` and `3xVP64` to `fused_domain`.

### Minor changes since schema version 1

* Add `VPH` to `fused_domain`.
