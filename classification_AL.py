import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Load the dataset
df = pd.read_csv('dataset.csv')

# Process the data as described
df['y'] = 10 * df['Count'] * df['Horizontal Continuity'] + df['Fill %'] * df['Horizontal Continuity']

# Encode the 'Component' column for the classification model
label_encoder = LabelEncoder()
df['component_encoded'] = label_encoder.fit_transform(df['Component'])

# Plotting the data
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Aspect Ratio', y='y', hue='Component')
plt.title('Scatter plot of Aspect Ratio vs. Deviation')
plt.xlabel('Aspect Ratio')
plt.ylabel('Processed Fill')
plt.legend(title='Component')
plt.show()

# Prepare data for classification model
X = df[['Aspect Ratio', 'y']]
y = df['component_encoded']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Make predictions on the test set
y_pred = knn.predict(X_test)

# Print model accuracy
accuracy = knn.score(X_test, y_test)
print(f'KNN Classification Model Accuracy: {accuracy:.2f}')

# Compute the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot the confusion matrix using seaborn
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
1