import os

from ..PCAnalyzer import PCAnalyzer

class Dataset:
    def __init__(self, dir="training_data"):
        self.dir = dir

        self.data_matrix = None
        self.pca = None

    def load_data(self):
        pass

    def pca_calculate(self):
        pass

    def to_pca_basis(self):
        pass
