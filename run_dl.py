import sys

from keras.layers import Dense
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

from common import *


def get_model():
    # construct
    m = Sequential()
    m.add(Dense(NUM_FEATURES, input_dim=NUM_FEATURES, kernel_initializer='normal', activation='relu'))
    m.add(Dense(1, kernel_initializer='normal'))
    # Compile
    m.compile(loss='mean_squared_error', optimizer='adam')

    return m


if __name__ == '__main__':
    X_train, Y_train, X_test, Y_test = csv2dataset(CSV_FILE_NAME, NUM_TESTING_ITEMS)
    X_train = X_train.T.reshape((NUM_FEATURES, 2099))
    Y_train = Y_train.T.reshape((1, 2099))
    X_test = X_test.T
    Y_test = Y_test.T

    model = get_model()
    # fix random seed for reproducibility
    seed = 7
    np.random.seed(seed)
    # evaluate model with standardized dataset
    estimator = KerasRegressor(build_fn=model, epochs=100, batch_size=5, verbose=0)

    kfold = KFold(n_splits=10, random_state=seed)
    results = cross_val_score(estimator, X_train, Y_train, cv=kfold)
    print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))

    # weights, time_cost = train_model(X_train, Y_train, optimizer='lsm')
    # test_model(X_test, Y_test, weights, time_cost)
    # plot_prediction(X_test, Y_test, weights)
else:
    print('plz run this module directly', file=sys.stderr)
