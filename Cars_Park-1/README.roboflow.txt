
Cars_Park - v1 2025-01-19 8:13pm
==============================

This dataset was exported via roboflow.com on January 19, 2025 at 1:20 PM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 356 images.
Car are annotated in YOLOv8 format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 640x640 (Stretch)
* Grayscale (CRT phosphor)
* Auto-contrast via adaptive equalization

The following augmentation was applied to create 3 versions of each source image:
* 50% probability of horizontal flip
* Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise
* Randomly crop between 0 and 20 percent of the image
* Random rotation of between -15 and +15 degrees
* Random shear of between -10° to +10° horizontally and -10° to +10° vertically
* Salt and pepper noise was applied to 0.1 percent of pixels


