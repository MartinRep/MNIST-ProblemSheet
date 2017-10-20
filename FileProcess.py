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
src_dir = "data/"


def get_gz_files(loc_directory):
    # List all the files in directory
    files = dict()
    for filename in os.listdir(loc_directory):
        # adds only Gzip files to the list
        if ".gz" in filename:
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
            print("\nRead %d labels from %s" % (len(cur_labels), filename))
            return cur_labels
        # image file with data
        else:
            arrays = [int.from_bytes(f.read(4), byteorder="big") for i in range(magic[3])]
            numOfImg, rows, columns = arrays[0], arrays[1], arrays[2]
            # creates file structure. Sizes of array are dynamically created from file structure
            file_data = np.zeros((numOfImg, rows, columns))
            print("\nWorking on a file %s processing %d images. Please wait..." % (filename, numOfImg))
            # reads bytes as a whole picture array instead of individual pixels. Much faster!!!
            pic_array = np.fromstring(f.read(numOfImg * rows * columns), np.dtype(('uint8', 1)))    # reads 28 * 28 pixels at once
            pic_array = pic_array.reshape(numOfImg, rows, columns)        # converts 1D array into 3D array of pixels
            file_data = pic_array.tolist()
            return file_data


# Prints out image to console
def show_picture(image):
    for column, col in enumerate(image):
        for pixel, pix in enumerate(col):
            # print(image[column][pixel])
            # Replaces pixel colors dark for '#' bright for '.'
            if image[column][pixel] > 128:
                print("#", end='')
            else:
                print(".", end='')
        print("", end='\n')


# Save images starting with name. Create filename with picture number and digit they representing
# example train-XXXXX-Y.png train=name,X=index,Y=digit picture represents
def save_img(title):
    index = 0
    for image in data[title]:
        cur_img = np.array(image)
        cur_img = pil.fromarray(cur_img).convert('RGB')
        # formats filename to include zeros
        out_filename = '-{:06.0f}-'.format(index)
        out_dir = src_dir + title + "/"
        # combines name with index and digit with extension
        out_filename = out_dir + title + out_filename + str(labels[title][index]) + ".png"
        # dir is not keyword
        try:
            os.makedirs(out_dir)
        except OSError:
            pass
        # let exception propagate
        # Saves the file
        cur_img.save(out_filename)
        index = index + 1
        print("\rImage %s saved" % out_filename, end='')


# gets all the *.gz files from directory Data.
dirFiles = get_gz_files(src_dir)

# dev
# dirFiles = {'t10k-labels': 't10k-labels-idx1-ubyte.gz', 't10k-images': 't10k-images-idx3-ubyte.gz'}

for file in dirFiles:
    # File process stopwatch start
    startTime = datetime.datetime.now()
    if "labels" in file:
        # Directory(labels) [file name] -> array of labels
        labels[file[:file.index("-")]] = read_file(src_dir + dirFiles[file])
    elif "images" in file:
        # Directory(data) [file name] -> 3 D array of pixels
        data[file[:file.index("-")]] = read_file(src_dir + dirFiles[file])
    # File process stopwatch stop
    stopTime = datetime.datetime.now()
    print("File %s took %.10s to process" % (dirFiles[file], stopTime - startTime))

#loops all the arrays with data from files and save them to disk
for name in data:
    save_img(name)

# Test
img = data["t10k"][9999]
show_picture(img)
print(labels["t10k"][9999])
