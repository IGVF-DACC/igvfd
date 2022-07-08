## Changelog for *`donor.json`*

### Schema version 2

* `parents` and `external_resources` must include at least one item.

### Minor changes since schema version 1

* Add `traits`.
* Rename `organism` to `taxa`.
* Require `sex`, set default to:
    ```json
    "unspecified"
    ```
