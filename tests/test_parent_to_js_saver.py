from src.parent_to_json_saver import Storage
import pytest


def test_parent_to_js_saver_is_abstract():
    with pytest.raises(TypeError):
        Storage()
