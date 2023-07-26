import json

import igvfd.audit.biosample
import igvfd.audit.construct_library
import igvfd.audit.formatter
import igvfd.audit.human_donor
import igvfd.audit.in_vitro_system
import igvfd.audit.item
import igvfd.audit.curated_set
import igvfd.audit.measurement_set
import igvfd.audit.curated_set
import igvfd.audit.ontology_term
import igvfd.audit.sample
import igvfd.audit.sequence_file
import igvfd.audit.tissue
import igvfd.audit.treatment
import igvfd.audit.variant
import igvfd.audit.whole_organism


NON_AUDIT_FUNCTION_NAMES = [
    'audit_checker',
    'audit_link',
]

AUDIT_MODULES_TO_PROCESS = [
    igvfd.audit.biosample,
    igvfd.audit.construct_library,
    igvfd.audit.formatter,
    igvfd.audit.human_donor,
    igvfd.audit.in_vitro_system,
    igvfd.audit.item,
    igvfd.audit.curated_set,
    igvfd.audit.measurement_set,
    igvfd.audit.curated_set,
    igvfd.audit.ontology_term,
    igvfd.audit.sample,
    igvfd.audit.sequence_file,
    igvfd.audit.tissue,
    igvfd.audit.treatment,
    igvfd.audit.variant,
    igvfd.audit.whole_organism,
]


def get_audit_function_names_from_module(module):
    module_attributes = dir(module)
    audit_function_names = [attribute for attribute in module_attributes if attribute.startswith(
        'audit_') and attribute not in NON_AUDIT_FUNCTION_NAMES]
    return audit_function_names


def parse_string_to_dictionary(docstring):
    '''
        The expected input for the docstring is as follows:
            audit_details: audit details
            audit_categories: audit categories
            audit_levels: ERROR, WARNING, NON_COMPLIANT
        There should be three "keys": audit_details, audit_categories, and audit_levels.
        The audit_levels should be seperated by commas. Additional keys or values starting with "audit_"
        should not be included in the input docstring. Ideally the input docstring keys should be in
        order as above for readability between docstrings, but this function allows for them to be out
        of order. It also removes whitespace within a key's value, including newlines.
    '''
    lines = docstring.strip().split('\n')
    single_line = ' '.join(line.strip() for line in lines)
    result_dict = {
        'audit_detail': '',
        'audit_category': '',
        'audit_levels': []
    }
    if 'audit_detail:' in single_line:
        after_audit_detail = single_line.split('audit_detail:')[1].strip()
        if 'audit_' in after_audit_detail:
            result_dict['audit_detail'] = after_audit_detail.split('audit_')[0].strip()
        else:
            result_dict['audit_detail'] = after_audit_detail
    if 'audit_category:' in single_line:
        after_audit_category = single_line.split('audit_category:')[1].strip()
        if 'audit_' in after_audit_category:
            result_dict['audit_category'] = after_audit_category.split('audit_')[0].strip()
        else:
            result_dict['audit_category'] = after_audit_category
    if 'audit_levels:' in single_line:
        after_audit_levels = single_line.split('audit_levels:')[1]
        if 'audit_' in after_audit_levels:
            audit_levels_str = after_audit_levels.split('audit_')[0].strip()
            result_dict['audit_levels'] = [level.strip() for level in audit_levels_str.split(',')]
        else:
            audit_levels_str = after_audit_levels.strip()
            result_dict['audit_levels'] = [level.strip() for level in audit_levels_str.split(',')]
    return result_dict


def get_docstring_dict_from_function_name(function_name):
    docstring = eval(function_name + '.__doc__')
    if docstring is not None:
        dict_docstring = parse_string_to_dictionary(docstring)
        return {function_name: dict_docstring}
    else:
        return {function_name: {}}


def main():
    audit_function_full_names = []
    for audit_module in AUDIT_MODULES_TO_PROCESS:
        module_name = audit_module.__name__
        function_names_in_module = get_audit_function_names_from_module(audit_module)
        for function_name in function_names_in_module:
            audit_function_full_names.append(module_name + '.' + function_name)
    audit_docstring_dict = {}
    for function_name in audit_function_full_names:
        audit_docstring_dict.update(get_docstring_dict_from_function_name(function_name))
    with open('src/igvfd/static/doc/auditdoc.json', 'w') as audit_json:
        json.dump(audit_docstring_dict, audit_json)


if __name__ == '__main__':
    main()
