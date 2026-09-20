# Image Processing & Raster Processing

A Python-based implementation of fundamental digital image processing and raster processing techniques commonly used in remote sensing.

The project focuses on implementing core raster transformations using **NumPy** and **OpenCV**, with an emphasis on understanding pixel-level operations, array manipulation, and image enhancement algorithms.

## What's Inside?

The `main.py` script implements a pipeline of raster and image-processing operations:

* **Custom Histogram Calculation:** Separates the raster into Blue, Green, and Red bands and calculates the frequency of each pixel intensity (0–255) using a custom loop-based implementation.

* **Targeted Contrast Stretching:** Applies a vectorized piecewise linear transformation to enhance selected intensity ranges.

* **2% Linear Stretch:** Calculates lower (`rL`) and upper (`rU`) intensity bounds based on a 2% pixel threshold and applies a linear contrast stretch to reduce the influence of extreme pixel values.

* **Density / Intensity Slicing:** Uses NumPy boolean masking to divide continuous intensity ranges into discrete classes based on predefined thresholds.

* **Bit-Plane Slicing:** Decomposes an 8-bit image into its individual binary bit planes to examine the contribution of each bit to the image's spatial information.

* **Raster Math (Band Arithmetic):** Performs element-wise addition, subtraction, multiplication, and division between two `.tif` raster arrays, followed by contrast stretching to produce a valid 8-bit output. This type of pixel-wise band arithmetic forms the basis of spectral index calculations such as NDVI and MNDWI.

## Tech Stack

* **Python**
* **NumPy** — array manipulation, vectorization, and boolean masking
* **OpenCV** — image input/output and image processing
* **Matplotlib** — visualization and comparison of processed images

## How to Run

1. Clone the repository.

2. Install the required dependencies:

```bash
pip install opencv-python numpy matplotlib
```

3. Place the sample raster files in the project root directory:

```text
image_01.tif
image_02.tif
```

4. Run the main script:

```bash
python main.py
```
