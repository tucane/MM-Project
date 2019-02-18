from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import pandas as pd

def main():
    good_data = pd.read_csv('ML_Fullstack/example_input/Fake_Data_Winter.csv', header=0).fillna(0).values
    good_train = good_data[:, :10]
    good_label = good_data[:, 10:]
    good_train, good_label = shuffle(good_train, good_label)

    broken_data = pd.read_csv('ML_Fullstack/example_input/Fake_Data_Winter_V1.csv', header=0).fillna(0).values
    broken_train = broken_data[:, :10]
    broken_label = broken_data[:, 10:]
    broken_train, broken_label = shuffle(broken_train, broken_label)

    c1, c2 = RandomForestRegressor(n_estimators=100), RandomForestRegressor(n_estimators=100)
    good_data_train, good_data_test, good_labels_train, good_labels_test = train_test_split(good_train, good_label, test_size=0.2,
                                                                                random_state=1)

    broken_data_train, broken_data_test, broken_labels_train, broken_labels_test = train_test_split(broken_train, broken_label, test_size=0.2,
                                                                                random_state=1)

    c1.fit(good_data_train, good_labels_train)
    c2.fit(broken_data_train, broken_labels_train)

    print(c1.score(good_data_test, good_labels_test))
    print(c2.score(broken_data_test, broken_labels_test))





if __name__ == '__main__':
    main()