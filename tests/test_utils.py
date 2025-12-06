from pathlib import Path
from utils import is_image_file


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
