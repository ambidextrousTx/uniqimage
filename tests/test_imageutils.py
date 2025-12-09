from PIL import Image
from imageutils import extract_image_dimensions


def test_image_dimension_extraction():
    img = Image.new('RGB', (1920, 1080))
    width, height = extract_image_dimensions(img)
    assert width == 1920
    assert height == 1080
