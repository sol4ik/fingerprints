from skimage.io import imread, imshow
from scipy import ndimage
import matplotlib.pylab as plt
import numpy as np
from math import sqrt, atan, cos, sin, ceil
from tqdm import tqdm

class Image:
    def __init__(self, path):
        self.original = imread(path, as_gray=True) # type - numpy.ndarray size = 200x200
        # self.cropped = self.centered()
        self._normalized_im = None
        self._window = 3
        self._noramlization()

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

            def local_orientation(i, j):
                print("j :", j)
                V_x = sum([2 * x_gradients[u, v] * y_gradients[u, v] for u in range(i, i + window)
                                 for v in range(j , j+ window)])

                V_y = sum( [ ((x_gradients[u, v])**2) * ((y_gradients[u, v])**2) for u in range(i, i + window)
                                  for v in range(j, j + window)] )
                if V_x == 0:
                    return 0
                return (1 / 2) * atan(V_y / V_x)

            def continious_vector_field_y( i, j):
                return sin(2 * local_orientation(i, j))

            def continious_vector_field_x(i, j):
                if local_orientation(i, j) == 0:
                    return 0
                return cos(2 * local_orientation(i, j))

            def filered_vector_field_x(i, j):
                return sum([gaussian_filtered_image[u, v] * continious_vector_field_x(i,j) for
                            u in range(-window // 2, window// 2) for v in
                            range(-window // 2, window // 2)])

            def filered_vector_field_y(i, j):
                return sum([gaussian_filtered_image[u, v] * continious_vector_field_y(i, j) for
                            u in range(-window // 2, window // 2) for v in range(-window // 2, window// 2)])

            def smoothed_orientation_field(i, j):
                if filered_vector_field_x(i,j) == 0:
                    smoothed_orientation = 0
                else:
                    smoothed_orientation = 1/2*(atan(filered_vector_field_y(i,j)/filered_vector_field_x(i,j)) )
                return smoothed_orientation

            pixels_orientation = np.zeros((window, window))
            for k in range(window):
                for l in range(window):
                    pixels_orientation[k, l] = smoothed_orientation_field(i + k, j + l)

            # print("PIXELS orientation: ",pixels_orientation)

            self.diff_y = sum([sin(2 * pixels_orientation[k, window-1]) for k in range(window)]) - sum([
                sin(2 * pixels_orientation[k, 0]) for k in range(window)])

            # print("Diff y = ", self.diff_y)


            self.diff_x = sum([cos(2 * pixels_orientation[window-1, l]) for l in range(window)]) - sum([
                cos(2 * pixels_orientation[0, l]) for l in range(window)])

            # print("Diff x = ", self.diff_x)



    def orientations(self):

        orients = []
        window = 3
        mask = np.zeros((len(self._normalized_im) - window, len(self._normalized_im) - window))
        self._noramlization()

        grad_x = ndimage.sobel(self._normalized_im, axis=0, mode='constant')
        grad_y = ndimage.sobel(self._normalized_im, axis=1, mode='constant')
        gaussian_filtered_image = ndimage.gaussian_filter(self._normalized_im, sigma=1)

        for i in tqdm(range(0, len(self._normalized_im) - window, window)):
            for j in tqdm(range(0, len(self._normalized_im[0]) - window, window)):
                block = Image.Block(i,j,grad_x, grad_y, gaussian_filtered_image, window, self._normalized_im)
                # print("block.diff_y", block.diff_y, "block.diff_x", block.diff_x)
                if block.diff_y < 0 and block.diff_x < 0:
                    orients.append(block.center_location)
                    mask[i,j] = 1
                # elif block.diff_y != 0 and block.diff_x != 0:
                #     print("NOT null",block.center_location)
        plt.imshow(self._normalized_im, cmap=plt.cm.gray)
        plt.show()

        plt.imshow(mask, cmap=plt.cm.gray)
        plt.show()
        return orients



im = Image("test.jpg")
print("ORIENTATIONS")
print(im.orientations())
