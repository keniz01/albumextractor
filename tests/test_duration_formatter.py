import pytest
from formatters.time_formatter import duration_formatter

@pytest.mark.parametrize(
    "test_input, expected_output",
    [(268.89, "04:29"), (968.21,"16:08"), (20000.21,"05:33:20")]
)
def test_duration_formatter(test_input, expected_output):
    result = duration_formatter(test_input)
    assert result == expected_output

def test_duration_formatter_raise_type_error():
    with pytest.raises(Exception):
        duration_formatter("should_be_a_number")    