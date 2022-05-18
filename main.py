import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys

# img = cv.imread('goku.jpeg')
# gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# fig, ax = plt.subplots(1, 2, figsize=(16, 8))
# fig.tight_layout()

# ax[0].imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
# ax[0].set_title("Original")

# ax[1].imshow(cv.cvtColor(gray_image, cv.COLOR_BGR2RGB))
# ax[1].set_title("Grayscale")
# plt.show()

if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")
    
    # get file name from arguement
    sys.argv[1]