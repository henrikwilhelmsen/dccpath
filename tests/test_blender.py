import pytest


def test_which_blender() -> None:
    pass


@pytest.mark.parametrize(
    ("input", "expected"),
    [
        ("some_input", "some_expected_result"),
    ],
)
def test_blender(input: str, expected: str) -> None:
    pass
