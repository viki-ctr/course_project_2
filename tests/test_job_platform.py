import pytest
from src.job_platform import JobPlatformApi


def test_job_platform_is_abstract():
    with pytest.raises(TypeError):
        JobPlatformApi()
