import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


class CLAHE:
    def __init__(self, img):
        self.img = cv.cvtColor(cv.imread(img), cv.COLOR_BGR2GRAY)
        self.orig_min = self.img.min()
        self.orig_max = self.img.max()

        self.height, self.width = self.img.shape

        self.nb_rects = 8

        self.lookup_tables_rect = {}
        self.numpy_control_points = []

        self.center_points = np.zeros((self.nb_rects, self.nb_rects, 2))

        self.cliping_limit = 125

    def divide_into_rect(self):
        self.height_rect = self.height // self.nb_rects
        self.width_rect = self.width // self.nb_rects
        self.y_rect_center = self.height_rect // 2
        self.x_rect_center = self.width_rect // 2

    def get_dist_rect(self, x_start, y_start):
        histogram, bins = np.histogram(self.img[y_start:y_start+self.height_rect,
                                       x_start:x_start+self.width_rect], 256, [0, 256])
        histogram = self.cliping(histogram)
        norm_histogram = histogram / histogram.sum()
        plt.bar(bins[:-1], norm_histogram)
        dist = norm_histogram.cumsum()
        new_dist = (dist*255).astype(np.int32)
        self.lookup_tables_rect[(y_start+self.y_rect_center, x_start+self.x_rect_center)] = new_dist
        self.numpy_control_points.append([y_start+self.y_rect_center, x_start+self.x_rect_center])

    def walking_by_central_point(self):
        for i, x_start in enumerate(range(0, self.width, self.width_rect)):
            for j, y_start in enumerate(range(0, self.height, self.height_rect)):
                if x_start+self.x_rect_center < self.width and y_start+self.y_rect_center < self.height:
                    self.get_dist_rect(x_start, y_start)
                    self.center_points[j, i] = [y_start+self.y_rect_center, x_start+self.x_rect_center]

        self.numpy_control_points = np.asarray(self.numpy_control_points)

    def get_zone_n_points(self, i, j):

        if i != -1 and i != 7 and j != -1 and j != 7:
            top_left = self.center_points[j, i].astype(int)
            bottom_right = self.center_points[j + 1, i + 1].astype(int)
            zone = 'blue'
            result = [zone, top_left, bottom_right]
        elif i == -1 and j != 7 and j != -1:
            top_left = np.array([self.center_points[j, 0][0], 0]).astype(int)
            bottom_right = self.center_points[j + 1, i + 1].astype(int)

            first_point = self.center_points[j, 0].astype(int)
            second_point = self.center_points[j + 1, 0].astype(int)
            zone = 'green'
            result = [zone, top_left, bottom_right, first_point, second_point]
        elif j == -1 and i != -1 and i != 7:
            top_left = np.array([0, self.center_points[0, i][1]]).astype(int)
            bottom_right = self.center_points[j + 1, i + 1].astype(int)

            first_point = self.center_points[0, i].astype(int)
            second_point = self.center_points[0, i + 1].astype(int)
            zone = 'green'
            result = [zone, top_left, bottom_right, first_point, second_point]
        elif i == 7 and j != -1 and j != 7:
            top_left = self.center_points[j, i].astype(int)
            bottom_right = np.array([self.center_points[j + 1, i][0], self.width - 1]).astype(int)

            first_point = self.center_points[j, 7].astype(int)
            second_point = self.center_points[j + 1, 7].astype(int)
            zone = 'green'
            result = [zone, top_left, bottom_right, first_point, second_point]
        elif j == 7 and i != -1 and i != 7:
            top_left = self.center_points[j, i].astype(int)
            bottom_right = np.array([self.height - 1, self.center_points[j, i + 1][1]]).astype(int)

            first_point = self.center_points[7, i].astype(int)
            second_point = self.center_points[7, i + 1].astype(int)
            zone = 'green'
            result = [zone, top_left, bottom_right, first_point, second_point]
        elif i == -1 and j == -1:
            top_left = np.array([0, 0])
            bottom_right = self.center_points[j + 1, i + 1].astype(int)
            dot_point = self.center_points[0, 0].astype(int)
            zone = 'red'
            result = [zone, top_left, bottom_right, dot_point]
        elif i == -1 and j == 7:
            top_left = np.array([self.center_points[j, 0][0], 0]).astype(int)
            bottom_right = np.array([self.height - 1, self.center_points[j, i + 1][1]]).astype(int)

            dot_point = self.center_points[7, 0].astype(int)
            zone = 'red'
            result = [zone, top_left, bottom_right, dot_point]
        elif i == 7 and j == -1:
            top_left = np.array([0, self.center_points[0, i][1]]).astype(int)
            bottom_right = np.array([self.center_points[j + 1, i][0], self.width - 1]).astype(int)

            dot_point = self.center_points[0, 7].astype(int)
            zone = 'red'
            result = [zone, top_left, bottom_right, dot_point]
        elif i == 7 and j == 7:
            top_left = self.center_points[j, i].astype(int)
            bottom_right = np.array([self.height - 1, self.width - 1]).astype(int)
            dot_point = self.center_points[7, 7].astype(int)
            zone = 'red'
            result = [zone, top_left, bottom_right, dot_point]
        return result

    def fill_each_point(self):
        for i in range(-1,8):
            for j in range(-1,8):
                info = self.get_zone_n_points(i,j)
                zone, top_left, bottom_right = info[:3]

                for y in range(top_left[0], bottom_right[0]):
                    for x in range(top_left[1], bottom_right[1]):
                        if zone == 'blue':
                            top_right = np.array([top_left[0], bottom_right[1]])
                            bottom_left = np.array([bottom_right[0], top_left[1]])

                            x_ratio = np.array([(top_right[1]-x)/(top_right[1]-top_left[1]),
                                                (x-top_left[1])/(top_right[1]-top_left[1])])
                            y_ratio = np.array([(bottom_left[0]-y)/(bottom_left[0]-top_left[0]),
                                                (y-top_left[0])/(bottom_left[0]-top_left[0])])

                            r1 = x_ratio[0]*self.lookup_tables_rect[tuple(top_left)] + x_ratio[1]*self.lookup_tables_rect[tuple(top_right)]
                            r2 = x_ratio[0] * self.lookup_tables_rect[tuple(bottom_left)] + x_ratio[1] * \
                                 self.lookup_tables_rect[tuple(bottom_right)]

                            z = y_ratio[0]*r1 + y_ratio[1]*r2

                            self.img[y,x] = np.uint8(z[self.img[y,x]])


                        elif zone == 'green':
                            first_point, second_point = info[3:]
                            if i == -1 or i == 7:

                                ratio = np.array([(second_point[0] - y) / (second_point[0] - first_point[0]),
                                                  (y - first_point[0]) / (second_point[0] - first_point[0])])
                            elif j == -1 or j == 7:
                                ratio = np.array([(second_point[1] - x) / (second_point[1] - first_point[1]),
                                                  (x - first_point[1]) / (second_point[1] - first_point[1])])


                            z = ratio[0]*self.lookup_tables_rect[tuple(first_point)]+ratio[1]*self.lookup_tables_rect[tuple(second_point)]
                            self.img[y, x] = np.uint8(z[self.img[y, x]])


                        elif zone == 'red':
                            dot_point = info[3]
                            self.img[y,x] = np.uint8(self.lookup_tables_rect[tuple(dot_point)][self.img[y,x]])


    def cliping(self, histogram):
        r = len(histogram)
        top = self.cliping_limit
        bottom = 0
        while (top - bottom) > 1:
            middle = (top+bottom)/2
            s = histogram[np.where(histogram > self.cliping_limit)[0]].sum()
            if s > (self.cliping_limit - middle)*r:
                top = middle
            else:
                bottom = middle
        histogram = np.where(histogram < bottom, histogram + self.cliping_limit - bottom, self.cliping_limit)
        return histogram


    def show(self):
        plt.imshow(self.img, cmap='gray')
        plt.axis('off')
        plt.show()

