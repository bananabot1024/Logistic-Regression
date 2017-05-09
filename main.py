from random import seed, randrange
from math import exp
from sklearn import cross_validation
import pandas

# Make a prediction with coefficients
def predict(row, coefficients):
	y_pred = coefficients[0]
	for i in range(len(row)-1):
		y_pred += coefficients[i + 1] * row[i]
	return 1.0 / (1.0 + exp(-y_pred))

# Estimate logistic regression coefficients using stochastic gradient descent
def gradient_descent(X_train, Y_train, l_rate, n_epoch):
	coef = [0.0 for i in range(len(X_train[0])+1)]
	for epoch in range(n_epoch):
		for row_ind in range(len(X_train)):
			y_pred = predict(X_train[row_ind], coef)
			error = Y_train[row_ind] - y_pred
			coef[0] = coef[0] + l_rate * error * y_pred * (1.0 - y_pred)
			for i in range(len(X_train[row_ind])):
				coef[i + 1] = coef[i + 1] + l_rate * error * y_pred * (1.0 - y_pred) * X_train[row_ind][i]
	return coef

# Linear Regression Algorithm With Stochastic Gradient Descent
def logistic_regression(X_train, X_validation, Y_train, Y_validation, l_rate, n_epoch):
	predictions = list()
	coef = gradient_descent(X_train, Y_train, l_rate, n_epoch)
	for row in X_validation:
		y_pred = predict(row, coef)
		y_pred = round(y_pred)
		predictions.append(y_pred)
	return(predictions)

# load dataset
filename = "data.csv"
dataset = pandas.read_csv(filename).values

# normalize
minmax = list()
for i in range(len(dataset[0])):
    col_values = [row[i] for row in dataset]
    value_min = min(col_values)
    value_max = max(col_values)
    minmax.append([value_min, value_max])

for row in dataset:
    for i in range(len(row)):
        row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])

# X stores inputs
X = dataset[:,0:8]
# Y stores output
Y = dataset[:,8]
# dataset partitioned into 75% training, 25% testing
validation_size = 0.25
X_train, X_validation, Y_train, Y_validation = cross_validation.train_test_split(X, Y, test_size = validation_size, random_state = 1)

# evaluate algorithm
l_rate = 0.1
n_epoch = 100
predictions = logistic_regression(X_train, X_validation, Y_train, Y_validation, l_rate, n_epoch)
correct = 0
for i in range(len(Y_validation)):
    if Y_validation[i] == predictions[i]:
        correct += 1
print(correct / float(len(Y_validation)) * 100.0)
