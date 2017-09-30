# Adapted from https://stackoverflow.com/questions/120656/directory-listing-in-python#120701
#              https://stackoverflow.com/questions/8703496/hash-map-in-python#8703509
import os
import gzip
#import PIL.Image as pil
directory = "data"

def getGzFiles(directory):
    #List all the files in directory
    files = dict()
    for filename in os.listdir(directory):
        #adds only Gzip files to the list
        if(filename.find(".gz")):
            #Directory (hashmap) key = filename up to second "-", Value = filename
            files[filename[:filename.index("-", filename.index("-")+1)]] = filename
    return files

def readLabelFile(filename):
    with gzip.open(filename,'rb') as f:
        magic = f.read(4)
        dimensions = magic[3]
        #Check for number of dimensions in a file, if 1 the file is considered LABEL file
        if(dimensions == 1):
            #get size of the items array
            items = int.from_bytes(f.read(4), byteorder="big")
            labels = []
            for label in range(items):
                labels.append(int.from_bytes(f.read(1), byteorder="big"))
            print(labels)
            print(len(labels))

        # magicNum = int(magic)
        # print(magicNum)
        # magicNum = int.from_bytes(magic, byteorder='big')
        #print(magicNum)
        
        #print(int.from_bytes(f.read(4), byteorder='big'))
        #magic = f.read(4)
        #print(int(magic))
        #magic = int(f.read(4))
        #print(magic)
        #magic = int(magic)

        #nolab = int(f.read(4))
        #nolab = int(nolab)
        #labels = [f.read(1) for i in range(nolab)]
        #labels = [int(label)for label in labels]
        return magic

#train_labels = read_labels_from_file('data/t10k-images-idx3-ubyte.gz')
files = getGzFiles(directory)
for file in files:
    if "labels" in file:
        readLabelFile(directory + "/" + files[file])

#img = train_images[4999]
#img = np.array(img)
#img = pil.fromarray(img)
#img = convert('RGB')
#img.show
#img.save('2.png')