from skimage.io import imread, imshow
from scipy import ndimage
import matplotlib.pylab as plt
import numpy as np
from math import sqrt, atan, cos, sin, ceil
from tqdm import tqdm
import png

class Image:
    def __init__(self, path):
        self.original = imread(path, as_gray=True) # type - numpy.ndarray size = 200x200
        self._window = 3
        self.radius = 150//2 # діаметр відповідно 148
        self._noramlization()
        # self.crop_image() # assigns to self.centered_im the value of centered image

    def _noramlization(self):
        desired_mean = 50  # according to the paper
        desired_variance = 50  # according to the paper
        self._normalized_im = np.zeros(self.original.shape)
        m, n = self.original.shape
        for i in range(m):
            for j in range(n):
                if self.original[i, j] > np.mean(self.original):
                    self._normalized_im[i, j] = desired_mean + sqrt(
                        desired_variance * ((self.original[i, j] - np.mean(self.original)) ** 2) / np.var(self.original, ddof=1))
                else:
                    self._normalized_im[i, j] = desired_mean - sqrt(
                        desired_variance * ((self.original[i, j] - np.mean(self.original)) ** 2) / np.var(self.original, ddof=1))

    class Block:

        def __init__(self, i, j, x_gradients, y_gradients, gaussian_filtered_image, window, im):
            center_x = i + window//2
            center_y = j + window // 2
            self.center_location = (center_x, center_y)

            def local_orientation(i, j):         # gradients direction 
                V_x = sum([2 * x_gradients[u, v] * y_gradients[u, v] for u in range(i, i + window)
                                 for v in range(j , j+ window)])

                V_y = sum( [ ((x_gradients[u, v])**2) * ((y_gradients[u, v])**2) for u in range(i, i + window)
                                  for v in range(j, j + window)] )
                if V_x == 0:
                    return 0
                return (1 / 2) * atan(V_y / V_x)

            pixels_orientation = np.zeros((window, window))
            for k in range(window):
                for l in range(window):
                    pixels_orientation[k, l] = local_orientation(i + k, j + l)

            self.diff_y = sum([sin(2 * pixels_orientation[k, window-1]) for k in range(window)]) - sum([
                sin(2 * pixels_orientation[k, 0]) for k in range(window)])

            self.diff_x = sum([cos(2 * pixels_orientation[window-1, l]) for l in range(window)]) - sum([
                cos(2 * pixels_orientation[0, l]) for l in range(window)])

    def __orientations(self):
        orients = []
        window = 25
        self._noramlization()

        mask = np.zeros((len(self._normalized_im) - window, len(self._normalized_im) - window)) # for visualization of detected core points

        grad_x = ndimage.sobel(self._normalized_im, axis=0, mode='constant')
        grad_y = ndimage.sobel(self._normalized_im, axis=1, mode='constant')
        gaussian_filtered_image = ndimage.gaussian_filter(self._normalized_im, sigma=1)


        for i in tqdm(range(0, len(self._normalized_im) - 2*window - 1, window)):
            for j in (range(0, len(self._normalized_im[0]) - 2*window - 1, window)):
                block = Image.Block(i,j,grad_x, grad_y, gaussian_filtered_image, window, self._normalized_im)
                if block.diff_y < 0 and block.diff_x < 0:
                    orients.append(block.center_location)
                    mask[i,j] = 1
        #  visualization of gradients and detected core points
        # plt.subplot(2, 2, 1), plt.imshow(self._normalized_im, cmap='gray')
        # plt.title('Original'), plt.xticks([]), plt.yticks([])
        # plt.subplot(2, 2, 2), plt.imshow(grad_x, cmap='gray')
        # plt.title('Grad_X'), plt.xticks([]), plt.yticks([])
        # plt.subplot(2, 2, 3), plt.imshow(grad_y, cmap='gray')
        # plt.title('Grad_Y'), plt.xticks([]), plt.yticks([])
        # plt.subplot(2, 2, 4), plt.imshow(mask, cmap='gray')
        # plt.title('MASK window = 25'), plt.xticks([]), plt.yticks([])
        # plt.show()
        return orients

    def __set_center(self):

        locals = self.__orientations()
        def most_frequent(List):
            return max(set(List), key=List.count)

        most_frequent_x = most_frequent([i[0] for i in locals])

        most_frequent_y = most_frequent([i[1] for i in locals])

        return (most_frequent_x, most_frequent_y)

    def crop_image(self):

        core_point = self.__set_center()

        max_x = 0
        max_y = 0

        if core_point[0] - self.radius < 0:
            min_x = 0
            max_x += abs(core_point[0] - self.radius)
        else:
            min_x = core_point[0] - self.radius

        if core_point[0] + self.radius > self.original.shape[0]:
            max_x = self.original.shape[0]
            min_x = min_x - abs(core_point[0] + self.radius - self.original.shape[0])
        else:
            max_x += core_point[0] + self.radius

        if core_point[1] - self.radius < 0:
            min_y = 0
            max_y += abs(core_point[1] - self.radius)
        else:
            min_y = core_point[1] - self.radius

        if core_point[1] + self.radius > self.original.shape[1]:
            max_y = self.original.shape[1]
            min_y -= (core_point[1] + self.radius) - self.original.shape[1]
        else:
            max_y += core_point[1] + self.radius

        self.centered_im = self._normalized_im[min_x: max_x, min_y : max_y]

    def save_img(self, path_to_save):
        to_image = np.array(self.centered_im).astype(np.uint8)
        png.from_array(to_image, 'L').save(path_to_save)


# EXAMPLE OF USAGE
im = Image("../../data/sub1/11.jpg")
# plt.subplot(2, 2, 1), plt.imshow(im._normalized_im, cmap='gray')
# plt.title('Original test0 150 freq'), plt.xticks([]), plt.yticks([])
# plt.subplot(2, 2, 2), plt.imshow(im.centered_im, cmap='gray')
# plt.title('centered test0 150 freq'), plt.xticks([]), plt.yticks([])
# im.save_img()

# im2 = Image("test2.jpg")
# plt.subplot(2, 2, 3), plt.imshow(im2._normalized_im, cmap='gray')
# plt.title('Original test2 150 freq'), plt.xticks([]), plt.yticks([])
# plt.subplot(2, 2, 4), plt.imshow(im2.centered_im, cmap='gray')
# plt.title('centered test2 150 freq'), plt.xticks([]), plt.yticks([])
#
# plt.show()
#
#
# im3 = Image("test_294.jpg")
# plt.subplot(2, 2, 1), plt.imshow(im3._normalized_im, cmap='gray')
# plt.title('Original test0 150 freq'), plt.xticks([]), plt.yticks([])
# plt.subplot(2, 2, 2), plt.imshow(im3.centered_im, cmap='gray')
# plt.title('centered test0 150 freq'), plt.xticks([]), plt.yticks([])
#
# im4 = Image("test_504.jpg")
# plt.subplot(2, 2, 3), plt.imshow(im4._normalized_im, cmap='gray')
# plt.title('Original test2 150 freq'), plt.xticks([]), plt.yticks([])
# plt.subplot(2, 2, 4), plt.imshow(im4.centered_im, cmap='gray')
# plt.title('centered test2 150 freq'), plt.xticks([]), plt.yticks([])
#
# plt.show()