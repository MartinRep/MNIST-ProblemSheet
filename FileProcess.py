# Adapted from https://stackoverflow.com/questions/120656/directory-listing-in-python#120701
#              https://stackoverflow.com/questions/8703496/hash-map-in-python#8703509
import os
import gzip
#import PIL.Image as pil

def getFiles(directory):
    #List all the files in directory
    files = dict()
    for filename in os.listdir(directory):
        #adds only Gzip files to the list
        if(filename.find(".gz")):
            #Directory (hashmap) key = filename up to second "-", Value = filename
            files[filename[:filename.index("-",filename.index("-")+1)]] = filename
    return files

def read_labels_from_file(filename):
    with gzip.open(filename,'rb') as f:
        magic = f.read(4)
        print(magic)
        # magicNum = int(magic)
        # print(magicNum)
        magicNum = int.from_bytes(magic, byteorder='big')
        print(magicNum)
        
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
files = getFiles('data/')
for file in files:
    print(files[file])

#img = train_images[4999]
#img = np.array(img)
#img = pil.fromarray(img)
#img = convert('RGB')
#img.show
#img.save('2.png')