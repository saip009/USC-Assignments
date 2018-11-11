import numpy as np


class KMeans():

    '''
        Class KMeans:
        Attr:
            n_cluster - Number of cluster for kmeans clustering (Int)
            max_iter - maximum updates for kmeans clustering (Int) 
            e - error tolerance (Float)
    '''

    def __init__(self, n_cluster, max_iter=100, e=0.0001):
        self.n_cluster = n_cluster
        self.max_iter = max_iter
        self.e = e

    def fit(self, x):
        '''
            Finds n_cluster in the data x
            params:
                x - N X D numpy array
            returns:
                A tuple
                (centroids a n_cluster X D numpy array, y a size (N,) numpy array where cell i is the ith sample's assigned cluster, number_of_updates an Int)
            Note: Number of iterations is the number of time you update the assignment
        '''
        assert len(x.shape) == 2, "fit function takes 2-D numpy arrays as input"
        np.random.seed(42)
        N, D = x.shape

        # TODO:
        # - comment/remove the exception.
        # - Initialize means by picking self.n_cluster from N data points
        # - Update means and membership until convergence or until you have made self.max_iter updates.
        # - return (means, membership, number_of_updates)

        # DONOT CHANGE CODE ABOVE THIS LINE

        # 3, Init
        m = x[np.random.choice(N, self.n_cluster, replace=False), :]
        # m = [np.random.permutation(x)[:2]]
        # print(m)
        # print(m.shape, x.shape, self.n_cluster)
        r = np.zeros(N)
        j = 10000000000  # large number

        # 4 repeat
        for it in range(0, self.max_iter):

            # 5 membership
            dist = ((m - np.expand_dims(x, axis=1)) ** 2)
            dist_mat = np.sum(dist, axis=2)
            # print(dist_mat.shape, mu.shape, x.shape, temp42002.shape)
            r = np.argmin(dist_mat, axis=1)
            # print(r.shape)

            # 6 j_new
            j_new = 0
            for ik in range(0, self.n_cluster):
                j_new += np.sum((x[ik == r] - m[ik]) ** 2)
            j_new /= N
            # print(J_new)

            # 7 break
            if abs(j - j_new) <= 2 * self.e:
                break

            # 9 j updaet
            j = j_new

            # 10 m update
            m = np.array([np.mean(x[r == k], axis=0) for k in range(self.n_cluster)])

        return (m, r, it)

        # raise Exception(
        #     'Implement fit function in KMeans class (filename: kmeans.py)')

        # DONOT CHANGE CODE BELOW THIS LINE

class KMeansClassifier():

    '''
        Class KMeansClassifier:
        Attr:
            n_cluster - Number of cluster for kmeans clustering (Int)
            max_iter - maximum updates for kmeans clustering (Int) 
            e - error tolerance (Float) 
    '''

    def __init__(self, n_cluster, max_iter=100, e=1e-6):
        self.n_cluster = n_cluster
        self.max_iter = max_iter
        self.e = e

    def fit(self, x, y):
        '''
            Train the classifier
            params:
                x - N X D size  numpy array
                y - (N,) size numpy array of labels
            returns:
                None
            Stores following attributes:
                self.centroids : centroids obtained by kmeans clustering (n_cluster X D numpy array)
                self.centroid_labels : labels of each centroid obtained by 
                    majority voting ((N,) numpy array) 
        '''

        assert len(x.shape) == 2, "x should be a 2-D numpy array"
        assert len(y.shape) == 1, "y should be a 1-D numpy array"
        assert y.shape[0] == x.shape[0], "y and x should have same rows"

        np.random.seed(42)
        N, D = x.shape
        # TODO:
        # - comment/remove the exception.
        # - Implement the classifier
        # - assign means to centroids
        # - assign labels to centroid_labels

        # DONOT CHANGE CODE ABOVE THIS LINE
        # raise Exception(
        #     'Implement fit function in KMeansClassifier class (filename: kmeans.py)')

        # 2 run k means
        k_means = KMeans(n_cluster=self.n_cluster, max_iter=self.max_iter, e=self.e)
        centroids, membership, it = k_means.fit(x)

        for k in range(0, self.n_cluster):
            yk = y[k == membership]
            # print(y.shape, yk.shape)

        # Vote
        votes = [[0] * 10 for _ in range(self.n_cluster)]
        for y_i, r_i in zip(y, membership):
            votes[r_i][y_i] += 1

        centroid_labels = np.array([v.index(max(v)) for v in votes])

        # DONOT CHANGE CODE BELOW THIS LINE

        self.centroid_labels = centroid_labels
        self.centroids = centroids

        assert self.centroid_labels.shape == (self.n_cluster,), 'centroid_labels should be a numpy array of shape ({},)'.format(
            self.n_cluster)

        assert self.centroids.shape == (self.n_cluster, D), 'centroid should be a numpy array of shape {} X {}'.format(
            self.n_cluster, D)

    def predict(self, x):
        '''
            Predict function

            params:
                x - N X D size  numpy array
            returns:
                predicted labels - numpy array of size (N,)
        '''

        assert len(x.shape) == 2, "x should be a 2-D numpy array"

        np.random.seed(42)
        N, D = x.shape
        # TODO:
        # - comment/remove the exception.
        # - Implement the prediction algorithm
        # - return labels

        # DONOT CHANGE CODE ABOVE THIS LINE
        # raise Exception(
        #     'Implement predict function in KMeansClassifier class (filename: kmeans.py)')

        dist = ((self.centroids - np.expand_dims(x, axis=1)) ** 2)
        dist_mat = np.sum(dist, axis=2)
        r = np.argmin(dist_mat, axis=1)
        labels = self.centroid_labels[r]

        # DONOT CHANGE CODE BELOW THIS LINE
        return labels

