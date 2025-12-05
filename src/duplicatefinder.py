from PIL import Image
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import imagehash
import logging

logger = logging.getLogger(__name__)


def compute_image_hash(image_path):
    try:
        image = Image.open(image_path)
        image_hash = imagehash.average_hash(image)
        return image_path, image_hash
    except Exception as e:
        logger.error(f"Could not compute image hash for %s".format(image_path))
        return image_path, None


def compute_image_hashes_concurrently(image_paths, verbose=False):
    hashes_to_paths = {}
    logger.info(f"Computing hashes for {len(image_paths)} images...")

    # Each process in the pool gets its own memory, so we cannot
    # pass the hashes_to_paths to the workers. With multiprocessing,
    # it is cleaner to distribute the work of computing hashes and
    # then combine the results in the caller as done here
    with ProcessPoolExecutor() as executor:
        # A simpler solution of using `executor.map` causes tqdm to
        # remain quiet while the workers are computing image hashes
        # This approach is meant to show a progress bar even as the
        # multiprocessing workers are completing because it processes
        # results as they complete
        futures = {executor.submit(compute_image_hash, path): path for path in image_paths}
        for future in tqdm(as_completed(futures), total=len(image_paths),
                           desc="Computing image hashes concurrently",
                           colour="green",
                           disable=verbose):
            image_path, image_hash = future.result()
            if image_hash is not None:
                if image_hash not in hashes_to_paths:
                    hashes_to_paths[image_hash] = []
                hashes_to_paths[image_hash].append(image_path)

    return hashes_to_paths


def compute_image_hashes(image_paths, verbose=False):
    hashes_to_paths = {}
    logger.info(f"Computing hashes for {len(image_paths)} images...")
    count = 0

    for image_path in tqdm(image_paths, desc="Computing image hashes sequentially",
                           colour="green", disable=verbose):
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
