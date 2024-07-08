## Image Processor: A Tool for Removing Watermarks from Images

This repository provides a simple yet effective tool for removing watermarks from images using PaddleOCR and OpenCV. It leverages the power of deep learning for text detection and inpainting techniques for seamless removal.

**Features:**

* **Automatic Watermark Detection:** Utilizes PaddleOCR to accurately identify text in images, even those with complex backgrounds.
* **Interactive Removal:** Provides a visual interface to refine the removal process by manually selecting areas for removal.
* **Batch Processing:** Allows processing multiple images at once, streamlining the workflow.
* **Save and Replace:** Saves the processed images with a "_fixed" suffix and optionally replaces the original images.



**Getting Started:**

1. **Prerequisites:**
   * Python 3.6 or higher
   * PyQt5
   * OpenCV
   * PaddleOCR (Install using `pip install paddleocr`)
2. **Installation:**
   * Clone the repository: `git clone https://github.com/zhangheli/py-image-remover.git`
   * Navigate to the project directory: `cd py-image-remover`
   * Install the required packages: `pip install -r requirements.txt`
3. **Running the Application:**
   * Execute the main script: `python app.py`

**Usage:**

1. Click the "Start" button to open a file dialog.
2. Select the images you want to process.
3. The application will automatically detect and remove watermarks from each image.
4. You can further refine the removal process by:
   * **Selecting areas:** Use the left mouse button to draw a circle around the remaining watermark.
   * **Applying changes:** Press Enter to apply the selection and remove the watermark.
   * **Saving the image:** Press Q to save the processed image and continue to the next image.

**Example:**

![Example](https://github.com/zhangheli/py-image-remover/blob/main/example.png)

**License:**

This project is licensed under the MIT License.

**Contributing:**

Contributions are welcome! Feel free to open an issue or submit a pull request.

**Acknowledgements:**

* PaddlePaddle for providing the PaddleOCR library.
* OpenCV for image processing functionalities.
* PyQt5 for the graphical user interface.

**Disclaimer:**

This tool is intended for personal use and educational purposes. It is not guaranteed to work perfectly on all images and may not be suitable for commercial use.