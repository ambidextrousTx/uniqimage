import tempfile
from pathlib import Path
from utils import is_image_file, can_scan_folder


def test_can_read_jpg():
    path = Path('test_fixtures/image2.jpg')
    assert is_image_file(path)


def test_can_read_png():
    path = Path('test_fixtures/image1.png')
    assert is_image_file(path)


def test_is_image_file_case_insensitive():
    path = Path('test_fixtures/image4.JPG')
    assert is_image_file(path)


def test_is_image_file_rejects_non_images():
    path = Path('test_fixtures/image.txt')
    assert not is_image_file(path)


def test_can_scan_folder_valid_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        assert can_scan_folder(Path(tmpdir))


def test_can_scan_folder_nonexistent():
    assert not can_scan_folder(Path('/this/does/not/exist'))


def test_can_scan_folder_file_not_directory():
    with tempfile.NamedTemporaryFile('r+') as tmpfile:
        assert not can_scan_folder(Path(tmpfile.name))
    pass
