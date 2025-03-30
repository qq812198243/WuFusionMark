# Image Annotation Tool

## Project Overview
This is an image annotation tool based on Qwen-VL-Max API and OpenCV, which can automatically recognize objects in images and generate bounding boxes with labels.

## Features
- Support image URL input
- Automatically recognize objects and annotate them
- Preview and save annotation results
- Provide a simple graphical user interface

## Installation Guide
```bash
pip install -r requirements.txt
```

## Usage
1. Run `main_window.py` to start the GUI
2. Enter API key and image URL
3. Click "Start Annotation" button
4. View and save the annotation results

## Technical Details
- Use Qwen-VL-Max API for image recognition
- Use OpenCV for image processing and annotation drawing
- Use PyQt5 to build the user interface

## Example Code
```python
# Basic usage example
from draw_objects import ImageAnnotator

# Create annotator instance
annotator = ImageAnnotator(json_data, "image.jpg")

# Load and annotate image
annotator.load_image()
annotator.draw_annotations()
annotator.show_result()
annotator.save_result()
```

## Notes
- Valid API key required
- Image URL must be publicly accessible
- Annotation results will be saved in local "img" folder
- Register at https://bailian.console.aliyun.com/ to get API key, then fill it in the `api_key` variable in code.

## Contribution
Issues and suggestions are welcome, or you can directly submit Pull Requests.

## License
MIT License

## Author
- [allenW]
- Contact: qq:812198243

## Version History
- v1.0.0 Initial version with basic features

## Project Name
Multimodal Image Annotation Tool