## Changelog for *`user.json`*

### Schema version 6

* Update `email` regex to disallow capital letters.

### Schema version 5

* Add regex for `email`.

### Schema version 4

* Require `viewing_groups` to contain at least one value.

### Minor changes since schema version 3

* Update `aliases` regex to add `buenrostro-bernstein` as a namespace.
* Add `release_timestamp`.

### Schema version 3

* Disallow empty strings in `description`.

### Minor changes since schema version 2

* Add `description`.
* Add `aliases` to `identifyingProperties`.

### Schema version 2

* Restrict `aliases`, `submits_for`, and `groups` to be a non-empty array with at least one item.

### Minor changes since schema version 1

* Add `submitter_comment`, `submitted_by`, `creation_timestamp` and `aliases`.
* Expand `job_title` enum list to include:
    ```json
    "enum": [
        "Primary Investigator",
        "Project Manager",
        "Submitter",
        "Post Doc",
        "Data Wrangler",
        "Scientist",
        "Computational Scientist",
        "Software Developer",
        "NHGRI staff member",
        "Other"
    ]
    ```
