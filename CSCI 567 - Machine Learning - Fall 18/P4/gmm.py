import numpy as np
from kmeans import KMeans

class GMM():
    '''
        Fits a Gausian Mixture model to the data.

        attrs:
            n_cluster : Number of mixtures (Int)
            e : error tolerance (Float) 
            max_iter : maximum number of updates (Int)
            init : initialization of means and variance
                Can be 'random' or 'kmeans' 
            means : means of Gaussian mixtures (n_cluster X D numpy array)
            variances : variance of Gaussian mixtures (n_cluster X D X D numpy array) 
            pi_k : mixture probabilities of different component ((n_cluster,) size numpy array)
    '''

    def __init__(self, n_cluster, init='k_means', max_iter=100, e=0.0001):
        self.n_cluster = n_cluster
        self.e = e
        self.max_iter = max_iter
        self.init = init
        self.means = None
        self.variances = None
        self.pi_k = None

    def fit(self, x):
        '''
            Fits a GMM to x.

            x: is a NXD size numpy array
            updates:
                self.means
                self.variances
                self.pi_k
        '''
        assert len(x.shape) == 2, 'x can only be 2 dimensional'

        np.random.seed(42)
        N, D = x.shape

        if (self.init == 'k_means'):
            # TODO
            # - comment/remove the exception
            # - initialize means using k-means clustering
            # - compute variance and pi_k (see P4.pdf)

            # DONOT MODIFY CODE ABOVE THIS LINE
            # raise Exception(
            #     'Implement initialization of variances, means, pi_k using k-means')

            # initialize ooutpus
            k_means = KMeans(n_cluster=self.n_cluster, max_iter=self.max_iter, e=self.e)
            self.means, r, it = k_means.fit(x)
            gamma = np.identity(self.n_cluster)[r]

            # Initialize inputs
            nk = sum(gamma)
            self.variances = np.zeros((self.n_cluster, D, D))
            for k in range(self.n_cluster):
                self.variances[k] = np.dot((gamma[:, k]) * np.transpose(x - self.means[k]), (x - self.means[k])) / nk[k]
            self.pi_k = nk / N

            # DONOT MODIFY CODE BELOW THIS LINE

        elif (self.init == 'random'):
            # TODO
            # - comment/remove the exception
            # - initialize means randomly
            # - initialize variance to be identity and pi_k to be uniform

            # DONOT MODIFY CODE ABOVE THIS LINE
            # raise Exception(
            #     'Implement initialization of variances, means, pi_k randomly')

            # Initialize N, mu, Sigma, pi
            n = np.zeros(self.n_cluster)
            self.means = np.random.rand(self.n_cluster, D)
            # print(self.means.shape, self.means)
            self.variances = np.array([np.identity(D)] * self.n_cluster)
            self.pi_k = np.array([(1 / self.n_cluster) for x in range(self.n_cluster)])

            # DONOT MODIFY CODE BELOW THIS LINE

        else:
            raise Exception('Invalid initialization provided')

            # TODO
            # - comment/remove the exception
            # - Use EM to learn the means, variances, and pi_k and assign them to self
            # - Update until convergence or until you have made self.max_iter updates.
            # - Return the number of E/M-Steps executed (Int)
            # Hint: Try to separate E & M step for clarity
            # DONOT MODIFY CODE ABOVE THIS LINE
            # raise Exception('Implement fit function (filename: gmm.py)')

            # 4 l init
            # gamma_sum1 = np.sum(gamma, axis=1)
            # l = sum(np.log(gamma_sum1))
            l = 100000

            # 5 loop to max iter 12
            gamma = np.zeros((N, self.n_cluster))
            for it in range(0, self.max_iter):

                # 6 E step
                for k in range(self.n_cluster):
                    # sigma = np.copy(self.variances[k])
                    sigma = np.array([_ for _ in self.variances[k]])
                    # print(sigma.shape, type(sigma))
                    while not np.isfinite(np.linalg.cond(sigma)):
                        sigma += .001 * np.identity(D)
                    g_pdf = self.Gaussian_pdf(mean=self.means, variance=sigma)
                    f = np.exp(
                        -0.5 * np.sum(np.multiply(np.dot(x - self.means[k], np.linalg.inv(sigma)), x - self.means[k]),
                                      axis=1)) / np.sqrt(((2 * np.pi) ** D) * np.linalg.det(sigma))
                    gamma[:, k] = np.multiply(self.pi_k[k], f)

                gamma_sum1 = np.sum(gamma, axis=1)
                gamma = np.transpose(np.transpose(gamma) / gamma_sum1)
                gamma_sum0 = np.sum(gamma, axis=0)  # nk

                # 7 M step
                for k in range(self.n_cluster):
                    self.means[k] = np.transpose(np.sum(gamma[:, k] * np.transpose(np.transpose(x)).T, axis=1)) / \
                                    gamma_sum0[k]
                    x_del = x - self.means[k]
                    self.variances[k] = np.dot(gamma[:, k] * (np.transpose(x_del)), (x - self.means[k])) / gamma_sum0[k]
                self.pi_k = gamma_sum0 / N

                # 8 new log-likelihood
                l_new = sum(np.log(gamma_sum1))

                # 9 10
                if abs(l - l_new) <= self.e:
                    break

                # 11
                l = l_new

            return it

            # DONOT MODIFY CODE BELOW THIS LINE

		
    def sample(self, N):
        '''
        sample from the GMM model

        N is a positive integer
        return : NXD array of samples

        '''
        assert type(N) == int and N > 0, 'N should be a positive integer'
        np.random.seed(42)
        if (self.means is None):
            raise Exception('Train GMM before sampling')

        # TODO
        # - comment/remove the exception
        # - generate samples from the GMM
        # - return the samples

        # DONOT MODIFY CODE ABOVE THIS LINE
        # raise Exception('Implement sample function in gmm.py')

        D = self.means.shape[1]
        choice = np.random.choice(a=self.n_cluster, size=N, replace=True, p=self.pi_k)
        choice_len = len(choice)
        # print(sample_choice.shape)
        samples = np.zeros((N, self.means.shape[1]))
        # samples = np.random.multivariate_normal(self.means, self.variances)
        for i in range(0, len(choice)):
            mu = self.means[choice[i]]
            sigma = self.variances[choice[i]]
            samples[i] = np.random.multivariate_normal(mu, sigma)
        # print(samples.shape)

        # DONOT MODIFY CODE BELOW THIS LINE

        # DONOT MODIFY CODE ABOVE THIS LINE
        raise Exception('Implement sample function in gmm.py')
        # DONOT MODIFY CODE BELOW THIS LINE
        return samples        

    def compute_log_likelihood(self, x, means=None, variances=None, pi_k=None):
        '''
            Return log-likelihood for the data

            x is a NXD matrix
            return : a float number which is the log-likelihood of data
        '''
        assert len(x.shape) == 2,  'x can only be 2 dimensional'
        if means is None:
            means = self.means
        if variances is None:
            variances = self.variances
        if pi_k is None:
            pi_k = self.pi_k    
        # TODO
        # - comment/remove the exception
        # - calculate log-likelihood using means, variances and pi_k attr in self
        # - return the log-likelihood (Float)
        # Note: you can call this function in fit function (if required)
        # DONOT MODIFY CODE ABOVE THIS LINE
        # raise Exception('Implement compute_log_likelihood function in gmm.py')

        N, D = x.shape
        gamma = np.zeros((N, self.n_cluster))
        for k in range(self.n_cluster):
            # sigma = np.copy(self.variances[k])
            sigma = np.array([_ for _ in self.variances[k]])
            # print(sigma.shape, type(sigma))
            while not np.isfinite(np.linalg.cond(sigma)):
                sigma += .001 * np.identity(D)
            g_pdf = self.Gaussian_pdf(mean=self.means, variance=sigma)
            f = np.exp(-0.5 * np.sum(np.multiply(np.dot(x - self.means[k], np.linalg.inv(sigma)), x - self.means[k]),
                                     axis=1)) / np.sqrt(((2 * np.pi) ** D) * np.linalg.det(sigma))
            gamma[:, k] = np.multiply(self.pi_k[k], f)
        log_likelihood = float(sum(np.log(np.sum(gamma, axis=1))))


        # DONOT MODIFY CODE BELOW THIS LINE
        return log_likelihood

    class Gaussian_pdf():
        def __init__(self,mean,variance):
            self.mean = mean
            self.variance = variance
            self.c = None
            self.inv = None
            '''
                Input: 
                    Means: A 1 X D numpy array of the Gaussian mean
                    Variance: A D X D numpy array of the Gaussian covariance matrix
                Output: 
                    None: 
            '''
            # TODO
            # - comment/remove the exception
            # - Set self.inv equal to the inverse the variance matrix (after ensuring it is full rank - see P4.pdf)
            # - Set self.c equal to ((2pi)^D) * det(variance) (after ensuring the variance matrix is full rank)
            # Note you can call this class in compute_log_likelihood and fit
            # DONOT MODIFY CODE ABOVE THIS LINEs
            # raise Exception('Impliment Guassian_pdf __init__')

            d = self.mean.shape[1]
            # make invertible
            while np.linalg.det(variance) == 0:
                variance += 0.001 * np.eye(d, dtype=int)
            self.inv = np.linalg.inv(variance)
            self.c = ((2 * np.pi) ** d) * (np.linalg.det(variance))

            # DONOT MODIFY CODE BELOW THIS LINE

        def getLikelihood(self, x):
            '''
                Input:
                    x: a 1 X D numpy array representing a sample
                Output:
                    p: a numpy float, the likelihood sample x was generated by this Gaussian
                Hint:
                    p = e^(-0.5(x-mean)*(inv(variance))*(x-mean)'/sqrt(c))
                    where ' is transpose and * is matrix multiplication
            '''
            # TODO
            # - Comment/remove the exception
            # - Calculate the likelihood of sample x generated by this Gaussian
            # Note: use the described implementation of a Gaussian to ensure compatibility with the solutions
            # DONOT MODIFY CODE ABOVE THIS LINE
            # raise Exception('Impliment Guassian_pdf getLikelihood')

            p = np.exp(-0.5 * np.dot(np.dot(x - self.mean, self.inv), np.transpose(x - self.mean)) / np.sqrt(self.c))

            # DONOT MODIFY CODE BELOW THIS LINE
            return p
