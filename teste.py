from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

l=[]
l.append('1')
l.append('2')
l1=['11','12',14, 3, 7 , 3]
l = np.unique(l, axis=0)
print (l)
o=[]
o.append(l)
l=[]
l.append(1)
l.append(3)

o.append(l)


o = np.unique(o, axis=0)
print(o)