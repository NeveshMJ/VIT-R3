import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Optional: reduce TensorFlow log spam (0 = all logs, 2 = warnings+errors, 3 = errors only)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

model = load_model("civic_model.h5")

# Optional: remove "compiled metrics" warning (not required for prediction)
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")

# MUST match alphabetical order used by image_dataset_from_directory during training
class_names = [
    "garbage",
    "pothole",
    "stagnant_water",
    "streetlight_damage"
]

CONFIDENCE_THRESHOLD = 0.60

def predict_issue(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # scale to [-1, 1] for MobileNetV2

    preds = model.predict(img_array, verbose=0)
    idx = int(np.argmax(preds))
    confidence = float(np.max(preds))
    predicted_class = class_names[idx]

    if confidence < CONFIDENCE_THRESHOLD:
        return "Uncertain - Manual Review Needed", confidence

    return predicted_class, confidence

import os

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    test_image = os.path.join(BASE_DIR, "test.jpg")  # put test.jpg beside predict.py

    if not os.path.exists(test_image):
        print(f"❌ Test image not found: {test_image}")
        print("👉 Put test.jpg in the same folder as predict.py OR change the filename/path.")
    else:
        issue, conf = predict_issue(test_image)
        print("✅ Predicted Issue:", issue)
        print("✅ Confidence:", round(conf, 2))