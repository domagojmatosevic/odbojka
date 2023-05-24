import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split


if __name__ == "__main__":
    df = pd.read_csv(r"utakmice/done_data/test.csv", encoding='windows-1252')
    y = df["pobjednikDomacinIliGost"]
    df = df[['datum', 'domacin', 'gost', 'omjSvukOsSet', 'omjSvukIzgSet']]

    x_train, x_test, y_train, y_test = train_test_split(df, y, test_size=0.3, train_size=0.7, random_state=42)

    check_x = x_test
    x_train = x_train.drop(['datum', 'domacin', 'gost'], axis=1)
    x_test = x_test.drop(['datum', 'domacin', 'gost'], axis=1)

    model = GaussianNB()

    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    print("Training data accuracy is ", str(accuracy_score(y_pred, y_test) * 100), "%")
    print("F1 score is ", f1_score(y_test, y_pred, average='binary'))

    count = 0
    wrong = 0
    frames = pd.concat([check_x, y_test], axis=1, join='inner')
    predictions = model.predict(x_test)

    for x in frames.values:

        if int(predictions[count]) == 0 and x[5] == 1:
            print(x[0], x[1], "versus",
                  x[2], "is 0")
            print("Real result is ", x[5])
            wrong += 1

        elif int(predictions[count]) == 1 and x[5] == 0:
            print(x[0], x[1], "versus",
                  x[2], "is 1")
            print("Real result is ", x[5])
            wrong += 1

        count += 1

    print(wrong)
    print(len(check_x))
    print(wrong / len(check_x))