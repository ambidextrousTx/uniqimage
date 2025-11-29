from PIL import Image


def get_image_info(image_paths):
    # [(Path('img1.jpg'), 1920, 1080), (Path('img2.jpg'), 800, 600)]
    image_info = []
    for image_path in image_paths:
        try:
            image = Image.open(image_path)
            width, height = image.size
            image_info.append((image_path, width, height))
        except Exception as e:
            print("Error reading image {}: {}".format(image_path, e))

    return image_info
