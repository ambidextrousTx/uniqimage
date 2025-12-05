# uniqimage

## De-duplicate images locally based on image contents

You will need to install the following locally
* uv for dependency and environment management
* tkinter for the GUI
* tqdm for the progress bar
* imagehash for calculating image hashes
* PIL to work in conjunction with tkinter and imagehash
* Python >= 3.13

`uv` takes care of the other libraries, but especially for
`tkinter` you might have to do what is necessary for your
specific environment because your Python may not be
configured with it.

## Running the app

```bash
$ uv run src/scanner.py /path/to/images/folder
```

Computes image hashes and collects images with the same
(similar) hashes. Then shows them in a GUI as similar
'duplicate groups'. The content-based hashing algorithm
is simplistic - sometimes e.g. if two images differ in
the orientation of a face, it might still think they are
duplicates. Always double-check the output.

Image dimensions are also displayed, which might help
decide which copy to keep. Finally, you may either copy
the path to a duplicate or reveal them in the file 
manager and delete it.
