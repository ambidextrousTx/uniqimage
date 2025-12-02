import argparse
from pathlib import Path
from duplicatefinder import compute_image_hashes, find_duplicates
from imageutils import get_image_info, show_duplicates
from utils import is_image_file, can_scan_folder


def main():
    parser = argparse.ArgumentParser(
        description='Identify duplicate images in a folder')
    parser.add_argument('folder', type=str, help='the target folder')
    args = parser.parse_args()
    input_folder = args.folder
    print(f'Scanning {input_folder} ...')
    target_directory = Path(input_folder)
    if not can_scan_folder(target_directory):
        return

    image_files = [f for f in target_directory.rglob('*') if is_image_file(f)]
    print(f'Found {len(image_files)} files')

    hashes_to_paths = compute_image_hashes(image_files)
    duplicates = find_duplicates(hashes_to_paths)

    if not duplicates:
        print(f'No duplicates found')
        return

    print(f'Found {len(duplicates)} duplicate groups:')
    for count, (image_hash, duplicate_paths) in enumerate(duplicates.items(), start=1):
        image_info = get_image_info(duplicate_paths)
        print(f'Group {count}:')
        for path, width, height in image_info:
            print(f'    {path} -> {width} x {height}')

        show_duplicates(duplicates)


if __name__ == "__main__":
    main()
