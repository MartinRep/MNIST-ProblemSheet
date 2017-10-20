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


### 1. Read the data files
```
 arrays = [int.from_bytes(f.read(4), byteorder="big") for i in range(magic[3])] # Reads data arrays size 4 bytes each. Array size is defined by files magic number
            numOfImg, rows, columns = arrays[0], arrays[1], arrays[2] # Just a transfer to more human readable variables
            print("\nWorking on a file %s processing %d images. Please wait..." % (filename, numOfImg))
            pic_array = np.fromstring(f.read(numOfImg * rows * columns), np.dtype(('uint8', 1)))    # example reads 60,000 x 28 x 28 pixels at once
            return pic_array.reshape(numOfImg, rows, columns)
```

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
for index, image in enumerate(data[title]): # Loops over data hashmap of specified title, enumerating index too
        cur_img = np.array(image)
        cur_img = pil.fromarray(cur_img).convert('RGB') # PIL.Image library converts array into image
        out_filename = '-{:06.0f}-'.format(index)  # formats filename to include zeros
        out_dir = src_dir + title + "/"
        out_filename = out_dir + title + out_filename + str(labels[title][index]) + ".png" # combines name with index and digit with extension
        try:    # tries to create output directory.
            os.makedirs(out_dir)
        except OSError:
            pass
        cur_img.save(out_filename) # Saves the file
```

### Output
![Execution times](https://github.com/MartinRep/MNIST-ProblemSheet/blob/master/MNIST%20Execution%20times.PNG)
