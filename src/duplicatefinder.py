from PIL import Image
import imagehash
import logging

logger = logging.getLogger(__name__)


def compute_image_hashes(image_paths):
    hashes_to_paths = {}
    logger.info(f"Computing hashes for {len(image_paths)} images...")
    count = 0

    for image_path in image_paths:
        count += 1
        logger.info(f"Processed {count}/{len(image_paths)}")
        try:
            image = Image.open(image_path)
            image_hash = imagehash.average_hash(image)

            if image_hash not in hashes_to_paths:
                hashes_to_paths[image_hash] = []
            hashes_to_paths[image_hash].append(image_path)

        except Exception as e:
            logger.error(f"Could not process {image_path}: {e}")
            continue

    logger.debug('Done')
    return hashes_to_paths


def find_duplicates(hashes_to_paths):
    duplicates = {image_hash: image_paths for image_hash, image_paths in hashes_to_paths.items() if len(image_paths) > 1}
    logger.info(f'Found {len(duplicates)}')
    logger.info(duplicates)
    return duplicates
