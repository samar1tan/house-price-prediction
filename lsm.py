import numpy as np


def lsm(X_train, Y_train):
    """ Least Square Method Optimizer """
    Xt = np.transpose(X_train)
    XtX = np.dot(Xt, X_train)
    XtY = np.dot(Xt, Y_train)
    weights = np.linalg.solve(XtX, XtY)

    return weights
