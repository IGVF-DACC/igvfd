import importlib
import json
import pkgutil

import igvfd.audit


NON_AUDIT_FUNCTION_NAMES = [
    'audit_checker',
    'audit_link'
]

EXCLUDED_MODULES = {'igvfd.audit.item'}

AUDIT_MODULES_TO_PROCESS = [
    importlib.import_module(name)
    for importer, name, ispkg in pkgutil.walk_packages(
        igvfd.audit.__path__,
        prefix='igvfd.audit.'
    )
    if name not in EXCLUDED_MODULES
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
