from pyramid.authorization import (
    Allow,
)
from pyramid.view import view_config
from snovault import (
    Item,
    calculated_property,
    collection,
)
from snovault.attachment import ItemWithAttachment
from igvfd.types.base import Item as IGVFItem
from igvfd.types.base import paths_filtered_by_status


def includeme(config):
    config.scan(__name__, categories=None)
    config.include('.testing_auditor')


@view_config(name='testing-user', request_method='GET')
def user(request):
    return {
        'authenticated_userid': request.authenticated_userid,
        'effective_principals': request.effective_principals,
    }


@view_config(name='testing-allowed', request_method='GET')
def allowed(context, request):
    from pyramid.security import principals_allowed_by_permission
    permission = request.params.get('permission', 'view')
    return {
        'has_permission': bool(request.has_permission(permission, context)),
        'principals_allowed_by_permission': principals_allowed_by_permission(context, permission),
    }


@collection(
    'testing-downloads',
    properties={
        'title': 'Test download collection',
        'description': 'Testing. Testing. 1, 2, 3.',
    },
)
class TestingDownload(ItemWithAttachment):
    item_type = 'testing_download'
    schema = {
        'type': 'object',
        'properties': {
            'attachment': {
                'type': 'object',
                'attachment': True,
                'properties': {
                    'type': {
                        'type': 'string',
                        'enum': ['image/png'],
                    }
                }
            },
            'attachment2': {
                'type': 'object',
                'attachment': True,
                'properties': {
                    'type': {
                        'type': 'string',
                        'enum': ['image/png'],
                    }
                }
            }
        }
    }


@collection(
    'testing-keys',
    properties={
        'title': 'Test keys',
        'description': 'Testing. Testing. 1, 2, 3.',
    },
    unique_key='testing_alias',
)
class TestingKey(Item):
    item_type = 'testing_key'
    schema = {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
                'uniqueKey': True,
            },
            'alias': {
                'type': 'string',
                'uniqueKey': 'testing_alias',
            },
        }
    }


@collection('testing-link-sources')
class TestingLinkSource(Item):
    item_type = 'testing_link_source'
    schema = {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
            },
            'uuid': {
                'type': 'string',
            },
            'target': {
                'type': 'string',
                'linkTo': 'TestingLinkTarget',
            },
            'status': {
                'type': 'string',
            },
        },
        'required': ['target'],
        'additionalProperties': False,
    }


@collection('testing-link-targets', unique_key='testing_link_target:name')
class TestingLinkTarget(Item):
    item_type = 'testing_link_target'
    name_key = 'name'
    schema = {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
                'uniqueKey': True,
            },
            'uuid': {
                'type': 'string',
            },
            'status': {
                'type': 'string',
            },
        },
        'additionalProperties': False,
    }
    rev = {
        'reverse': ('TestingLinkSource', 'target'),
    }
    embedded = [
        'reverse',
    ]

    @calculated_property(schema={
        'title': 'Sources',
        'type': 'array',
        'items': {
            'type': 'string',
            'linkFrom': 'TestingLinkSource.target',
        },
    })
    def reverse(self, request, reverse):
        return paths_filtered_by_status(request, reverse)


@collection(
    'testing-post-put-patch',
    acl=[
        (Allow, 'group.submitter', ['add', 'edit', 'view']),
    ],
)
class TestingPostPutPatch(Item):
    item_type = 'testing_post_put_patch'
    schema = {
        'required': ['required'],
        'type': 'object',
        'properties': {
            'schema_version': {
                'type': 'string',
                'pattern': '^\\d+(\\.\\d+)*$',
                'requestMethod': [],
                'default': '1',
            },
            'uuid': {
                'title': 'UUID',
                'description': '',
                'type': 'string',
                'format': 'uuid',
                'permission': 'admin_only',
                'requestMethod': 'POST',
            },
            'required': {
                'type': 'string',
            },
            'simple1': {
                'type': 'string',
                'default': 'simple1 default',
            },
            'simple2': {
                'type': 'string',
                'default': 'simple2 default',
            },
            'protected': {
                # This should be allowed on PUT so long as value is the same
                'type': 'string',
                'default': 'protected default',
                'permission': 'admin_only',
            },
            'protected_link': {
                # This should be allowed on PUT so long as the linked uuid is
                # the same
                'type': 'string',
                'linkTo': 'TestingLinkTarget',
                'permission': 'admin_only',
            },
        }
    }


@collection('testing-server-defaults')
class TestingServerDefault(Item):
    item_type = 'testing_server_default'
    schema = {
        'type': 'object',
        'properties': {
            'uuid': {
                'serverDefault': 'uuid4',
                'type': 'string',
            },
            'user': {
                'serverDefault': 'userid',
                'linkTo': 'User',
                'type': 'string',
            },
            'now': {
                'serverDefault': 'now',
                'format': 'date-time',
                'type': 'string',
            },
            'accession': {
                'serverDefault': 'accession',
                'accessionType': 'AB',
                'format': 'accession',
                'type': 'string',
            },
        }
    }


@collection('testing-dependencies')
class TestingDependencies(Item):
    item_type = 'testing_dependencies'
    schema = {
        'type': 'object',
        'dependentRequired': {
            'dep1': ['dep2'],
            'dep2': ['dep1'],
        },
        'properties': {
            'dep1': {
                'type': 'string',
            },
            'dep2': {
                'type': 'string',
                'enum': ['dep2'],
            },
        }
    }


@view_config(name='testing-render-error', request_method='GET')
def testing_render_error(request):
    return {
        '@type': ['TestingRenderError', 'Item'],
        '@id': request.path,
        'title': 'Item triggering a render error',
    }


@view_config(context=TestingPostPutPatch, name='testing-retry')
def testing_retry(context, request):
    from sqlalchemy import inspect
    from transaction.interfaces import TransientError

    model = context.model
    attempt = request.environ.get('retry.attempts')

    if attempt == 0:
        raise TransientError()

    return {
        'retry.attempts': attempt,
        'detached': inspect(model).detached,
    }


@collection(
    name='test-igvf-items',
    properties={
        'title': 'Test IGVF Item',
        'description': 'Item to test for set_status properties',
    },
    unique_key='accession',
)
class TestingIGVFItem(IGVFItem):
    item_type = 'test_igvf_item'
    schema = {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'type': 'object',
        'properties': {
            'description': {
                'type': 'string',
            },
            'accession': {
                'title': 'Accession',
                'description': '',
                'type': 'string',
                'format': 'accession',
                'serverDefault': 'accession',
                'permission': 'admin_only',
                'accessionType': 'FI',
            },
            'status': {
                'title': 'Status',
                'type': 'string',
                'permission': 'admin_only',
                'default': 'in progress',
                'description': 'The status of the metadata object.',
                'enum': [
                    'in progress',
                    'released',
                    'preview',
                    'deleted',
                    'replaced',
                    'revoked'
                ]
            }
        }
    }
    name_key = 'accession'
