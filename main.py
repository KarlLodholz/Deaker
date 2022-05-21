import cv2 as cv
from scipy.signal import find_peaks
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import sys
# import time

def intensity_map(img):
    # make black and white
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # get width and height and depth
    h, w = img.shape
    # intensity count for the img
    int_cnt = np.array([0]*256)
    for y in range(h):
        for x in range(w):
            int_cnt[img[y,x]] += 1
    return int_cnt


def edit(img, int_cnt, num_clr):
    if(num_clr > 1):
        # make black and white
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # get width and height and depth
        h, w = img.shape
        # find the highest values in the int_cnt
        peaks, _ = find_peaks(int_cnt, height=0)
        # get largest peaks and sort them
        if(len(peaks) < num_clr):
            num_clr = len(peaks)
            print("color max:"+str(num_clr))
        srt_idx = np.argsort(_['peak_heights'])
        temp = srt_idx[-num_clr : ]
        srt_int = [None]*num_clr
        for i in range(num_clr):
            srt_int[i] = peaks[temp[i]]
        srt_int = np.sort(srt_int)

        # calculate ranges of intensities
        # init intensity ranges
        rng = []
        for i in range(num_clr-1):
            rng.append((srt_int[i] + srt_int[i+1]) / 2)
        rng.append(256)
        
        # increase contrast
        int_fill = deepcopy(srt_int)
        div = 255/(srt_int[num_clr-1]-srt_int[0])
        for i in range(num_clr):
            int_fill[i] = (int_fill[i] - srt_int[0]) * div
        
        # create fill table
        fill_int_ref = []
        cntr = 0
        for i in range(256):
            if(i > rng[cntr]):
                cntr += 1
            fill_int_ref.append(int_fill[cntr])
        
        #edit the img
        for y in range(h):
            for x in range(w):
                img[y,x] = fill_int_ref[img[y,x]]
    return img

if __name__ == "__main__":
    # get file name from arguement
    file_str = sys.argv[1]
    strt = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    num_pics = end-strt+1
    n_col = int(num_pics/2+.5)
    n_row = int(num_pics/n_col+.5)
    fig, ax = plt.subplots(nrows=n_row, ncols=n_col, squeeze=False, figsize=(16, 8))
    fig.tight_layout()

    orig = cv.imread(file_str)
    pics = []
    i = 0
    int_cnt = intensity_map(orig)
    for y in range(n_row):
        for x in range(n_col):
            if i < num_pics:
                pics.append(edit(orig, int_cnt, strt+i))
                ax[y][x].imshow(cv.cvtColor(pics[i], cv.COLOR_BGR2RGB))
                ax[y][x].set_title(i+strt)
                print(i+strt)
                i+=1
            ax[y][x].axis('off')
    plt.show()
