import numpy as np
from sys import stderr


# Hyperparams
LEARNING_RATE_MIN = 0.000000000001
LEARNING_RATE_MAX = LEARNING_RATE_MIN * 1000
LEARNING_RATE_UP_INTERVAL = 1000000
LEARNING_RATE_UP_RATIO = 1.01
TARGET_COST = 10000
MAX_ITERATIONS = int(1 / LEARNING_RATE_MIN)
PRINT_INTERVAL = LEARNING_RATE_UP_INTERVAL / 10


def bgd(X_train, Y_train):
    """ Batch Gradient Descent Optimizer (due to high instability) """
    weights = np.zeros(len(X_train[0]))  # init weights
    lr = LEARNING_RATE_MIN
    try:
        for i in range(MAX_ITERATIONS):
                # pick data (skipped)

                # descend
                Y_pred = X_train @ weights
                loss = Y_pred - Y_train
                gradient = X_train.T @ loss
                weights -= lr * gradient

                # calculate Mean Square Error
                Y_pred = X_train @ weights
                loss = Y_pred - Y_train
                cost = np.sum(loss ** 2) / len(X_train)

                if not i % PRINT_INTERVAL:
                    print('Iteration {0}: cost={1:.2f}'.format(i, cost))

                if not (i + 1) % LEARNING_RATE_UP_INTERVAL:
                    lr = min(LEARNING_RATE_MAX, lr * 1.01)
                    if lr != LEARNING_RATE_MAX:
                        print('speed up: lr={0}'.format(lr), file=stderr)

                if cost <= TARGET_COST:  # or until MAX_ITERATIONS end
                    break
    except KeyboardInterrupt as kbi:  # training can be stopped manually by ctrl+c
        print(kbi)

    return weights
