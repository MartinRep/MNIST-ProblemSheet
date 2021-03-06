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

# Solution
 - Clone this repo.
 - Place downloaded `.gz` files into `data/` folder.
 - Download & Install [Python](https://www.python.org/downloads/)
 - Run `pip install -r requirements.txt` to install dependancies
 - Finally `python FileProcess.py`
 - Output files will be in their respected subdirectories inside `/data` folder

### 1. Read the data files
`pic_array = np.fromstring(f.read(numOfImg * rows * columns), np.dtype(('uint8', 1)))` reads all the pixels at once  
`images = pic_array.reshape(numOfImg, rows, columns)` Transform 1D array into 3D array

### 2. Output an image to the console
```
for column, col in enumerate(image): # enumerable used instead od range(len(image))
        for pixel, pix in enumerate(col):
            # print(image[column][pixel]) # Prints out the raw byte values of pixels as an image
            if image[column][pixel] > 128: # Replaces pixel colors dark for '#' bright for '.'
                print("#", end='')
            else:
                print(".", end='')
        print("", end='\n')
```

### 3. Output the image files as PNGs
```
cur_img = np.array(image)
cur_img = pil.fromarray(cur_img).convert('RGB') # PIL.Image library converts array into image
out_filename = '-{:06.0f}-'.format(index)  # formats filename to include zeros
out_filename = out_dir + title + out_filename + str(labels[title][index]) + ".png" # combines name with index and digit with extension
cur_img.save(out_filename) # Saves the file
```

### Output
![Execution times](https://github.com/MartinRep/MNIST-ProblemSheet/blob/master/MNIST%20Execution%20times.PNG)
