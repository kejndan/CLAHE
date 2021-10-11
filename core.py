import cv2 as cv
import matplotlib.pyplot as plt


class CLAHE:
    def __init__(self, img):
        self.img = cv.cvtColor(cv.imread(img), cv.COLOR_BGR2GRAY)

    def show(self):
        plt.imshow(self.img, cmap='gray')
        plt.axis('off')
        plt.show()