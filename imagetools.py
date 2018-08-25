import os
import imageio

def readLabels(path = "."):
    return [file for file in os.listdir(path) if file[-4:] == ".jpg"]

def floatComp(x, y):
    return float(x[:-4]) > float(y[:-4])

def sortLabels(labels, asFloat = False):
    if asFloat:
        labels.sort(cmp = floatComp)
    else:
        labels.sort()

def readImages(path = ".", nth = 1):
    labels = readLabels(path)
    sortLabels(labels, asFloat = True)
    nthLabels = [labels[n * nth] for n in range(len(labels) / nth)]
    ret = []
    imageCount = len(nthLabels)
    for label, i in zip(nthLabels, range(imageCount)):
        print "read image {}/{} : {}".format(i + 1, imageCount, label)
        im = imageio.imread(path + "/" + label)
#        print im
        ret.append(im)
    return ret
    
def writeAnimation(outFile):
    print "writing file : {}".format(outFile)
    imageio.mimwrite(uri = outFile, ims = ims, fps = 24)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('imagePath', type=str, help = "path to read images")
    parser.add_argument('outFile', type=str, help = "filename for animation")
    parser.add_argument('--nth', type=int, default = 1, help = "process only every nth image")
    parameters = parser.parse_args()
    print parameters
    ims = readImages(parameters.imagePath, nth = parameters.nth)
    writeAnimation(parameters.outFile)
    exit(0)
    


#ims2 = ims[:]
#ims2.reverse()

#ims += ims2

#imageio.mimwrite(uri = "last.mp4", ims = ims, fps = 24)

