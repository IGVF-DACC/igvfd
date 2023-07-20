## Changelog for *`treatment.json`*

### Schema version 4
* Add `lab` and `award`.
* Add `depletion`. It is `False` by default. If it is `True`, `amount` and `amount_units` should not be specified.
* Remove `amount` and `amount_units` from required properties list.

### Schema version 3
* Require `purpose`.

### Minor changes since schema version 2

* Add `description`.

### Schema version 2

* Restrict `aliases` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add `temperature_units` enum list:
    ```json
    "enum": [
        "Celsius"
    ]
    ```
* Rename `temperature (Celsius)` to `temperature`.
