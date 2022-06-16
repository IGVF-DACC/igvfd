## Changelog for user.json

### Schema Version 1
* Schema code forked from ENCODEd version 9 user schema.
* *job_title* property now has an enum list:
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
* user is unchanged, but will have gained properties for aliases and submitted due to change of basic_item mixin.
