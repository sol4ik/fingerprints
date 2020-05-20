import numpy as np
from collections import OrderedDict

from ..finger_error.finger_error import FingerError


class PCAnalyzer:
    def __init__(self, n, p, data):
        """
        :param n: number of observations / data matrix rows / column size
        :param p: number of characteristics / data matrix columns / row size
        :param data: the data matrix of size n x p
        """
        self.__calculated = False
        self.n = n
        self.p = p
        self.k = p - int(2 * p / 3 + 1)  # data dimension to reduce to

        self.data = data
        self.__centered_data = data

        self.__sigma = None  # covariance matrix
        self.__eigen = OrderedDict()

        self.k_basis = None
        self.to_k_basis = None

    def calculate(self):
        self.__center_data()
        self.__covariance_matrix()
        self.__principal_components()

        # construct change of basis matrix
        self.k_basis = list()
        for evc in self.__eigen.values():
            self.k_basis.append(list(evc))
        self.k_basis = np.array(self.k_basis)

        # transition matrix to a new basis - first k principal components
        self.to_k_basis = np.linalg.pinv(self.k_basis)

        self.__calculated = True

    def change_basis(self, vector):
        """
        After calculating the principal components of our dataset we want to
        express all the data within new reduced basis.
        :param vector: vector to expressed within new basis
        """
        if not self.__calculated:
            raise FingerError("no principal components calculated")
        if len(vector) != self.p:
            raise FingerError("invalid data dimension")
        return self.to_k_basis.dot(vector)

    def change_basis_all(self):
        """
        Express all the data from input data matrix within new basis consisting of
        k principal components.
        """
        to_return = list()
        for v in self.data:
            to_return.append(self.change_basis(v))
        return to_return


    def __center_data(self):
        """
        PCA starts off by assuming that our data are spread with zero mean,
        which means that we need to center them.
        """
        print("...center data")
        data_center = np.array(self.data).mean(axis=1)
        data_center = np.array([[el for _ in range(self.p)] for el in data_center])
        self.__centered_data = np.array(self.data) - data_center

    def __covariance_matrix(self):
        print("...covariance matrix")
        c = np.array(self.__centered_data)
        c_t = c.transpose()
        self.__sigma = c_t.dot(c)

    def __principal_components(self):
        print("...principal components")
        # eigenvalues and eigenvectors of covariance matrix
        evs, evcs = np.linalg.eig(self.__sigma)

        # since cv matrix is symmetric and we have exactly p eigenvalues
        for i in range(self.p):
            self.__eigen[evs[i]] = evcs[i]

        evs.sort()
        to_del = evs[::-1][:self.k + 1]

        # for key in to_del:
        #     del self.__eigen[key]
