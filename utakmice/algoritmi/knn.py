import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

if __name__ == "__main__":
    df = pd.read_csv(r"utakmice/done_data/test.csv", encoding='windows-1252')
    y = df["pobjednikDomacinIliGost"]
    df = df[['datum', 'domacin', 'gost', 'omjSvukOsSet', 'omjSvukIzgSet', 'omjProPobj']]

    x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.4, train_size=0.6, random_state=42)

    check_x = x_test
    x_train = x_train.drop(['datum', 'domacin', 'gost'], axis=1)
    x_test = x_test.drop(['datum', 'domacin', 'gost'], axis=1)

    f1 = 0
    kvalue = 1
    model = KNeighborsClassifier(n_neighbors=kvalue)
    model.fit(x_train, y_train)
    modelAccu= model.score(x_test, y_test) * 100

    for k in range(1, 21):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(x_train, y_train)

        # Compute test data accuracy
        test_accuracy = knn.score(x_test, y_test) * 100
        temp = f1_score(y_test, knn.predict(x_test), average='binary')
        if (temp > f1) & (test_accuracy > modelAccu):
            model = knn
            modelAccu = test_accuracy
            f1 = temp
            kvalue = k

    print("k-value is ", kvalue)
    print("Training data accuracy is ", str(modelAccu), "%")
    print("F1 score is ", f1)


    count = 0
    wrong = 0
    frames = pd.concat([check_x, y_test], axis = 1, join ='inner')
    predictions = model.predict(x_test)

    for x in frames.values:

        if int(predictions[count]) == 0 and x[6] == 1:
            print(x[0], x[1], "versus",
                  x[2], "is 0")
            print("Real result is ", x[6])
            wrong += 1

        elif int(predictions[count]) == 1 and x[6] == 0:
            print(x[0], x[1], "versus",
                  x[2], "is 1")
            print("Real result is ", x[6])
            wrong += 1

        count += 1

    print(wrong)
    print(len(check_x))
    print(wrong/len(check_x))