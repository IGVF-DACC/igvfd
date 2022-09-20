import pytest
from unittest import TestCase


def test_page_upgrade_2_3(upgrader, page_v2):
    value = upgrader.upgrade('page', page_v2, current_version='2', target_version='3')
    assert value['schema_version'] == '3'
    assert 'news' not in value
    assert 'news_excerpt' not in value
    assert 'news_keywords' not in value
    assert 'layout' in value and 'rows' not in value['layout']
    assert 'blocks' in value['layout']
    assert len(value['layout']['blocks']) == 1
    TestCase().assertListEqual(
        value['layout']['blocks'],
        [
            {
                '@id': '#block1',
                '@type': 'markdown',
                'body': '<p></p>',
                'direction': 'ltr'
            }
        ]
    )
