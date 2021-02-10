# patch-viewer

🐧 WIP

### Installation

```bash
$ conda create -n patch-viewer python=3.9
$ conda activate patch-viewer
$ pip install "napari[all]" # install napari
$ pip install -e . # install patch-viewer plugin (as editable)
```


### Usage

```bash
$ napari # opens viewer, can drag and drop files
# or 
$ napari path/to/my_blockmap.h5 # automatically loads view for file
```