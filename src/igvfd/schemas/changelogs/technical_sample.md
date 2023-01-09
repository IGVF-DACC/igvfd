## Changelog for *`technical_sample.json`*

### Schema version 5

* Rename `aliases` to `alias`.
* Rename `alternate_accessions` to `alternate_accession`.
* Rename `collections` to `collection`.
* Rename `documents` to `document`.
* Rename `dbxrefs` to `dbxref`.

### Schema version 4

* Change `technical_sample_term` to link to `Sample Term`.
* Require `technical_sample_term`.

### Minor changes since schema version 3

* Add `description`.
* Add `revoke_detail`.

### Schema version 3

* Remove `additional_description`.

### Schema version 2

* Restrict `dbxrefs`, `aliases`, and `alternate_accessions` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Rename `date` to `date_obtained`.
