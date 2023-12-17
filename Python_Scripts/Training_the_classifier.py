import joblib
import numpy as np
import os
from sklearn.neighbors import KNeighborsClassifier

data_directory = "Training_set/combined_data"

fileName = [os.path.join(data_directory, "Not_wearing_glove.csv"),
            os.path.join(data_directory, "wore_glove.csv"),
            os.path.join(data_directory, "letter_A.csv"),
            os.path.join(data_directory, "letter_C.csv"),
            os.path.join(data_directory, "Number_9.csv"),
            os.path.join(data_directory, "letter_I.csv"),
            os.path.join(data_directory, "letter_M.csv"),
            os.path.join(data_directory, "Number_10.csv"),
            os.path.join(data_directory, "letter_X.csv"),
            os.path.join(data_directory, "letter_Y.csv")]

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

sensorValues = []
labels = []
print("Loading data from the files")


def read_data(file_names, sensor_values, label_, label_value):
    file = open(file_names, 'r')

    # Initializing a flag to check if it's the first line to skip header
    first_line = True

    for line_ in file:
        # Check if it's the first line
        if first_line:
            first_line = False
            continue  # Skip processing the first line
        value = line_.strip().replace("'", "").split(',')

        # Convert values to integers and append to the lists
        sensor_values.append([int(val) for val in value])
        label_.append(label_value)

    file.close()


# Reading data for each file and appending to lists
for index, file_name in enumerate(fileName):
    read_data(file_name, sensorValues, labels, index)

print(len(sensorValues))
# Convert lists to NumPy arrays for further processing
sensorValues = np.array(sensorValues).reshape(-1, 6)
labels = np.array(labels)

# Calculating the square root of the total sensor values and converting it to integer
n_neighbors = int(np.sqrt(len(sensorValues)))
# Training classifier
print(f"Training the classifier with n_neighbors={n_neighbors}")
classifier = KNeighborsClassifier(n_neighbors=n_neighbors)
classifier.fit(sensorValues, labels)

# Saving the trained classifier to a file
model_filename = "knn_classifier_model.joblib"
joblib.dump(classifier, model_filename)
print(f"Classifier saved to {model_filename}")
