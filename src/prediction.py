import numpy as np

import matplotlib.pyplot as plt

X = []
y = []
Xstring = []
ystring = []

disx = []
disy = []


def traing():
    training_data = np.loadtxt("dataset.txt", dtype=str, delimiter=",")
    for record in training_data:
        print(record)

        if record[0] != '':

            lis = []
            for i in range(0, len(record) - 1):
                if record[i] != '':
                    lis.append(float(record[i]))

            Xstring.append(lis)
            ystring.append(int(record[4]))


traing()
print("=====================================")

print(len(disx), disx)
print(disy)
X = Xstring
y = ystring

print(y)


def accuracy_c(feature):
    x_labels = []
    y_labels = []

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)



    from sklearn.naive_bayes import GaussianNB
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict([feature])
    if(feature[1]>3):
        return 1
    return (y_pred[0])



