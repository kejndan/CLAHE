import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class CLAHE:
    def __init__(self, img):
        self.img = cv.cvtColor(cv.imread(img), cv.COLOR_BGR2GRAY)
        self.height, self.width = self.img.shape

        self.nb_rects = 8

        self.lookup_tables_rect = {}
        self.numpy_control_points = []

    def divide_into_rect(self):
        self.height_rect = self.height // self.nb_rects
        self.width_rect = self.width // self.nb_rects



        self.y_rect_center = self.height_rect  // 2

        self.x_rect_center = self.width_rect // 2



    def get_dist_rect(self, x_start, y_start):
        histogram, bins = np.histogram(self.img[y_start:y_start+self.height_rect,
                                       x_start:x_start+self.width_rect], 256, [0, 256])

        norm_histogram = histogram / histogram.sum()
        plt.bar(bins[:-1], norm_histogram)

        dist = norm_histogram.cumsum()

        # plt.plot(dist)
        new_dist = (dist*255).astype(np.int32)

        self.lookup_tables_rect[(y_start+self.y_rect_center, x_start+self.x_rect_center)] = new_dist[self.img[y_start+self.y_rect_center, x_start+self.x_rect_center]]

        self.numpy_control_points.append([y_start+self.y_rect_center, x_start+self.x_rect_center])
        # plt.show()


    def walking_by_central_point(self):
        for x_start in range(0, self.width, self.width_rect):
            for y_start in range(0, self.height, self.height_rect):
                if x_start+self.x_rect_center < self.width and y_start+self.y_rect_center < self.height:
                    self.get_dist_rect(x_start, y_start)
        self.numpy_control_points = np.asarray(self.numpy_control_points)


    def get_nearest_control_points(self, point, nb_nearest_points, type_dist='abs'):
        control_points = np.abs(self.numpy_control_points - np.asarray(point)).sum(axis=1)

        control_points = np.argsort(control_points)[:nb_nearest_points]










    def show(self):
        plt.imshow(self.img, cmap='gray')
        plt.axis('off')
        plt.show()

