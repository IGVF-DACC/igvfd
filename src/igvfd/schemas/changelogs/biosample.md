## Changelog for *`biosample.json`*

### Minor changes since schema version 3

* Add `description`.

### Schema version 3

* Restrict `treatments`, `donors`, `dbxrefs`, `aliases`, `collections`, and `alternate_accessions` to be a non-empty array with at least one item.

### Schema version 2

* Add `donors` and `taxa` to requirements.

### Minor changes since schema version 1

* Rename `organism` to `taxa`.
* Remove `related_biosamples` and `related_biosamples_relationship`.
* Add `pooled_from` and `part_of`.
