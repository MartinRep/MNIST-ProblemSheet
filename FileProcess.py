import gzip
#import PIL.Image as pil
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
        return labels

train_labels = read_labels_from_file('data/t10k-images-idx3-ubyte.gz')

#img = train_images[4999]
#img = np.array(img)
#img = pil.fromarray(img)
#img = convert('RGB')
#img.show
#img.save('2.png')