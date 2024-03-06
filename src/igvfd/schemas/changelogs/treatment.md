## Changelog for *`treatment.json`*

### Schema version 7

* Objects with released or archived status without `release_timestamp` are now automatically updated to have `release_timestamp` `2024-03-06T12:34:56Z`.

### Minor changes since schema version 6

* Add `release_timestamp`.
* Add `environmental` to `treatment_type`.
* Add `archived` to `status`.

### Schema version 6

* Disallow empty strings in `description`.

### Minor changes since schema version 5

* Rename `title` to `summary`.

### Schema version 5

* Rename `source` to `sources`.

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
