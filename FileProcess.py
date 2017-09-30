# Adapted from https://stackoverflow.com/questions/120656/directory-listing-in-python#120701
#              https://stackoverflow.com/questions/8703496/hash-map-in-python#8703509
import os
import gzip
import numpy as np
import PIL.Image as pil
import datetime


def get_gz_files(dir):
    # List all the files in directory
    files = dict()
    for filename in os.listdir(dir):
        # adds only Gzip files to the list
        if filename.find(".gz"):
            # Directory (hashmap) key = filename up to second "-", Value = filename
            files[filename[:filename.index("-", filename.index("-")+1)]] = filename
    return files


def read_file(filename):
    with gzip.open(filename,'rb') as f:
        magic = f.read(4)
        # Check for number of dimensions in a file, if 1 the file is considered LABEL file
        if magic[3] == 1:
            # get size of the items array
            items = int.from_bytes(f.read(4), byteorder="big")
            labels = []
            for label in range(items):
                labels.append(int.from_bytes(f.read(1), byteorder="big"))
            print("Read %d labels from %s" % (len(labels), filename))
            return labels
        # image file with data
        else:
            arrays = []
            arrays = [int.from_bytes(f.read(4), byteorder="big") for i in range(magic[3])]
            data = np.zeros((arrays[0], arrays[1], arrays[2]))
            if arrays[0] <= 10000:
                print("Working on a file %s processing %d images. Please wait..." % (filename, arrays[0]))
                for image in range(arrays[0]):
                    for row in range(arrays[1]):
                        for column in range(arrays[2]):
                            data[image][row][column] = int.from_bytes(f.read(1), byteorder="big")
            return data


def show_picture(image):
    for column in range(len(image)):
        for pixel in range(len(image[0])):
            if image[column][pixel] > 128:
                print("#", end='')
            else:
                print(".", end='')
                # print(image[column][pixel])
        print("")


directory = "data/"

dirFiles = get_gz_files(directory)
labels = {}
data = {}
for file in dirFiles:
    startTime = datetime.datetime.now()
    if "labels" in file:
        # Directory [file name] -> array of labels
        labels[file[:file.index("-")]] = read_file(directory + dirFiles[file])
    elif "images" in file:
        # Directory [file name] -> 3 dimenional array of pixels
        data[file[:file.index("-")]] = read_file(directory + dirFiles[file])
    stopTime = datetime.datetime.now()
    print("File %s took %.10s to process" % (dirFiles[file], stopTime - startTime))

# Test
img = data["t10k"][999]
show_picture(img)
# print(img)
# img = np.array(img)
# img = pil.fromarray(img).convert('RGB')
# img.show
# img.save('2.png')
