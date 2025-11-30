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
