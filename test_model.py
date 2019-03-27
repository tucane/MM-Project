from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.externals import joblib

import pandas as pd
from data_utils.data_utils import getRValue
if __name__ == '__main__':
    df = pd.read_csv('ML_Fullstack/example_input/fake_data_2.csv', header=0)
    df = shuffle(df)

    df['RValue'] = df.apply(lambda x: getRValue(x[df.columns[2]]), axis=1)

    data_indices = [1, 3, 4, 5, 6, 7, 8, 9, 11, 14]
    label_indices = [12, 13]


    data_data = df.filter(items = [df.columns[idx] for idx in data_indices]).values
    data_label = df.filter(items = [df.columns[idx] for idx in label_indices]).values


    classifier = RandomForestRegressor(n_estimators=100)

    data_train, data_test, label_train, label_test = train_test_split(data_data, data_label, test_size=0.2,
                                                                                random_state=1)
    classifier.fit(data_train, label_train)

    import time
    start = time.time()
    score = classifier.score(data_test, label_test)
    end = time.time()
    print(end - start)
    print(score)


