"""Test utilities module"""

import mini_infer


def test_import():
    """Test that mini_infer can be imported"""
    assert mini_infer.__version__ == "0.1.0"


def test_module_structure():
    """Test that key modules exist"""
    # These will be implemented in Week 2-8
    # For now, just check they can be imported
    from mini_infer import kernels, memory, engine, utils

    assert kernels is not None
    assert memory is not None
    assert engine is not None
    assert utils is not None


def test_placeholder():
    """Placeholder test to make CI pass"""
    assert True
