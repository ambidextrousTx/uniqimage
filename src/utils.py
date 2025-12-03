import logging

logger = logging.getLogger(__name__)


def is_image_file(path):
    return path.suffix.lower() in {'.jpg', '.jpeg', '.png'}


def can_scan_folder(folder):
    if not folder.exists():
        logger.error(f"Folder '{folder}' does not exist")
        return False
    if not folder.is_dir():
        logger.error(f"Folder '{folder}' is not a directory")
        return False
    return True
