from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.spatial.distance import mahalanobis
import numpy as np

a = np.array([1,2,3])

b = np.array([2,2,3])

print(mahalanobis(a,b))