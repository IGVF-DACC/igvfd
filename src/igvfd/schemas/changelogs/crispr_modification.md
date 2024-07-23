## Changelog for *`crispr_modification.json`*

### Schema version 3

* Require `sources` if `product_id` is specified.
* Require `product_id` if `lot_id` is specified.

### Minor changes since schema version 2

* Extend `fused_domain` enum list to include `KOX1-KRAB`.
* Add calculated property `biosamples_modified`.

### Schema version 2

* Adjust `fused_domain` enum list to remove `KRAB`.
* Adjust `fused_domain` enum list to replace `VPR` with `VP64-p65-Rta (VPR)`.
* Adjust `fused_domain` enum list to replace `ZIM3` with `ZIM3-KRAB`.
