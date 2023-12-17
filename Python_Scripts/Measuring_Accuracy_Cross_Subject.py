import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score
from joblib import load
from sklearn.decomposition import PCA

sensorValues = []
labels = []
data_directory = "Testing_set/1"

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

# Load the saved classifier
clf_loaded = load('knn_classifier_model.joblib')

# Validate the classifier on the whole data set
y_pred_valid = clf_loaded.predict(sensorValues)

# Calculate the accuracy for the new dataset with the saved classifier
accuracy1 = accuracy_score(labels, y_pred_valid)

# Calculate individual accuracies for each class
individual_accuracies_valid = []
for label_index, label_name in enumerate(gesture_labels):
    mask = (labels == label_index)
    individual_accuracy_valid = accuracy_score(labels[mask], y_pred_valid[mask])
    individual_accuracies_valid.append(individual_accuracy_valid)

# Plotting individual accuracies for validation set
plt.figure(figsize=(10, 6))
plt.bar(gesture_labels, individual_accuracies_valid, color='blue')
plt.title('Individual Accuracies(Cross-subject)')
plt.xlabel('Gesture Labels')
plt.ylabel('Accuracy')
plt.ylim(0, 1)  # Set the y-axis limit between 0 and 1 for percentage
plt.yticks(np.arange(0, 1, 0.1))
plt.xticks(rotation=45, ha='right')
plt.axhline(y=1, color='red', linestyle='--', linewidth=3)

# Add individual accuracy values on the data points
fixed_y_positions = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

# Add individual accuracy values at fixed positions
for x, y_fixed, y_actual in zip(gesture_labels, fixed_y_positions, individual_accuracies_valid):
    plt.text(x, y_fixed, f'{y_actual:.2%}', fontsize=9, color='green', ha='center',
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
# Add overall accuracy value as a legend
overall_accuracy_text = f'Overall Accuracy (Cross Subject): {accuracy1:.2%}'
plt.legend([overall_accuracy_text], loc='lower center')
plt.tight_layout()
plt.show()

# Calculate confusion matrix for validation set
conf_matrix_valid = confusion_matrix(labels, y_pred_valid)

# Display confusion matrix for validation set
plt.figure(figsize=(5, 5))
sns.heatmap(conf_matrix_valid, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=gesture_labels, yticklabels=gesture_labels)
plt.title('Confusion Matrix (Validation Set)')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()


# Checking how well the predicted labels align with the true class labels
# Defining class names
class_names = {
    0: "Not wearing glove",
    1: "Wearing glove",
    2: "letter A",
    3: "letter C",
    4: "Number 9",
    5: "letter I",
    6: "letter M",
    7: "Number 10",
    8: "letter X",
    9: "letter Y"
}

pca = PCA(n_components=3)
X_valid_pca = pca.fit_transform(sensorValues)

# Creating 2D scatter plots for each pair of principal components
fig, axs = plt.subplots(1, 2, figsize=(18, 6))

class_colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

# Plotting the true class data clusters
for class_index in range(len(gesture_labels)):
    mask = (labels == class_index)
    axs[0].scatter(
        X_valid_pca[mask, 0], X_valid_pca[mask, 1],
        label=class_names[class_index], color=class_colors[class_index], alpha=0.5
    )

axs[0].set_xlabel('Principal Component 1')
axs[0].set_ylabel('Principal Component 2')
axs[0].set_title('True Class Data Clusters')
axs[0].legend()

# Plot the predicted values on top of the true class data clusters
for class_index in range(len(gesture_labels)):
    mask = (y_pred_valid == class_index)
    axs[1].scatter(
        X_valid_pca[mask, 0], X_valid_pca[mask, 1],
        marker='x', s=100, color=class_colors[class_index], label=class_names[class_index]
    )

axs[1].set_xlabel('Principal Component 1')
axs[1].set_ylabel('Principal Component 2')
axs[1].set_title('Predicted Values')
axs[1].legend()

plt.tight_layout()
plt.show()
