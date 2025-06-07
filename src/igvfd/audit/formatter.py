import re
import json


def audit_link(linkText, uri):
    """Generate link markdown from URI."""
    return '[{}]({})'.format(linkText, uri)


def path_to_text(path):
    """Convert object path to the text portion."""
    accession = re.match(r'\/.*\/(.*)\/', path)
    return accession.group(1) if accession else None


def space_in_words(objects_string):
    """Insert a space between objects that have more than one
    capital letter eg. AntibodyChar --> Antibody Char"""
    add_space = re.sub(r'(\w)([A-Z])', r'\1 \2', objects_string)
    return add_space


def get_audit_message(audit_function, index=0):
    """Retrieves a full audit message, description/category/level, from the docstring of an audit function as a dict.
    By default retrieves the first full message.
    """
    docstring = audit_function.__doc__
    if docstring:
        try:
            return json.loads(docstring)[index]
        except Exception as e:
            raise ValueError(
                f'Docstring: {docstring!r} in function: {audit_function.__name__!r} is not valid JSON format. Error: {str(e)}')


def join_obj_paths(data_object_paths: list) -> str:
    """Join a list of object paths into a single string for audit messages."""
    if not data_object_paths:
        raise ValueError('No data objects provided for joining paths.')
    # Remove leading and trailing slashes and join with commas
    return ', '.join([audit_link(path_to_text(data_obj), data_obj)for data_obj in data_object_paths])
