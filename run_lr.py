import sys

from common import *

if __name__ == '__main__':
    X_train, Y_train, X_test, Y_test = csv2dataset(CSV_FILE_NAME, NUM_TESTING_ITEMS)
    weights, time_cost = train_model(X_train, Y_train, optimizer='lsm')
    test_model(X_test, Y_test, weights, time_cost)
    plot_prediction(X_test, Y_test, weights)
else:
    print('plz run this module directly', file=sys.stderr)
