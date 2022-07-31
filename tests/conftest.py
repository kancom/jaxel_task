import pytest
from trial.application import Pair


@pytest.fixture
def pair():
    return Pair("USDTRUB")
