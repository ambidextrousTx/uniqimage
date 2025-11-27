import argparse
from pathlib import Path
from duplicatefinder import compute_image_hashes


def is_image_file(path):
    return path.suffix.lower() in {'.jpg', '.jpeg', '.png'}


def can_scan_folder(folder):
    if not folder.exists():
        print(f"Error: Folder '{folder}' does not exist")
        return False
    if not folder.is_dir():
        print(f"Error: '{folder}' is not a directory")
        return False
    return True


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

    hashes = compute_image_hashes(image_files)


if __name__ == "__main__":
    main()
