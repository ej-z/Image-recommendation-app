import numpy as np
from decomposition_algorithms import Decomposition
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from tensorly import decomposition
import tensorly as tl
from scipy.sparse.linalg import eigs
from scipy.sparse import csc_matrix,random


def test():
    #cp_decomp()
    features = []
    for i in range(0,6):
        features.append('F'+str(i+1))

    A = [[90,60,90],[90,90,30],[60,60,60],[60,60,90],[30,30,30]]
    A = np.array(A)
    C = ((np.matmul(A.T , A) - (sum(A).T * sum(A) / 5)) / (5 - 1))
    V = np.sqrt(np.mat(np.diag(C)).T * np.mat(np.diag(C)))
    COV = np.divide(C, V + 1e-119)
    D = np.cov(A.T)

    A = random(500,600,density=0.25)
    #print(A)
    pca_code(A)

def cp_decomp():



    A = [[[0 for _ in range(0, 5)] for _ in range(0, 30)] for _ in range(0, 10)]
    for i in range(0, 10):
        for j in range(0, 30):
            for k in range(0, 5):
                A[i][j][k] = np.random.rand()

    H = np.array(A)
    B = decomposition.parafac(H,3)
    C = tl.kruskal_to_tensor(B)
    print(B.shape)
    k = 0

def pca_code(data):
    #raw_implementation

    #data-=np.mean(data, axis=0)
    #data/=np.std(data, axis=0)
    cov_mat=np.cov(data.todense(), rowvar=False)
    csc_mat = csc_matrix(cov_mat)
    csc_vals,csc_vec = eigs(csc_mat,5)
    evals, evecs = np.linalg.eigh(cov_mat)

    #print("evals", evals)
    print("_"*30)
    #print(evecs.T)
    print("_"*30)
    print("_" * 30)
    print("evals", csc_vals)
    print("_" * 30)
    #print(csc_vec.T)
    print("_" * 30)
    A = np.matmul(csc_vec.T,data.todense().T).T
    B = np.matmul(data.todense(),csc_vec)
    #using scipy package
    clf=PCA(n_components=5,svd_solver='arpack')

    X_train=clf.fit_transform(data.todense())
    print(clf.explained_variance_)
    print("_"*30)
    #print(clf.components_)
    print("__"*30)
    print(A == X_train)
    print(clf)


def svd_code(data):
    #raw_implementation
    evals, evecs, V = np.linalg.svd(data)
    print(evecs)
    idx = np.argsort(evals)[::-1]

    #using scipy package

    clf=TruncatedSVD(n_components=4, algorithm='arpack')
    clf.fit_transform(data)
    print(clf.explained_variance_)
