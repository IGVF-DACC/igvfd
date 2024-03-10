## Changelog for *`configuration_file.json`*

### Schema version 6

* Require `release_timestamp` for any objects with `released`, `archived`, or `revoked` status.

### Schema version 5

* Change `seqspec_of` from a calculated property to a submittable property.

### Minor changes since schema version 4

* Add `release_timestamp`.
* Add `MPRAbase` to `collections`.

### Schema version 4

* Require publicly released files to have `upload_status` of `validated` or `invalidated`.

### Schema version 3

* Disallow empty strings in `description`.

### Schema version 2

* Require a minimum of 1 item for `dbxrefs`.

### Minor changes since schema version 1

* Add `seqspec_of`.
* Expand `collections` enum list to include `ClinGen`, `GREGoR`, `IGVF_catalog_beta_v0.1`, and `MaveDB`.
