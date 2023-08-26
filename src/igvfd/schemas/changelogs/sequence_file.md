## Changelog for *`sequence_file.json`*

### Schema version 4

* Restrict `minimum_read_length` to a maximum value of 300000000.
* Restrict `maximum_read_length` to a maximum value of 300000000.
* Restrict `mean_read_length` to a maximum value of 300000000.
* Change `mean_read_length` type to number.

### Minor changes since schema version 3

* Add `seqspec`.

### Schema version 3

* Require `sequencing_platform`.
* Add `flowcell_id` and `lane`.
