# patch-viewer (Napari)

🐧 WIP

### 1. Anaconda
Install [Anaconda](https://www.anaconda.com/products/individual) for your operating system (Choosing the Graphical or Command Line Installer depends on your preference).

### 2. Install MacOS System Dependencies (Brew + OpenSlide)
Brew is a Package Manager for MacOS that can be installed with these [instructions](https://brew.sh/). To install, open Terminal and copy+paste:
```bash
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Once Brew is installed, you can install OpenSlide via:
```bash
$ brew install openslide
$ pip-python3 install openslide-python
```

### 3. Install Python Dependencies for Napari
```bash
$ conda create -n patch-viewer python=3.9
$ conda activate patch-viewer
$ pip install "napari[all]" # install napari
$ pip install -e . # install patch-viewer plugin (as editable)
```

### 4. Napari Usage

To Open Napari:
```bash
$ napari # opens viewer, can drag and drop files
# or 
$ napari path/to/my_blockmap.h5 # automatically loads view for file
```
