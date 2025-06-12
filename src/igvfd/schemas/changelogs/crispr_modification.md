## Changelog for *`crispr_modification.json`*

### Minor changes since schema version 4

* Extend `fused_domain` enum list to include `Tet1`.
* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `fused_domain` enum list to include `2xVP64-2A-Puro`.
* Extend `fused_domain` enum list to include `2xVP64-2A-Thy1.1`.

### Schema version 4

* Extend `status` enum list to include `preview`.
* Rename `tagged_protein` to `tagged_proteins`.

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
