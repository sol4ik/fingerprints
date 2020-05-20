import os
import numpy as np

from ..finger.finger import Finger
from ..image.image import Image
from ..PCAnalyzer.pcanalyzer import PCAnalyzer

class Dataset:
    DELTA = 0.3
    def __init__(self, dir="sub1"):
        self.dir = "training_data/" + dir
        self.suggestion = dir

        self.data = list()
        self.data_matrix = list()
        self.to_recognize = None
        self.pca = None

    def load_data(self):
        """
        Load all the images from data directory
        """
        for subdir in os.walk(self.dir):
            for img in os.listdir(subdir[0]):
                if os.path.isfile(img):
                    self.data.append(Image(self.dir + "/" + subdir + "/" + img))
            return

    def add_new(self, path):
        self.to_recognize = Image(path)
        self.to_recognize.crop_image()

    def data_to_matrix(self):
        for img in self.data:
            self.data_matrix.append(np.ndarray.flatten(img.original))

        self.data_matrix.append(np.ndarray.flatten(self.to_recognize.centered_im))

    def pca_calculate(self):
        """
        Create PCAnalyzer object. Calculate principal components for data.
        """
        self.data_to_matrix()

        self.pca = PCAnalyzer(len(self.data_matrix), 150 * 150, self.data_matrix)
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

    def norm(self, vect):
        norm = 0
        for v in vect:
            norm += v ** 2
        return norm ** 0.5

    def verify(self):
        print("...verifying")
        self.new_basis_data = list()
        for vect in self.data_matrix:
            self.new_basis_data.append(self.pca.change_basis(vect))

        distances = list()
        sum_dist = 0
        for vect in self.new_basis_data[:-1]:
            new_dist = self.dist(self.new_basis_data[-1], vect)
            distances.append(new_dist)
            sum_dist += new_dist
        avg_dist = sum_dist / len(distances)
        avg_dist /= self.norm(self.new_basis_data[-1])
        if abs(avg_dist - self.DELTA) > 0:
            return False
        return True

d = Dataset("../../data")
d.load_data()
