## Changelog for *`treatment.json`*

### Schema version 4
* Add required `lab`, `depletion` and `award`.
* Add `depletion`.
* Remove requirement for `amount` and `amount_units`.

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
