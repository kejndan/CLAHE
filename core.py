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

        self.center_points = np.zeros((self.nb_rects, self.nb_rects, 2))

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



        self.lookup_tables_rect[(y_start+self.y_rect_center, x_start+self.x_rect_center)] = new_dist

        self.numpy_control_points.append([y_start+self.y_rect_center, x_start+self.x_rect_center])
        # plt.show()


    def walking_by_central_point(self):
        for i, x_start in enumerate(range(0, self.width, self.width_rect)):
            for j, y_start in enumerate(range(0, self.height, self.height_rect)):
                if x_start+self.x_rect_center < self.width and y_start+self.y_rect_center < self.height:
                    self.get_dist_rect(x_start, y_start)
                    center_point = [y_start+self.y_rect_center, x_start+self.x_rect_center]
                    self.center_points[j, i] = [y_start+self.y_rect_center, x_start+self.x_rect_center]



        self.numpy_control_points = np.asarray(self.numpy_control_points)


    def get_nearest_control_points(self, point, nb_nearest_points, type_dist='abs'):
        control_points = np.abs(self.numpy_control_points - np.asarray(point)).sum(axis=1)

        control_points = np.argsort(control_points)[:nb_nearest_points]
        return  self.numpy_control_points[control_points]


    def matrix_values(self):
        matrix = np.zeros((self.height, self.width, 2))
        for i in range(self.height):
            for j in range(self.width):
                matrix[i, j] = [i,j]
        return matrix


    def fill_each_point(self):


        for i in range(-1,8):
            for j in range(-1,8):
                border = 0
                if i == -1 and j == -1:
                    top_left = np.array([0, 0])
                    border = 2
                elif i == -1:
                    top_left = np.array([self.center_points[j-1,0][0], 0]).astype(int)
                    border += 1
                elif j == -1:
                    top_left = np.array([0,self.center_points[0, i-1][1]]).astype(int)

                    border += 1
                else:
                    top_left = self.center_points[j,i].astype(int)

                    border += 0

                if i == 7 and j == 7:
                    bottom_right = np.array([self.height, self.width]).astype(int)

                    border = 2
                elif i == 7:
                    bottom_right = np.array([self.center_points[j+1,i][0],self.width]).astype(int)

                    border += 1
                elif j == 7:
                    bottom_right = np.array([self.height,self.center_points[j, i+1][1]]).astype(int)

                    border += 1
                else:
                    bottom_right = self.center_points[j+1,i+1].astype(int)

                    border += 0

                if border == 2:
                    zone = 'red'
                elif border == 1:
                    zone = 'green'
                else:
                    zone = 'blue'

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
                            self.img[y,x] = 127

                            x_ratio = np.array([(bottom_right[1]-x)/(bottom_right[1]-top_left[1]),
                                                (x-top_left[1])/(bottom_right[1]-top_left[1])])

                            if i == -1 or j == 7:
                                first_point = self.center_points[j,i].astype(int)
                            elif j == -1 or i == 7:
                                first_point = self.center_points[j,i].astype(int)


                            z = x_ratio[0]*self.lookup_tables_rect[tuple(bottom_left)]


                        elif zone == 'red':
                            self.img[y,x] = 255







    def show(self):
        plt.imshow(self.img, cmap='gray')
        plt.axis('off')
        plt.show()

