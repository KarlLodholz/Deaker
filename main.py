import cv2 as cv
from scipy.signal import find_peaks
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import sys

def generate_color_gradient(dark_hsv, light_hsv, direction):
    # Create an array for storing the colors
    debuggin = False
    colors = []

    hue_dist = 0
    if dark_hsv[0] > light_hsv[0] and direction == 1:
        hue_dist = 180-dark_hsv[0] + light_hsv[0]
    elif dark_hsv[0] < light_hsv[0] and direction == -1:
        hue_dist = 180-light_hsv[0] + dark_hsv[0]
    else:
        hue_dist = abs(light_hsv[0] - dark_hsv[0])
        
        
    # Calculate the hue increment based on the direction
    hue_increment = hue_dist / 256.0 * direction
    
    # Calculate the saturation and value parameters for the circle equation
    t = np.linspace(0, 1, 256)
    saturation = np.sqrt(1-t)
    value = np.sqrt(t)

    # Generate the colors using HSV representation
    for i in range(256):
        hue = (dark_hsv[0] + (i * hue_increment) + 180) % 180
        hsv = np.uint8([[[round(hue), saturation[i] * 256, value[i] * 256]]])
        color = cv.cvtColor(hsv, cv.COLOR_HSV2RGB)
        if debuggin:
            print(str(i)+": "+str(color))
        colors.append(color)
    
    if debuggin:
        img = np.zeros((256,256,3), np.uint8)
        for y in range(256):
            for x in range(256):
                img[y][x] = colors[x]
        cv.imshow("gradient",img)
        cv.waitKey(0)
    
    return colors

def intensity_map(img):
    # make black and white
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    # get width and height and depth
    h, w = img.shape
    # f count for the img
    int_cnt = np.array([0]*256)
    for y in range(h):
        for x in range(w):
            int_cnt[img[y,x]] += 1
    return int_cnt


def edit(src, palette, int_cnt, num_clr):
    dst = deepcopy(src)
    if(num_clr > 1):
        img = deepcopy(src)
        # make black and white
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        # get width and height and depth
        h, w = img.shape
        # find the highest values in the int_cnt
        peaks, _ = find_peaks(int_cnt, height=0)
        # get largest peaks and sort them
        if(len(peaks) < num_clr):
            num_clr = len(peaks)
            print("color max:"+str(num_clr))
        srt_idx = np.argsort(_['peak_heights'])
        print(srt_idx)
        temp = srt_idx[-num_clr : ]
        print(temp)
        srt_int = [None]*num_clr
        for i in range(num_clr):
            srt_int[i] = peaks[temp[i]]
        srt_int = np.sort(srt_int)
        
        # calculate ranges of intensities
        # init intensity ranges
        rng = []
        for i in range(num_clr-1):
            rng.append((srt_int[i] + srt_int[i+1]) / 2)
        rng.append(255)

        # increase contrast by normalizing
        int_fill = deepcopy(srt_int)
        div = 255/(srt_int[num_clr-1]-srt_int[0])
        for i in range(num_clr):
            int_fill[i] = (int_fill[i] - srt_int[0]) * div
        # print(int_fill)
        
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
                # print(img[y,x])
                dst[y,x] = palette[fill_int_ref[img[y,x]]]

    return cv.cvtColor(dst, cv.COLOR_RGB2BGR)

if __name__ == "__main__":
    # get file name from arguement
    file_str = sys.argv[1]
    strt = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    end = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    num_pics = end-strt+1
    n_col = int(num_pics/2+.5)
    n_row = int(num_pics/n_col+.5)
    fig, ax = plt.subplots(nrows=n_row, ncols=n_col, squeeze=False, figsize=(20, 10))
    fig.tight_layout()

    orig = cv.imread(file_str)
    pic = deepcopy(orig)
    
    #apply a blur
    prims = [5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    # pic = cv.GaussianBlur(pic, (prims[5], prims[5]), 0)
    pic = cv.GaussianBlur(pic, (97, 97), 0)
    # orig = remove_background(orig)
    
    pics = []
    i = 0
    int_cnt = intensity_map(pic)
    # gradient = generate_color_gradient([0,255,255],[180,255,255],1)
    gradient = generate_color_gradient([160,255,0],[90,0,255],-1) #purple(black) and yellow(white)
    # gradient = generate_color_gradient([100,0,255],[30,255,0],1)
            
    for y in range(n_row):
        for x in range(n_col):
            if i < num_pics:
                pics.append(edit(pic, gradient, int_cnt, strt+i*2))
                # pics.append(edit(cv.GaussianBlur(pic, (prims[strt+i*4], prims[strt+i*4]), 0), gradient, int_cnt, 41))
                print(i)
                ax[y][x].imshow(pics[i])
                ax[y][x].set_title(strt+i*2)
                i+=1
            ax[y][x].axis('off')
    plt.show()
