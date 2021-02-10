import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Union

import h5py
import numpy as np

# Default parameters for each heatmap layer
# https://github.com/napari/napari/blob/d5a28122129e6eae0f5ada77cb62c4bd5a714b60/napari/layers/base/base.py#L26
RENDERING_DEFAULTS = {
    "visible": True,
    "colormap": "turbo",
    "opacity": 0.5,
}


@dataclass
class Patches:
    coords: np.ndarray
    scores: np.ndarray
    counts: int
    patch_size: Tuple[int, int]
    labels: List[str]

    @classmethod
    def from_h5(cls, path: Union[Path, str]):
        with h5py.File(path) as f:
            coords = f["coords"][:]
            scores = f["attention_scores"][:]
            counts = f["counts"][:][0]

        # TODO: derive these from the blockmap source
        patch_size = (512, 512)
        labels = [
            "Tumor Suppressor Genes",
            "Oncogenes",
            "Protein Kinases",
            "Cell Differentiation Markers",
            "Transcription Factors",
            "Cytokines and Growth Factors",
        ]
        return cls(coords, scores, counts, patch_size, labels)

    def as_layer(
        self, normalize=True, meta=RENDERING_DEFAULTS
    ) -> Tuple[np.ndarray, Dict, str]:

        # Compute the size of the given raster
        size_x, size_y = self.patch_size
        x_min, y_min = np.amin(self.coords, axis=0)
        x_max, y_max = np.amax(self.coords, axis=0) + (size_x, size_y)

        x_len = math.ceil((x_max - x_min) / size_x)
        y_len = math.ceil((y_max - y_min) / size_y)

        # Scale and translate each pixel resolution heatmap to reference size
        meta = {
            **meta,
            **{"translate": (0, y_min, x_min), "scale": (1, size_y, size_x)},
        }

        # Create dense pixel heatmap
        data = np.zeros((len(self.labels), y_len, x_len), dtype="f4")
        for i, label in enumerate(self.labels):

            # Extract attention scores for current heatmap
            scores = self.scores[:, 0, i]

            if normalize:
                # normalize scores for current heatmap between 0-1
                min_score = np.amin(scores)
                scores = (scores - min_score) / (np.amax(scores) - min_score)

            # Fill dense array with corresponding attention scores
            for coord_idx, (left, top) in enumerate(self.coords):
                idx = (
                    i,
                    math.ceil((top - y_min) / size_y),
                    math.ceil((left - x_min) / size_x),
                )
                data[idx] = scores[coord_idx]

        return (data, {**meta, **{"name": "heatmap"}}, "image")
