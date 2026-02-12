## Changelog for *`rodent_donor.json`*

### Minor changes since schema version 14

* Add `is_on_anvil`.
* Extend `collections` enum list to include `E2G Pillar Project`.
* Extend `collections` enum list to include `Bridge Sample`.
* Add calculated property `superseded_by`.
* Add `supersedes`.
* Extend `strain_background` enum list to include `CC001/Unc`.
* Extend `strain_background` enum list to include `CC002/Unc`.
* Extend `strain_background` enum list to include `CC003/Unc`.
* Extend `strain_background` enum list to include `CC004/TauUnc`.
* Extend `strain_background` enum list to include `CC005/TauUnc`.
* Extend `strain_background` enum list to include `CC006/TauUnc`.
* Extend `strain_background` enum list to include `CC007/Unc`.
* Extend `strain_background` enum list to include `CC008/GeniUnc`.
* Extend `strain_background` enum list to include `CC009/Unc`.
* Extend `strain_background` enum list to include `CC010/GeniUnc`.
* Extend `strain_background` enum list to include `CC011/Unc`.
* Extend `strain_background` enum list to include `CC012/GeniUnc`.
* Extend `strain_background` enum list to include `CC013/GeniUnc`.
* Extend `strain_background` enum list to include `CC015/Unc`.
* Extend `strain_background` enum list to include `CC017/Unc`.
* Extend `strain_background` enum list to include `CC018/Unc`.
* Extend `strain_background` enum list to include `CC024/GeniUnc`.
* Extend `strain_background` enum list to include `CC025/GeniUnc`.
* Extend `strain_background` enum list to include `CC028/GeniUnc`.
* Extend `strain_background` enum list to include `CC029/Unc`.
* Extend `strain_background` enum list to include `CC030/GeniUnc`.
* Extend `strain_background` enum list to include `CC032/GeniUnc`.
* Extend `strain_background` enum list to include `CC036/Unc`.
* Extend `strain_background` enum list to include `CC037/TauUnc`.
* Extend `strain_background` enum list to include `CC038/GeniUnc`.
* Extend `strain_background` enum list to include `CC041/TauUnc`.
* Extend `strain_background` enum list to include `CC043/GeniUnc`.
* Extend `strain_background` enum list to include `CC055/TauUnc`.
* Extend `strain_background` enum list to include `CC057/Unc`.
* Extend `strain_background` enum list to include `CC060/Unc`.
* Extend `strain_background` enum list to include `CC062/Unc`.
* Extend `strain_background` enum list to include `CC065/Unc`.
* Extend `strain_background` enum list to include `CC071/TauUnc`.
* Extend `strain_background` enum list to include `CC074/Unc`.
* Extend `collections` enum list to include `IGVF_catalog_v1.0`.
* Extend `collections` enum list to include `Benchmark`.
* Extend `collections` enum list to include `TF Perturb-seq Project`.
* Add `preview_timestamp`.
* Update `aliases` regex to add `igvf-dacc-processing-pipeline` as a namespace.
* Update `aliases` regex to add `steven-gazal` as a namespace.
* Update `aliases` regex to add `katie-pollard` as a namespace.
* Update `aliases` regex to add `kushal-dey` as a namespace.
* Update `aliases` regex to add `stephen-yi` as a namespace.
* Extend `collections` enum list to include `ACMG73`.
* Extend `collections` enum list to include `Morphic`.
* Extend `collections` enum list to include `StanfordFCC`.
* Extend `collections` enum list to include `IGVF phase 1`.
* Extend `collections` enum list to include `TOPMED Freeze 8`.
* Extend `collections` enum list to include `Williams Syndrome Research`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.5`.
* Extend `status` enum list to include `preview`.
* Extend `strain_background` enum list to include `B6129S1F1/J`.
* Extend `strain_background` enum list to include `B6AF1/J`.
* Extend `strain_background` enum list to include `B6CASTF1/J`.
* Extend `strain_background` enum list to include `B6NODF1/J`.
* Extend `strain_background` enum list to include `B6NZOF1/J`.
* Extend `strain_background` enum list to include `B6PWKF1/J`.
* Extend `strain_background` enum list to include `B6WSBF1/J`.
* Extend `collections` enum list to include `VarChAMP`.

### Schema version 14

* Remove `publication_identifiers`.

### Schema version 13

* Require `sources` if `product_id` is specified.

### Minor changes since schema version 12

* Restrict `publication_identifiers` to submission by admins only.
* Add `publications`.
* Update calculation of `summary`.
* Extend `collections` enum list to include `Vista`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.2`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.3`.
* Extend `collections` enum list to include `IGVF_catalog_beta_v0.4`.

### Schema version 12

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Minor changes since schema version 11

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 11

* Disallow empty strings in `description`.

### Minor changes since schema version 10
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.

### Schema version 10

* Rename `source` to `sources`.

### Schema version 9

* Rename `references` to `publication_identifiers`.

### Schema version 8

* Add `virtual`.

### Schema version 7

* Remove `parents`.

### Minor changes since schema version 6

* Add `dbxrefs`.

### Schema version 6

* Remove `traits`.

### Schema version 5

* Add `rodent_identifier`.
* Add `individual_rodent`.

### Schema version 4

* Remove `external_resource`.

### Minor changes since schema version 2

* Add `description`.
* Add `revoke_detail`.
* Add `phenotypic_features`.

### Schema version 2

* Restrict `parents`, `external_resources`, `aliases`, `collections`, `alternate_accessions`, `documents`, and `references` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add `traits`.
* Rename `organism` to `taxa`.
* Require `sex`, set default to:
    ```json
    "unspecified"
    ```
* Rename `taxon_id` to `organism`.
* Restrict `taxon_id` to NCBI taxonomy ids that start with NCBI:txid followed by numbers.
