import pytest


def test_multiplexer_init_multiplexer_config():
    from infrastructure.constructs.existing.igvf_dev import Resources
    from infrastructure.multiplexer import MultiplexerConfig
    config = MultiplexerConfig(
        construct_id='ABC',
        on=False,
        construct_class=Resources,
        kwargs={}
    )
    assert config.construct_id == 'ABC'
    assert config.on == False
    assert issubclass(config.construct_class, Resources)
    assert config.kwargs == {}


def test_multiplexer_init_multiplexer():
    from aws_cdk import Stack
    from infrastructure.constructs.existing import igvf_dev
    from infrastructure.multiplexer import MultiplexerConfig
    from infrastructure.multiplexer import Multiplexer
    stack = Stack(
        env=igvf_dev.US_WEST_2
    )
    config = MultiplexerConfig(
        construct_id='ABC',
        on=False,
        construct_class=igvf_dev.Resources,
        kwargs={}
    )
    multiplexer = Multiplexer(
        scope=stack,
        configs=[config],
    )
    assert multiplexer.resources == {}
    config = MultiplexerConfig(
        construct_id='ABC',
        on=True,
        construct_class=igvf_dev.Resources,
        kwargs={}
    )
    multiplexer = Multiplexer(
        scope=stack,
        configs=[config],
    )
    assert isinstance(multiplexer.resources['ABC'], igvf_dev.Resources)
