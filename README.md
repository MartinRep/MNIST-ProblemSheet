# Emerging Technologies MNIST Problem sheet

## Problem set: Read the MNIST data files
These problems relate to the famous [MNIST](http://yann.lecun.com/exdb/mnist/) data set.
Save your work as a Python file, or a collection of Python files.
Place them in a single repository on [GitHub](https://github.com/), complete with a README.
The files are in a bespoke format, as described on the [website](http://yann.lecun.com/exdb/mnist/).


### 1. Read the data files
Download the image and label files.
Have Python decompress and read them byte by byte into appropriate data structures in memory.

### 2. Output an image to the console
Output the third image in the training set to the console.
Do this by representing any pixel value less than 128 as a full stop and any other pixel value as a hash symbol.

### 3. Output the image files as PNGs
Use Python to output the image files as PNGs, saving them in a subfolder in your repository.
Name the images in the format `train-XXXXX-Y.png` or `test-XXXXX-Y.png` where `XXXXX` is the image number (where it occurs in the data file) and `Y` is its label.
For instance, the five-thousandth training image is labelled 2, so its file name should be `train-04999-2.png`.
Note the images are indexed from 0, so the five-thousandth image is indexed as 4999.
See below for an example of it.
Commit these image files to GitHub.

# Solution

### Output
![Execution times](https://github.com/MartinRep/MNIST-ProblemSheet/blob/master/MNIST%20Execution%20times.PNG)
