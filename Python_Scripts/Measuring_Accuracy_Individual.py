import joblib
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from joblib import load

sensorValues = []
labels = []
data_directory = "Training_set/combined_data"

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


# Reading data for each file and appending to lists
for index, file_name in enumerate(fileName):
    read_data(file_name, sensorValues, labels, index)

# Convert lists to NumPy arrays for further processing
sensorValues = np.array(sensorValues).reshape(-1, 6)
labels = np.array(labels)

# Splitting the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(sensorValues, labels, train_size=0.6, test_size=0.4,
                                                      random_state=35,
                                                      stratify=labels)

# Training the classifier
# Calculating the square root of the total sensor values and converting it to integer
n_neighbors = int(np.sqrt(len(X_train)))
# Training classifier
print(f"Training the classifier with n_neighbors={n_neighbors}")
classifier = KNeighborsClassifier(n_neighbors=n_neighbors)
classifier.fit(X_train, y_train)

# Validate the classifier on the training set
y_pred_train = classifier.predict(X_train)
# Validate the classifier on the validation set
y_pred_valid = classifier.predict(X_valid)

# Calculate the accuracy for training set
accuracy1 = accuracy_score(y_train, y_pred_train)
# Calculate the accuracy for validation set
accuracy2 = accuracy_score(y_valid, y_pred_valid)
# print(f"Overall accuracy on the training set: {accuracy1:.2%}")
# print(f"Overall accuracy on the validation set: {accuracy2:.2%}")


# Calculate individual accuracies for each class(training set)
individual_accuracies1 = []
for label_index, label_name in enumerate(gesture_labels):
    mask = (y_train == label_index)
    individual_accuracy1 = accuracy_score(y_train[mask], y_pred_train[mask])
    individual_accuracies1.append(individual_accuracy1)
    # print(f"Accuracy for {label_name}: {individual_accuracy:.2%}")

# Plotting individual accuracies
plt.figure(figsize=(10, 6))
plt.bar(gesture_labels, individual_accuracies1, color='blue')
plt.title('Individual Accuracies')
plt.xlabel('Gesture Labels')
plt.ylabel('Accuracy')
plt.ylim(0, 1)  # Set the y-axis limit between 0 and 1 for percentage
plt.yticks(np.arange(0, 1, 0.1))
plt.xticks(rotation=45, ha='right')
# plt.axhline(y=1, color='red', linestyle='--', linewidth=3)

# Add individual accuracy values on the data points
fixed_y_positions = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

for x, y_fixed, y_actual in zip(gesture_labels, fixed_y_positions, individual_accuracies1):
    plt.text(x, y_fixed, f'{y_actual:.2%}', fontsize=9, color='green', ha='center',
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
# Add overall accuracy value as a legend
overall_accuracy_text = f'Overall Accuracy (Training Set): {accuracy1:.2%}'
plt.legend([overall_accuracy_text], loc='lower center')
plt.tight_layout()
plt.show()

# Calculate individual accuracies for each class(validation set)
individual_accuracies2 = []
for label_index, label_name in enumerate(gesture_labels):
    mask = (y_valid == label_index)
    individual_accuracy2 = accuracy_score(y_valid[mask], y_pred_valid[mask])
    individual_accuracies2.append(individual_accuracy2)
    # print(f"Accuracy for {label_name}: {individual_accuracy:.2%}")

# Plotting individual accuracies
plt.figure(figsize=(10, 6))
plt.bar(gesture_labels, individual_accuracies2, color='blue')
plt.title('Individual Accuracies')
plt.xlabel('Gesture Labels')
plt.ylabel('Accuracy')
plt.ylim(0, 1)  # Set the y-axis limit between 0 and 1 for percentage
plt.yticks(np.arange(0, 1, 0.1))
plt.xticks(rotation=45, ha='right')
# plt.axhline(y=1, color='red', linestyle='--', linewidth=3)
# Add individual accuracy values on the data points
for x, y in zip(gesture_labels, individual_accuracies2):
    plt.text(x, y - 0.5, f'{y:.2%}', fontsize=9, color='green', ha='center',
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
# Add overall accuracy value as a legend
overall_accuracy_text = f'Overall Accuracy (Validation Set): {accuracy2:.2%}'
plt.legend([overall_accuracy_text], loc='lower center')
plt.tight_layout()
plt.show()

# Calculate confusion matrix for training set
conf_matrix_train = confusion_matrix(y_train, y_pred_train)

# Display confusion matrix for training set
plt.figure(figsize=(5, 5))
sns.heatmap(conf_matrix_train, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=gesture_labels, yticklabels=gesture_labels)
plt.title('Confusion Matrix (Training Set)')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()

# Calculate confusion matrix for validation set
conf_matrix_valid = confusion_matrix(y_valid, y_pred_valid)

# Display confusion matrix for validation set
plt.figure(figsize=(5, 5))
sns.heatmap(conf_matrix_valid, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=gesture_labels, yticklabels=gesture_labels)
plt.title('Confusion Matrix (Validation Set)')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()
