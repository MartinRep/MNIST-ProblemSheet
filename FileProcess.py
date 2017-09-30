# Adapted from https://stackoverflow.com/questions/120656/directory-listing-in-python#120701
#              https://stackoverflow.com/questions/8703496/hash-map-in-python#8703509
import os
import gzip
import numpy as np
#import PIL.Image as pil
directory = "data/"

def getGzFiles(directory):
    #List all the files in directory
    files = dict()
    for filename in os.listdir(directory):
        #adds only Gzip files to the list
        if(filename.find(".gz")):
            #Directory (hashmap) key = filename up to second "-", Value = filename
            files[filename[:filename.index("-", filename.index("-")+1)]] = filename
    return files

def readFile(filename):
    with gzip.open(filename,'rb') as f:
        magic = f.read(4)
        #Check for number of dimensions in a file, if 1 the file is considered LABEL file
        if(magic[3] == 1):
            #get size of the items array
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
            for image in range(arrays[0]):
                print("Working on a Image[%d]" % image)
                for row in range(arrays[1]):
                    data[image][row] = int.from_bytes(f.read(arrays[2]), byteorder="big")
            return data


dirFiles = getGzFiles(directory)
labels = {}
data = {}
for file in dirFiles:
    if "labels" in file:
        #Directory [file name] -> array of labels
        labels[file[:file.index("-")]] = readFile(directory + dirFiles[file])
    elif "images" in file:
        #Directory [file name] -> 3 dimentional array of pixels
        data[file[:file.index("-")]] = readFile(directory + dirFiles[file])

#img = train_images[4999]
#img = np.array(img)
#img = pil.fromarray(img)
#img = convert('RGB')
#img.show
#img.save('2.png')