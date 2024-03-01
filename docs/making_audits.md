Adding audits
=========================

This document describes how to add and update audits that check metadata consistency and integrity.

Guide to where to edit Source Code
----------------

* **src** directory - contains all the python and javascript code for front and backends
    * **audit** - python instructions for checking metadata stored in the schema
    * **schemas** - JSON schemas ([JSONSchema], [JSON-LD]) describing allowed types and values for all metadata objects
    * **tests** - Unit and integration tests
    * **types** -  business logic for dispatching URLs and producing the correct JSON
    * **upgrade** - python instructions for upgrading old objects stored to the latest
    * **loadxl.py** - python script that defines the schema objects to load

-----

Adding a new aduit
----------------

1. To add a new audit, navigate to the *audit** directory. Determine what metadata is needed to implement the consistency and integrity check. This helps to determine which object has the appropriate metadata available and where to place the new audit. In the directory make a new python file or edit an exisiting python file named after the determined object.

2. Make a new audit definition, using the metadata needed as a guide to fall into one these 2 categories:

    * *Contained in an object* - all metadata need for audit are properties of the object where embedded
objects referred to by an identifier:

        @audit_checker('{metadata_object}', frame='object')
        def audit_new_audit_name(value, system):
            pass

    * *Requires metadata in other objects* - metadata need for audit are properties of the object as well as properties within embedded objects:

        @audit_checker('{metadata_object}', frame=['{linked_object_1}'])
        def audit_new_audit_name(value, system):
            pass

3. Define the description for the audit. The description should serve to describe what type of metadata is audited in a human-readable format without any technical language like field names. It should be kept in the positive as much as possible and limited to a sentence.

Additionally, decide on an appropriate ```AuditFailure``` category name for the audit. This category will be displayed on the faceted search. The category should be concise, precise, and avoid unnecessary language (e.g., "metadata" or "associated" since they are implied). Generally, audits will likely fall into one of the following three types of categories.

    * a missing property or link -> "missing property/item"
    * an inconsistency with an expectation of metadata on linked item(s) -> inconsistent "item" "property"
    * a property or link to a type that isn't expected -> unexpected "property"/"type"

Also determine which of the following 4 levels of severity the audit should fall into.

    * *ERROR* - Incorrect or inconsistent metadata. This is wrong no matter what.
    * *NOT COMPLIANT* - Not fulfilling a compliance standard like attached documents or definitely missing metadata. This should not be released this way.
    * *WARNING* - Possibly missing or inconsistent metadata. Data will be released with warnings.
    * *INTERNAL ACTION* - Metadata errors the DACC needs to update.

If there are multiple levels for a single category the description should reflect this with the levels in parantheses (ex. "The list of related donors are expected to be unique (WARNING) and should include a mutual link to the corresponding donor (ERROR).")

The description, category, and levels should be listed in the docstring of the audit function shown as following. The docstring for each audit is used to build a row in the audit documentation page for the respective type.
    '''
        audit_detail: Description of the audit.
        audit_category: Category of the audit.
        audit_levels: Level(s) of the audit. (comma-separated)
    '''

4. Write the logic for the metadata check and define the details to be displayed with the audit. The details should display the values for the metadata properties that are resulting in the AuditFailure.

    Example of a ```measurement_set``` which has a preferred assay title that does not correspond to its assay term:

        if preferred_assay_title and preferred_assay_title not in assay_object.get('preferred_assay_titles', []):
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} has '
                f'assay term "{assay_term_name}", but preferred assay title "{preferred_assay_title}", '
                f'which is not an expected preferred assay title for this assay term.'
            )
            yield AuditFailure('inconsistent assays', detail, level='WARNING')

    Use ```audit_link``` to format links so that the front end can find and present them. The first parameter is the text to display for the link, while the second is the link path. You must import ```audit_link``` from the .formatter library.

    The .formatter library also includes a ```path_to_text``` utility to help generate link text if all you have is the ```@id```. Pass this ```@id``` to ```path_to_text``` and it returns just the accession portion as text that you can use as link text.

5. In the **tests** directory add audit test to an existing/new python file named ```test_audit_{metadata_object}.py```. This example shows the basic structure of setting up ```pytest.fixture``` and test that ```property_1``` is present if ```property_2``` is RNA:

        @pytest.fixture
        def {metadata_object}_1:
            item = {
                'property_2': 'RNA',
            }
            return testapp.post_json('/{metadata_object}', item, status=201).json['@graph'][0]


        def test_{metadata_object}_property_1(testapp, {metadata_object}_1):
            res = testapp.get({metadata_object}_1['@id'] + '@@index-data')
                errors = res.json['audit']
                errors_list = []
                for error_type in errors:
                    errors_list.extend(errors[error_type])
                assert any(error['category'] == 'missing prperty 1' for error in errors_list)
