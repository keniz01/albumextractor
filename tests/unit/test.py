import pytest

@pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])
class TestClass:
    def test_run(self, n, expected):
        pass