## Changelog for *`treatment.json`*

### Minor changes since schema version 7

* Add calculated property `biosamples_treated`.

### Schema version 7

* Require `release_timestamp` for any objects with `released` or `archived` status.

### Minor changes since schema version 6

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
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
