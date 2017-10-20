# Adapted from https://stackoverflow.com/questions/120656/directory-listing-in-python#120701
#              https://stackoverflow.com/questions/8703496/hash-map-in-python#8703509
#              https://pyformat.info/
#              https://stackoverflow.com/questions/517127/how-do-i-write-output-in-same-place-on-the-console#517207
#              https://stackoverflow.com/questions/1274405/how-to-create-new-folder#1274465
#              https://stackoverflow.com/questions/11760095/convert-binary-string-to-numpy-array
#              https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html
import os
import gzip
import numpy as np
import PIL.Image as pil
import datetime

labels = {}
data = {}
src_dir = "data/" # data files directory


def get_gz_files(loc_directory): # List all the files in directory
    files = dict()
    for filename in os.listdir(loc_directory): # reads list files of loc_directory and loops through them
        if ".gz" in filename: # adds only Gzip files to the list
            files[filename[:filename.index("-", filename.index("-")+1)]] = filename # Directory (hash-map) key = filename up to second "-", Value = filename
    return files


def read_file(filename):
    with gzip.open(filename, 'rb') as f: # Opens file specied by filename a assaign it to f
        magic = f.read(4) # Reads magic number
        if magic[3] == 1: # Check for number of dimensions in a file, if 1 the file is considered LABEL file
            cur_labels = [] # Creates array so .append can be used later on
            items = int.from_bytes(f.read(4), byteorder="big") # get size of the items array
            for label in range(items):
                cur_labels.append(int.from_bytes(f.read(1), byteorder="big")) # Reads labels byte by byte
            print("\nRead %d labels from %s" % (len(cur_labels), filename))
            return cur_labels
        else: # image file with data
            arrays = [int.from_bytes(f.read(4), byteorder="big") for i in range(magic[3])] # Reads data arrays size 4 bytes each. Array size is defined by files magic number
            numOfImg, rows, columns = arrays[0], arrays[1], arrays[2] # Just a transfer to more human readable variables
            print("\nWorking on a file %s processing %d images. Please wait..." % (filename, numOfImg))
            pic_array = np.fromstring(f.read(numOfImg * rows * columns), np.dtype(('uint8', 1)))    # example reads 60,000 x 28 x 28 pixels at once
            return pic_array.reshape(numOfImg, rows, columns)        # return converted 1D array into 3D array of pixels


def show_picture(image): # Prints out image to console
    for column, col in enumerate(image): # enumerable used instead od range(len(image))
        for pixel, pix in enumerate(col):
            # print(image[column][pixel]) # Prints out the raw byte values of pixels as an image
            if image[column][pixel] > 128: # Replaces pixel colors dark for '#' bright for '.'
                print("#", end='')
            else:
                print(".", end='')
        print("", end='\n')


def save_img(title): # Save images starting with name. Create filename with picture number and digit it represents
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
        print("\rImage %s saved" % out_filename, end='')


dirFiles = get_gz_files(src_dir) # gets all the *.gz files from directory Data.
# dirFiles = {'t10k-labels': 't10k-labels-idx1-ubyte.gz', 't10k-images': 't10k-images-idx3-ubyte.gz'} # dev ONLY

for file in dirFiles:
    startTime = datetime.datetime.now() # File process stopwatch start
    if "labels" in file:
        labels[file[:file.index("-")]] = read_file(src_dir + dirFiles[file]) # Directory(labels) [file name] -> array of labels
    elif "images" in file:
        data[file[:file.index("-")]] = read_file(src_dir + dirFiles[file]) # Directory(data) [file name] -> 3D array of pixels
    stopTime = datetime.datetime.now() # File process stopwatch stop
    print("File %s took %.10s to process" % (dirFiles[file], stopTime - startTime))

for name in data:   #loops all the arrays with data from files and save them to disk
    save_img(name)

show_picture(data["t10k"][9999]) # Displays picture on console Test 
print(labels["t10k"][9999]) # Displays associated label
