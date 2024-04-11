from ..types.base import (
    STATUS_HIERARCHY
)
from snovault import (
    AuditFailure,
    audit_checker,
)
from snovault import (
    UPGRADER,
)
from snovault.schema_utils import validate
from snovault.util import simple_path_ids
from .formatter import (
    audit_link,
    path_to_text,
    space_in_words,
)


@audit_checker('Item', frame='object')
def audit_item_schema(value, system):
    context = system['context']
    registry = system['registry']
    if not context.schema:
        return

    properties = context.properties.copy()
    current_version = properties.get('schema_version', '')
    target_version = context.type_info.schema_version
    if target_version is not None and current_version != target_version:
        upgrader = registry[UPGRADER]
        try:
            properties = upgrader.upgrade(
                context.type_info.name, properties, current_version, target_version,
                finalize=False, context=context, registry=registry)
        except RuntimeError:
            raise
        except Exception as e:
            detail = '%r upgrading from %r to %r' % (
                e, current_version, target_version)
            yield AuditFailure('upgrade failure', detail, level='INTERNAL_ACTION')
            return

        properties['schema_version'] = target_version

    properties['uuid'] = str(context.uuid)
    validated, errors = validate(context.schema, properties, properties)
    for error in errors:
        category = 'validation error'
        path = list(error.path)
        if path:
            category += ': ' + '/'.join(str(elem) for elem in path)
        detail = ('{} {} has schema error {}.'.format(
            space_in_words(value['@type'][0]).capitalize(),
            audit_link(path_to_text(value['@id']), value['@id']),
            error.message
        )
        )
        yield AuditFailure(category, detail, level='INTERNAL_ACTION')


@audit_checker('Item', frame='object')
def audit_item_status(value, system):
    if 'status' not in value:
        return

    # objects with these statuses are not audited
    if value['status'] in ['revoked', 'disabled', 'deleted', 'replaced']:
        return

    if value['status'] in ['archived']:
        level += 30

    level = STATUS_HIERARCHY.get(value['status'], 50)

    context = system['context']
    request = system['request']
    linked = set()

    for schema_path in context.type_info.schema_links:
        linked.update(simple_path_ids(value, schema_path))

    for path in linked:
        # Avoid pulling the full @@object frame into request._embedded_uuids.
        linked_value = request.embed(path + '@@filtered_object?include=@id&include=@type&include=uuid&include=status')
        if 'status' not in linked_value:
            continue
        if linked_value['status'] == 'disabled':
            continue
        linked_level = STATUS_HIERARCHY.get(linked_value['status'], 50)
        if linked_value['status'] in ['archived']:
            linked_level += 30
        if linked_level == 0:
            detail = ('{} {} {} has {} subobject {} {}'.format(
                value['status'].capitalize(),
                space_in_words(value['@type'][0]).lower(),
                audit_link(path_to_text(value['@id']), value['@id']),
                linked_value['status'],
                space_in_words(linked_value['@type'][0]).lower(),
                audit_link(path_to_text(linked_value['@id']), linked_value['@id'])
            )
            )
            yield AuditFailure('mismatched status', detail, level='INTERNAL_ACTION')
        elif linked_level < level:
            detail = ('{} {} {} has {} subobject {} {}'.format(
                value['status'].capitalize(),
                space_in_words(value['@type'][0]).lower(),
                audit_link(path_to_text(value['@id']), value['@id']),
                linked_value['status'],
                space_in_words(linked_value['@type'][0]).lower(),
                audit_link(path_to_text(linked_value['@id']), linked_value['@id'])
            )
            )
            yield AuditFailure('mismatched status', detail, level='INTERNAL_ACTION')
