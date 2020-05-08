from PIL import Image
import numpy as np


class ImageProcessor:
    def __init__(self, path, name):
        self.path = path

    def read_image(self):
        img = Image.open(self.path)
        ar = np.array(img)

        ar_1channel = list()
        i = -1
        for row in ar:
            ar_1channel.append(list())
            i += 1
            for pixel in row:
                ar_1channel[i].append([int(sum(pixel) / 3) for _ in range(3)])

        ar_1channel = np.array(ar_1channel)
        ar_1channel = ar_1channel.flatten()
