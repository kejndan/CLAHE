import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class CLAHE:
    def __init__(self, img):
        self.img = cv.cvtColor(cv.imread(img), cv.COLOR_BGR2GRAY)
        self.height, self.width = self.img.shape

        self.nb_rects = 8

    def divide_into_rect(self):
        self.height_rect = self.height // self.nb_rects
        self.width_rect = self.width // self.nb_rects



        self.y_rect_center = self.height_rect  // 2

        self.x_rect_center = self.width_rect // 2


    def get_dist_rect(self, x_start, y_start):
        histogram, bins = np.histogram(self.img[x_start:x_start+self.width,
                                       y_start:y_start+self.height], 256, [0,256])

        norm_histogram = histogram / histogram.sum()
        plt.bar(bins[:-1]/256, norm_histogram)

        dist = norm_histogram.cumsum()

        # plt.plot(dist)
        new_dist = (dist*255).astype(np.int32)

        for i in range(self.height):
            for j in range(self.width):
                self.img[i, j] = new_dist[self.img[i,j]]

        plt.show()





    def show(self):
        plt.imshow(self.img, cmap='gray')
        plt.axis('off')
        plt.show()

