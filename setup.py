import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="patch-viewer",
    version="0.0.1",
    author="Trevor Manz",
    author_email="trevor.j.manz@gmail.com",
    description="A napari plugin to view attention-based heatmaps for whole slide images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manzt/patch-viewer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: napari",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "napari-plugin-engine>=0.1.9",
        "napari-lazy-openslide>=0.2.0",
        "napari>=0.4.3",
        "h5py>=3.0",
        "numpy",
    ],
    entry_points={
        "napari.plugin": ["patch-viewer = patch_viewer.plugin"],
    },
)
