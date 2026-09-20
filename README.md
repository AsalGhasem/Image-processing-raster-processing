# Image-processing-raster-processing

Hi! I'm a Geomatics Engineering student, and I put this repository together to showcase my transition from utilizing out-of-the-box remote sensing software to writing the underlying spatial algorithms from scratch. 

If you are reviewing my application for a remote sensing or spatial data science role, this project demonstrates my foundational understanding of how pixel manipulation, array operations, and digital image processing actually work under the hood using Python, NumPy, and OpenCV. 

Rather than calling pre-built OpenCV functions for every task, I manually implemented several core raster transformations to solidify my understanding of spectral data processing[cite: 1].

## What's Inside?

The `main.py` script executes a pipeline of standard remote sensing enhancements[cite: 1]:

*   **Custom Histogram Calculation:** I split the raster into its constituent Blue, Green, and Red bands and manually computed the frequency of each pixel intensity (0-255) using a custom loop structure rather than relying on built-in histogram tools[cite: 1]. Understanding spectral distribution is the first step in any remote sensing workflow.
*   **Targeted Contrast Stretching:** I wrote a vectorized piecewise linear transformation to enhance specific intensity ranges[cite: 1]. This is essentially how we highlight specific land cover signatures while suppressing background noise.
*   **2% Linear Stretch:** This implements a dynamic contrast stretch by calculating the lower (`rL`) and upper (`rU`) bounds based on a 2% pixel threshold[cite: 1]. This algorithm clips extreme outliers (like sensor anomalies or extreme reflections) to maximize the visual dynamic range[cite: 1].
*   **Density / Intensity Slicing:** Using NumPy boolean masking, I segmented specific continuous intensity bands into discrete integer values[cite: 1]. This is the algorithmic foundation for simple unsupervised classification (e.g., thresholding water bodies or vegetation)[cite: 1].
*   **Bit-Plane Slicing:** I sliced an 8-bit image into its constituent binary planes[cite: 1], isolating the higher-order bits containing the actual spatial structure from the lower-order bits that largely consist of random sensor noise[cite: 1].
*   **Raster Math (Band Arithmetic):** The script executes element-wise summation, subtraction, multiplication, and division between two `.tif` arrays, followed by a linear contrast stretch to keep the output within a valid 8-bit range[cite: 1]. This logic is the building block for calculating spectral indices like NDVI or MNDWI[cite: 1].

## Tech Stack

*   `opencv-python` (cv2) for image I/O and color space conversions[cite: 1].
*   `numpy` for heavy array manipulation, vectorization, and masking[cite: 1].
*   `matplotlib` for rendering side-by-side comparative visualizations[cite: 1].

## How to Run

1. Clone this repository.
2. Ensure you have the required libraries installed (`pip install opencv-python numpy matplotlib`).
3. Place your sample rasters (named `image_01.tif` and `image_02.tif`) in the root directory[cite: 1].
4. Execute the script:

```bash
python main.py
