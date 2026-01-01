# train_ocr_cnn.py
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

DATASET_DIR = "dataset"
IMG_SIZE = 32

CHAR_CLASSES = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
char_to_idx = {c: i for i, c in enumerate(CHAR_CLASSES)}
idx_to_char = {i: c for c, i in char_to_idx.items()}


def load_dataset():
    X, y = [], []
    for char in CHAR_CLASSES:
        folder = os.path.join(DATASET_DIR, char)
        if not os.path.isdir(folder):
            continue
        for fname in os.listdir(folder):
            path = os.path.join(folder, fname)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None: continue
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = img / 255.0
            X.append(img)
            y.append(char_to_idx[char])

    X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y = to_categorical(y, num_classes=len(CHAR_CLASSES))
    return X, y

def build_model():
    model = Sequential([
        Conv2D(32, (3,3), activation="relu", input_shape=(IMG_SIZE, IMG_SIZE, 1)),
        MaxPooling2D((2,2)),
        Conv2D(64, (3,3), activation="relu"),
        MaxPooling2D((2,2)),
        Flatten(),
        Dense(128, activation="relu"),
        Dropout(0.5),
        Dense(len(CHAR_CLASSES), activation="softmax")
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return model

if __name__ == "__main__":
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = build_model()
    model.fit(X_train, y_train, epochs=15, batch_size=64, validation_data=(X_test, y_test))

    model.save("ocr_char_cnn.h5")
    print("Model saved as ocr_char_cnn.h5")
