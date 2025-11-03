import pytest


@pytest.fixture
def temp_traffic_file(tmp_path):
    """Create a temporary file with the given content."""
    def _temp_traffic_file(content: str) -> str:
        file_path = tmp_path / "traffic.txt"
        with open(file_path, "w") as f:
            f.write(content)
        return file_path

    return _temp_traffic_file
