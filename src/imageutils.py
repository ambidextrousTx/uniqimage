from PIL import Image, ImageTk
import tkinter as tk
import subprocess
import logging

logger = logging.getLogger(__name__)


def append_path_to_clipboard(root, path):
    root.clipboard_clear()
    root.clipboard_append(path.name)


def reveal_in_finder(path):
    subprocess.run(["open", "-R", str(path)])


def show_duplicates(duplicates):
    root = tk.Tk()
    root.title("Duplicates Found")

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for group_num, (img_hash, paths) in enumerate(duplicates.items(), start=1):
        group_frame = tk.Frame(scrollable_frame, borderwidth=2, relief="groove")
        group_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(group_frame, text=f"Group {group_num}", font=("Arial", 12, "bold")).pack()

        images_frame = tk.Frame(group_frame)
        images_frame.pack()

        image_info = get_image_info(paths)
        for path, width, height in image_info:
            img_frame = tk.Frame(images_frame)
            img_frame.pack(side="left", padx=5)  # side="left" puts them horizontally

            try:
                image = Image.open(path)
                image.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(image=image)
                image_label = tk.Label(img_frame, image=photo)
                image_label.image = photo
                image_label.pack()
                copy_btn = tk.Button(img_frame, text="Copy Path", command=lambda p=path: append_path_to_clipboard(root, p))
                copy_btn.pack()
                reveal_in_finder_btn = tk.Button(img_frame, text="Reveal in Finder", command=lambda p=path:reveal_in_finder(p))
                reveal_in_finder_btn.pack()
            except Exception as e:
                logger.error("Could not load image", e)

            info_label = tk.Label(img_frame, text=f"{path.name}\n{width}x{height}")
            info_label.pack()

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()


def extract_image_dimensions(image):
    width, height = image.size
    return width, height


def get_image_info(image_paths):
    # [(Path('img1.jpg'), 1920, 1080), (Path('img2.jpg'), 800, 600)]
    image_info = []
    for image_path in image_paths:
        try:
            image = Image.open(image_path)
            width, height = extract_image_dimensions(image)
            image_info.append((image_path, width, height))
        except Exception as e:
            logger.error("Error reading image {}: {}".format(image_path, e))

    return image_info
