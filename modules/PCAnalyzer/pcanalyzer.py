import numpy as np


class PCAnalyzer:
    def __init__(self, n, p, data):
        """
        :param n: number of observations / data matrix rows / column size
        :param p: number of characteristics / data matrix columns / row size
        :param data: the data matrix of size n x p
        """
        self.n = n
        self.p = p
        self.data = data
        self.__centered_data = data

    def apply(self):
        self.__center_data()
        self.__covariance_matrix()

    def __center_data(self):
        """
        PCA starts off by assuming that our data are spread with zero mean,
        which means that we need to center them.
        """

        data_center = np.array(self.data).transpose().mean(axis=1)
        data_center = np.array([[el for _ in range(self.p)] for el in data_center])
        self.__centered_data = (np.array(self.data).transpose() - data_center).transpose()

        # data_center = [0 for _ in range(self.p)]
        # for i in range(self.p):
        #     cur_avg = 0
        #     for j in range(self.n):
        #         cur_avg += self.data[j][i]
        #     cur_avg /= self.n
        #     data_center[i] = cur_avg
        #
        # for i in range(self.p):
        #     for j in range(self.n):
        #         self.__centered_data[j][i] -= data_center[i]

    def __covariance_matrix(self):
        c = np.array(self.__centered_data)
        c_t = c.transpose()
        self.__cov_matrix = c_t.dot(c)

    def __principal_components(self):
        pass
