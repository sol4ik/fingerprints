import os
import numpy as np

from ..finger import Finger
from ..image import Image
from ..PCAnalyzer import PCAnalyzer

class Dataset:
    DELTA = 0.3
    def __init__(self, dir="sub1"):
        self.dir = "training_data/" + dir
        self.suggestion = dir

        self.data = list()
        self.data_matrix = None
        self.to_recognize = None
        self.pca = None

    def load_data(self):
        """
        Load all the images from data directory
        """
        for subdir in os.walk(self.dir):
            self.data.append(Finger(subdir[0]))
            self.data[-1].load_images()

    def add_new(self, path):
        self.to_recognize = Image(path)
        self.to_recognize.crop_image()

    def data_to_matrix(self):
        for finger in self.data:
            for img in finger.images:
                self.data_matrix.append(np.flatten(img.centered_im))
        self.data_matrix.append(np.flatten(self.to_recognize.centered_im))

    def pca_calculate(self):
        """
        Create PCAnalyzer object. Calculate principal components for data.
        """
        self.data_to_matrix()

        self.pca = PCAnalyzer(self.data_matrix)
        self.pca.calculate()

        self.to_pca_basis()

    def to_pca_basis(self):
        self.pca.change_basis_all()

    @staticmethod
    def dist(self, vect_1, vect_2):
        dist = 0
        for i in range(len(vect_1)):
            dist += (vect_1[i] - vect_2[i]) * 2
        dist = dist ** 0.5
        return dist

    def verify(self):
        for fingerprint in self.pca.

d = Dataset("../../data")
d.load_data()
