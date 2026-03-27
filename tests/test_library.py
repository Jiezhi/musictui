import pytest
from src.library import Library
from src.models import Track


def test_library_initialization(tmp_path):
    db_path = tmp_path / "test.db"
    library = Library(str(db_path))
    tracks = library.get_all_tracks()
    assert tracks == []
