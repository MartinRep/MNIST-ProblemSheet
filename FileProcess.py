# Adapted from https://stackoverflow.com/questions/120656/directory-listing-in-python#120701
#              https://stackoverflow.com/questions/8703496/hash-map-in-python#8703509
#              https://pyformat.info/
#              https://pyformat.info/
import os
import gzip
import numpy as np
import PIL.Image as pil
import datetime
import sys

labels = {}
data = {}
directory = "data/"


def get_gz_files(loc_directory):
    # List all the files in directory
    files = dict()
    for filename in os.listdir(loc_directory):
        # adds only Gzip files to the list
        if filename.find(".gz"):
            # Directory (hash-map) key = filename up to second "-", Value = filename
            files[filename[:filename.index("-", filename.index("-")+1)]] = filename
    return files


def read_file(filename):
    with gzip.open(filename, 'rb') as f:
        magic = f.read(4)
        # Check for number of dimensions in a file, if 1 the file is considered LABEL file
        if magic[3] == 1:
            cur_labels = []
            # get size of the items array
            items = int.from_bytes(f.read(4), byteorder="big")
            for label in range(items):
                cur_labels.append(int.from_bytes(f.read(1), byteorder="big"))
            print("Read %d labels from %s" % (len(cur_labels), filename))
            return cur_labels
        # image file with data
        else:
            arrays = [int.from_bytes(f.read(4), byteorder="big") for i in range(magic[3])]
            # creates file structure. Sizes of array are dynamically created from file structure
            file_data = np.zeros((arrays[0], arrays[1], arrays[2]))
            print("Working on a file %s processing %d images. Please wait..." % (filename, arrays[0]))
            for image in range(arrays[0]):
                sys.stdout.write("Images processed: %.0f   \r" % (image/arrays[0]/100))
                sys.stdout.flush()
                for row in range(arrays[1]):
                    for column in range(arrays[2]):
                        file_data[image][row][column] = int.from_bytes(f.read(1), byteorder="big")
            return file_data


# Prints out image to console
def show_picture(image):
    for column in range(len(image)):
        for pixel in range(len(image[0])):
            # print(image[column][pixel])
            # Replaces pixel colors dark for '#' bright for '.'
            if image[column][pixel] > 128:
                print("#", end='')
            else:
                print(".", end='')
        print("")


# Save images starting with name. Create filename with picture number and digit they representing
# example train-XXXXX-Y.png train=name,X=index,Y=digit picture represents
def save_img(title):
    index = 0
    for image in data[title]:
        cur_img = np.array(image)
        cur_img = pil.fromarray(cur_img).convert('RGB')
        # formats filename to include zeros
        out_filename = '-{:06.0f}-'.format(index)
        # combines name with index and digit with extension
        out_filename = directory + title + out_filename + str(labels[title][index]) + ".png"
        # Saves the file
        cur_img.save(out_filename)
        index = index + 1


dirFiles = get_gz_files(directory)
for file in dirFiles:
    # File process stopwatch start
    startTime = datetime.datetime.now()
    if "labels" in file:
        # Directory [file name] -> array of labels
        labels[file[:file.index("-")]] = read_file(directory + dirFiles[file])
    elif "images" in file:
        # Directory [file name] -> 3 dimenional array of pixels
        data[file[:file.index("-")]] = read_file(directory + dirFiles[file])
    # File process stopwatch stop
    stopTime = datetime.datetime.now()
    print("File %s took %.10s to process" % (dirFiles[file], stopTime - startTime))

# Test
img = data["t10k"][999]
show_picture(img)
print(labels["t10k"][999])
# loops all the arrays with data from files and save them to disk
for name in data:
    save_img(name)
