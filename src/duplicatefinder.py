from PIL import Image
import imagehash


def compute_image_hashes(image_paths):
    hashes_to_paths = {}
    print(f"Computing hashes for {len(image_paths)} images...")
    count = 0

    for image_path in image_paths:
        count += 1
        print(f"Processed {count}/{len(image_paths)}")
        try:
            image = Image.open(image_path)
            image_hash = imagehash.average_hash(image)

            if image_hash not in hashes_to_paths:
                hashes_to_paths[image_hash] = []
            hashes_to_paths[image_hash].append(image_path)

        except Exception as e:
            print(f"Warning: Could not process {image_path}: {e}")
            continue

    print('Done')
    return hashes_to_paths.values()
