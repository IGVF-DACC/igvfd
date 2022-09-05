import pytest


@pytest.fixture
def page(testapp):
    item = {
        'name': 'igvf-page',
        'title': 'IGVF Page',
        'news': True,
        'news_excerpt': 'Don’t miss the abstract deadline for ENCODE Users Meeting.',
        'news_keywords': ['Conferences', 'Encyclopedia'],
        'layout': {
            'rows': [
                {
                    'cols': [
                        {
                            'blocks': [
                                '#block1'
                            ]
                        }
                    ]
                }
            ],
            'blocks': [
                {
                    '@id': '#block1',
                    '@type': 'richtextblock',
                    'body': '<p></p>'
                },
                {
                    '@id': '#block4',
                    '@type': 'teaserblock',
                    'image': '/images/8a91ae78-731a-4a92-ae7c-273214be408a/',
                    'body': '<h2>Chromatin Structure</h2>',
                    'href': '/about/chromatin-structure'
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
