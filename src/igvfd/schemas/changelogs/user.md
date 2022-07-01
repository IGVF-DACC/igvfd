## Changelog for *`user.json`*

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
