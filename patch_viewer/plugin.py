from pathlib import Path
from typing import Union

from napari_lazy_openslide.lazy_openslide import reader_function
from napari_plugin_engine import napari_hook_implementation

from .patches import Patches

SUFFIX = "_blockmap.h5"

# TODO: Fix me! This is a very naive way to try to find the associated slide.
#
# This algorithm walks backward from the directory containing the h5 file to try
# to find the associated slide. It will "walk' up the tree greedily (max_level times),
# regexing for _first_ file that contains the `slide_id`. If no file is found, it
# raises an exception.
#
# It would be ideal to have the `_blockmap.h5` file contain an exact file name for
# the source so we can look for that _exact_ file (and not just a file with a shared ID,
# which is common between other outputs from clam).
def find_slide(path: Union[Path, str], max_level=2) -> Path:
    if isinstance(path, str):
        path = Path(path)
    slide_id = path.name[: -len(SUFFIX)]

    # Inspect the same directory as the .h5 file
    data_dir = path.absolute().parent
    for _ in range(max_level):
        for file in data_dir.glob(f"**/*{slide_id}*"):
            if file != path:
                # File is not the h5 but contains the slide_id
                return file
        # Jump up a directory level
        data_dir = data_dir.parent

    raise Exception(f"Cannot find corresponding WSI for ID: {slide_id}")


@napari_hook_implementation
def napari_get_reader(path: str):
    if isinstance(path, str) and path.endswith(SUFFIX):
        return patch_reader


def patch_reader(path: str):
    # Load slide
    slide_path = find_slide(path)
    pyramid_layer = reader_function(str(slide_path))[0]

    # Load patches
    patches = Patches.from_h5(path)

    return [pyramid_layer, patches.as_layer()]
