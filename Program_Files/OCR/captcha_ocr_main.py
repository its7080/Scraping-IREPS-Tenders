import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

# ==============================
# CONFIG
# ==============================
IMG_WIDTH = 160
IMG_HEIGHT = 50
BATCH_SIZE = 32
EPOCHS = 50

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
char_to_num = layers.StringLookup(vocabulary=list(CHARSET), mask_token=None)
num_to_char = layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), invert=True
)

MODEL_PATH = "captcha_ctc_model.h5"


# ==============================
# PREPROCESS
# ==============================
def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # adaptive threshold
    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    # remove lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    lines = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img = cv2.subtract(img, lines)

    # resize
    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=-1)

    return img


# ==============================
# DATA LOADER
# ==============================
def load_data(folder):
    X, y = [], []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        label = os.path.splitext(file)[0]

        if not all(c in CHARSET for c in label):
            continue

        img = preprocess_image(path)
        X.append(img)
        y.append(label)

    return np.array(X), y


def encode_labels(labels):
    encoded = []
    for label in labels:
        encoded.append(char_to_num(list(label)))
    return encoded


# ==============================
# CTC MODEL
# ==============================
def build_model():
    input_img = layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))

    x = layers.Conv2D(32, 3, activation="relu", padding="same")(input_img)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Reshape((-1, x.shape[-1]))(x)

    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True))(x)
    x = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(x)

    output = layers.Dense(len(CHARSET) + 1, activation="softmax")(x)

    model = tf.keras.Model(input_img, output)

    return model


# ==============================
# CTC LOSS
# ==============================
def ctc_loss(y_true, y_pred):
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

    return tf.keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)


# ==============================
# TRAIN
# ==============================
def train(folder):
    X, y_text = load_data(folder)
    y = encode_labels(y_text)

    y = tf.keras.preprocessing.sequence.pad_sequences(y, padding="post")

    model = build_model()

    model.compile(
        optimizer="adam",
        loss=ctc_loss
    )

    model.fit(
        X, y,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS
    )

    model.save(MODEL_PATH)
    print("✅ Model saved!")


# ==============================
# DECODE
# ==============================
def decode(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    result = tf.keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0]

    output = []
    for res in result:
        text = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output.append(text)
    return output


# ==============================
# PREDICT
# ==============================
def predict(image_path):
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects={"ctc_loss": ctc_loss}
    )

    img = preprocess_image(image_path)
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)

    text = decode(pred)[0]
    print("🔍 Prediction:", text)
    return text


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    print("1. Train")
    print("2. Predict")

    choice = input("Select: ")

    if choice == "1":
        folder = input("Dataset folder: ")
        train(folder)

    elif choice == "2":
        path = input("Image path: ")
        predict(path)