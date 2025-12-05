import argparse
import logging
from pathlib import Path
from duplicatefinder import compute_image_hashes_concurrently, find_duplicates
from imageutils import get_image_info, show_duplicates
from utils import is_image_file, can_scan_folder

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Identify duplicate images in a folder')
    parser.add_argument('folder', type=str, help='the target folder')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    set_up_logging(args)

    input_folder = args.folder
    logger.info(f'Scanning {input_folder} ...')
    target_directory = Path(input_folder)
    if not can_scan_folder(target_directory):
        return

    image_files = [f for f in target_directory.rglob('*') if is_image_file(f)]
    logger.info(f'Found {len(image_files)} files')

    hashes_to_paths = compute_image_hashes_concurrently(image_files)
    duplicates = find_duplicates(hashes_to_paths)

    if not duplicates:
        logger.warning(f'No duplicates found')
        return

    logger.info(f'Found {len(duplicates)} duplicate groups:')
    for count, (image_hash, duplicate_paths) in enumerate(duplicates.items(), start=1):
        image_info = get_image_info(duplicate_paths)
        logger.debug(f'Group {count}:')
        for path, width, height in image_info:
            logger.debug(f'    {path} -> {width} x {height}')

        show_duplicates(duplicates)


def set_up_logging(args):
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)


if __name__ == "__main__":
    main()
