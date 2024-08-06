# If seaborn is not installed, uncomment and run the following line:
# !pip install seaborn

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score
import seaborn as sns

# Parameters
num_samples_per_class = 100
sequence_length = 100
num_classes = 3

# Generate synthetic data
def generate_sine_wave(length):
    return np.sin(np.linspace(0, 2 * np.pi, length))

def generate_square_wave(length):
    return np.sign(np.sin(np.linspace(0, 2 * np.pi, length)))

def generate_random_noise(length):
    return np.random.randn(length)

X = []
y = []

for _ in range(num_samples_per_class):
    X.append(generate_sine_wave(sequence_length))
    y.append(0)  # Label for sine wave

    X.append(generate_square_wave(sequence_length))
    y.append(1)  # Label for square wave

    X.append(generate_random_noise(sequence_length))
    y.append(2)  # Label for random noise

X = np.array(X).reshape(-1, sequence_length, 1)
y = np.array(y)

# One-hot encode labels
y_one_hot = to_categorical(y, num_classes=num_classes)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y_one_hot, test_size=0.2, random_state=42)

# Normalize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train.reshape(-1, sequence_length)).reshape(-1, sequence_length, 1)
X_test = scaler.transform(X_test.reshape(-1, sequence_length)).reshape(-1, sequence_length, 1)

# Build the model
model = Sequential([
    Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=(sequence_length, 1)),
    MaxPooling1D(pool_size=2),
    Conv1D(filters=64, kernel_size=3, activation='relu'),
    MaxPooling1D(pool_size=2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

accuracy = accuracy_score(y_true, y_pred_classes)
print(f'Accuracy: {accuracy*100:.2f}%')

# Confusion Matrix
conf_matrix = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=['Sine', 'Square', 'Noise'], yticklabels=['Sine', 'Square', 'Noise'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# Plot test data with predicted regions
num_plots = 5
plt.figure(figsize=(15, 10))
for i in range(num_plots):
    plt.subplot(num_plots, 1, i+1)
    plt.plot(X_test[i].flatten(), label='Test Signal')
    plt.title(f'True Class: {y_true[i]}, Predicted Class: {y_pred_classes[i]}')
    plt.legend()

plt.tight_layout()
plt.show()
