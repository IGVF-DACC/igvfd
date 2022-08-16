import pytest


@pytest.fixture
def page(testapp):
    item = {
        'name': 'igvf-page',
        'title': 'IGVF Page',
        'layout': {
            'blocks': [
                {
                    '@id': '#block1',
                    '@type': 'markdown',
                    'body': '<p></p>',
                    'direction': 'ltr'
                }
            ]
        }
    }
    return testapp.post_json('/page', item, status=201).json['@graph'][0]


@pytest.fixture
def page_v2(page):
    item = page.copy()
    item.update({
        'schema_version': '2',
    })
    return item
