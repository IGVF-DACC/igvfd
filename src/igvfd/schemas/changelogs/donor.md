## Changelog for *`donor.json`*

### Schema version 2

* Restrict `parents` and `external_resources` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add `traits`.
* Rename `organism` to `taxa`.
* Require `sex`, set default to:
    ```json
    "unspecified"
    ```
