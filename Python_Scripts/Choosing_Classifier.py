import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

sensorValues_train = []
labels_train = []
data_directory_train = "Training_set/4"

sensorValues_valid = []
labels_valid = []
data_directory_valid = "Testing_set/5"

gesture_labels = [
    "Not wearing glove",
    "Wearing glove",
    "letter A",
    "letter C",
    "Number 9",
    "letter I",
    "letter M",
    "Number 10",
    "letter X",
    "letter Y"
]

fileName_train = [os.path.join(data_directory_train, "Not_wearing_glove.csv"),
                  os.path.join(data_directory_train, "wore_glove.csv"),
                  os.path.join(data_directory_train, "letter_A.csv"),
                  os.path.join(data_directory_train, "letter_C.csv"),
                  os.path.join(data_directory_train, "Number_9.csv"),
                  os.path.join(data_directory_train, "letter_I.csv"),
                  os.path.join(data_directory_train, "letter_M.csv"),
                  os.path.join(data_directory_train, "Number_10.csv"),
                  os.path.join(data_directory_train, "letter_X.csv"),
                  os.path.join(data_directory_train, "letter_Y.csv")]

fileName_valid = [os.path.join(data_directory_valid, "Not_wearing_glove.csv"),
                  os.path.join(data_directory_valid, "wore_glove.csv"),
                  os.path.join(data_directory_valid, "letter_A.csv"),
                  os.path.join(data_directory_valid, "letter_C.csv"),
                  os.path.join(data_directory_valid, "Number_9.csv"),
                  os.path.join(data_directory_valid, "letter_I.csv"),
                  os.path.join(data_directory_valid, "letter_M.csv"),
                  os.path.join(data_directory_valid, "Number_10.csv"),
                  os.path.join(data_directory_valid, "letter_X.csv"),
                  os.path.join(data_directory_valid, "letter_Y.csv")]


def read_data(file_names, sensor_values, label_, label_value):
    file = open(file_names, 'r')

    # Initializing a flag to check if it's the first line to skip header
    first_line = True

    for line_ in file:
        # Check if it's the first line
        if first_line:
            first_line = False
            continue  # Skip processing the first line
        # Remove newline character, leading and trailing spaces, and split the values
        value = line_.strip().replace("'", "").split(',')

        # Convert values to integers and append to the lists
        sensor_values.append([int(val) for val in value])
        label_.append(label_value)

    file.close()


classifiers = {
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(),
    "Random Forest": RandomForestClassifier(),
    "Decision Tree": DecisionTreeClassifier()
}

overall_accuracies = []

for classifier_name, classifier in classifiers.items():
    sensorValues_train = []
    labels_train = []

    # Reading training data
    for index, file_name in enumerate(fileName_train):
        read_data(file_name, sensorValues_train, labels_train, index)

    sensorValues_train = np.array(sensorValues_train).reshape(-1, 6)
    labels_train = np.array(labels_train)

    # Reading validation data
    sensorValues_valid = []
    labels_valid = []

    for index, file_name in enumerate(fileName_valid):
        read_data(file_name, sensorValues_valid, labels_valid, index)

    sensorValues_valid = np.array(sensorValues_valid).reshape(-1, 6)
    labels_valid = np.array(labels_valid)

    # Training the classifier on the training set
    classifier.fit(sensorValues_train, labels_train)

    # Predicting on the validation set
    y_pred_valid = classifier.predict(sensorValues_valid)
    accuracy_valid = accuracy_score(labels_valid, y_pred_valid)
    overall_accuracies.append(accuracy_valid)

    print(f"Overall accuracy on the validation set ({classifier_name}): {accuracy_valid:.2%}")

# Plotting overall accuracies
plt.bar(classifiers.keys(), overall_accuracies, color='blue')
plt.title('Overall Accuracy on Validation Set for Different Classifiers')
plt.xlabel('Classifiers')
plt.ylabel('Accuracy')
plt.ylim(0, 1)
plt.yticks(np.arange(0, 1, 0.1))
plt.show()
