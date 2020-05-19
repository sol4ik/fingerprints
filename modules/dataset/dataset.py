import os

from ..finger import Finger
from ..PCAnalyzer import PCAnalyzer

class Dataset:
    def __init__(self, dir="training_data"):
        self.dir = dir

        self.data = list()
        self.data_matrix = None
        self.pca = None

    def load_data(self):
        """
        Load all the images from data directory
        """
        for subdir in os.walk(self.dir):
            self.data.append(Finger(subdir[0]))
            self.data[-1].load_images()

    def data_to_matrix(self):
        pass

    def pca_calculate(self):
        """
        Create PCAnalyzer object. Calculate principal components for data.
        """
        self.pca = PCAnalyzer(self.data_matrix)
        self.pca.calculate()

    def to_pca_basis(self):
        self.pca.change_basis_all()

d = Dataset("../../data")
d.load_data()
