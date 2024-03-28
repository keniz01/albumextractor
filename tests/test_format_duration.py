import pytest
from main import format_duration

@pytest.mark.parametrize(
    "test_input, expected_output",
    [(268.89, "04:29"), (968.21,"16:08"), (20000.21,"05:33:20")]
)
def test_format_duration(test_input, expected_output):
    result = format_duration(test_input)
    assert result == expected_output

def test_format_duration_raise_type_error():
    with pytest.raises(Exception):
        format_duration("should_be_a_number")    