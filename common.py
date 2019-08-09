from bgd import bgd
import csv
from functools import reduce
from lsm import lsm
import matplotlib.pyplot as plt
import numpy as np
from sys import stderr
import time


# Env Settings
CSV_FILE_NAME = 'houses_info.csv'
NUM_ITEMS = 2998
NUM_TESTING_ITEMS = int(NUM_ITEMS * 0.3)


def csv2dataset(csv_file, num_test):
    """ divide csv data into training | testing sets """
    x = []
    y = []
    with open(csv_file) as f:
        rdr = csv.reader(f)
        next(rdr)  # skip table head
        # retrieve X (factors) and Y (total prices)
        for line in rdr:
            xline = [1.0]  # a1*x^0 == a1*1
            for s in line[1:]:  # skip (total) price in csv
                xline.append(float(s))
            x.append(xline)
            y.append(float(line[0]))

    x_train = np.array(x[: len(x) - num_test])
    y_train = np.transpose(np.array(y[: len(y) - num_test]))
    x_test = np.array(x[len(x) - num_test:])
    y_test = np.transpose(np.array(y[len(y) - num_test:]))

    return x_train, y_train, x_test, y_test


def train_model(X_train, Y_train, optimizer):
    """@:return weights """
    tic = time.time()
    weights = None
    if optimizer == 'lsm':
        weights = lsm(X_train, Y_train)
    elif optimizer == 'bgd':
        weights = bgd(X_train, Y_train)
    else:
        print('optimizers available: \'lsm\' or \'bgd\'', file=stderr)
        exit(1)

    print('--------------------')
    toc = time.time()
    print('time elapsed: {0:.2f} sec'.format(toc - tic))

    print('[' + optimizer + '] weights: ' + str(weights), end='\n\n')
    return weights, toc - tic


def test_model(X_test, Y_test, weights, time_cost=None):
    """ @:return avg. error rate (%) """
    ers = []
    for x, y in zip(X_test, Y_test):
        pred = np.dot(x, weights)
        er = abs(y - pred) / y * 100
        print('pred: ￥{:.2f}\t\t'.format(pred, ) + 'actual: ￥{:.0f}\t\t'.format(y) + 'error: {:.3f}%'.format(er))
        ers.append(er)

    print('--------------------')
    print('avg. error: {:.3f}%'.format(reduce(lambda a, b: a + b, ers) / len(ers)))
    if time_cost:
        print('training time cost: {:.2f} sec'.format(time_cost))


def plot_prediction(X_test, Y_test, weights):
    """ represent errors in prediction """
    # pick up 2 key factors
    X1, X2 = [], []
    Y_pred = []
    for data in X_test:
        X1.append(data[1])  # unit prices
        X2.append(data[7])  # construction areas
        x = np.array(data)
        prediction = np.dot(x, weights)
        Y_pred.append(prediction)
    X1 = np.array(X1)
    X2 = np.array(X2)
    Y_pred = np.array(Y_pred)

    # Figure 1
    plt.figure(num=1)
    plt.title('Total Prices vs. Unit Prices')
    plt.scatter(X1, Y_test, s=50, label='real value', alpha=0.5)
    plt.scatter(X1, Y_pred, s=50, label='prediction', alpha=0.5)
    plt.legend(loc='best')
    ax1 = plt.gca()
    ax1.spines['right'].set_color('none')
    ax1.spines['top'].set_color('none')

    # Figure 2
    plt.figure(num=2)
    plt.title('Total Prices vs. Construction Areas')
    plt.scatter(X2, Y_test, s=50, label='real value', alpha=0.5)
    plt.scatter(X2, Y_pred, s=50, label='prediction', alpha=0.5)
    plt.legend(loc='upper left')
    ax2 = plt.gca()
    ax2.spines['right'].set_color('none')
    ax2.spines['top'].set_color('none')

    plt.show()
