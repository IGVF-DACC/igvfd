import json

import igvfd.audit.analysis_set
import igvfd.audit.auxiliary_set
import igvfd.audit.biosample
import igvfd.audit.construct_library_set
import igvfd.audit.curated_set
import igvfd.audit.file_set
import igvfd.audit.file
import igvfd.audit.formatter
import igvfd.audit.human_donor
import igvfd.audit.in_vitro_system
import igvfd.audit.index_file
import igvfd.audit.matrix_file
import igvfd.audit.measurement_set
import igvfd.audit.multiplexed_sample
import igvfd.audit.ontology_term
import igvfd.audit.reference_file
import igvfd.audit.sequence_file
import igvfd.audit.sample
import igvfd.audit.tissue
import igvfd.audit.treatment
import igvfd.audit.whole_organism


NON_AUDIT_FUNCTION_NAMES = [
    'audit_checker',
    'audit_link',
    'register_dispatcher',
    'register_all_dispatchers'
]

AUDIT_MODULES_TO_PROCESS = [
    igvfd.audit.analysis_set,
    igvfd.audit.auxiliary_set,
    igvfd.audit.biosample,
    igvfd.audit.construct_library_set,
    igvfd.audit.curated_set,
    igvfd.audit.file_set,
    igvfd.audit.file,
    igvfd.audit.formatter,
    igvfd.audit.human_donor,
    igvfd.audit.in_vitro_system,
    igvfd.audit.index_file,
    igvfd.audit.matrix_file,
    igvfd.audit.measurement_set,
    igvfd.audit.multiplexed_sample,
    igvfd.audit.ontology_term,
    igvfd.audit.reference_file,
    igvfd.audit.sequence_file,
    igvfd.audit.sample,
    igvfd.audit.tissue,
    igvfd.audit.treatment,
    igvfd.audit.whole_organism,
]


def get_audit_function_names_from_module(module):
    module_attributes = dir(module)
    audit_function_names = [
        attribute for attribute in module_attributes
        if attribute.startswith('audit_')
        and attribute not in NON_AUDIT_FUNCTION_NAMES
        and not attribute.endswith('_dispatcher')
    ]
    return audit_function_names


def get_docstring_dict_from_function_name(function_name):
    docstring = eval(function_name + '.__doc__')
    if docstring is not None:
        try:
            docstring = json.loads(docstring)
            return {function_name: docstring}
        except:
            raise ValueError(f'Docstring: {docstring} in function: {function_name} is not valid JSON format.')
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
