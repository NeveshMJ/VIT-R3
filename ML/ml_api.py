"""
Civic AI Image Classification API
Serves the trained MobileNetV2 model as a REST endpoint.
Accepts base64-encoded images and returns the predicted issue category,
confidence score, and mapped government department.
"""

import os
import io
import base64
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)
CORS(app)

# --------------- MODEL SETUP ---------------
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "civic_model.h5")
model = load_model(MODEL_PATH)
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")

# Must match alphabetical order used by image_dataset_from_directory during training
CLASS_NAMES = [
    "garbage",
    "pothole",
    "stagnant_water",
    "streetlight_damage",
]

CONFIDENCE_THRESHOLD = 0.60

# Department mapping per the requirement
DEPARTMENT_MAP = {
    "pothole": "Road Department",
    "garbage": "Sanitary Department",
    "stagnant_water": "Water Department",
    "streetlight_damage": "Electrical Department",
}


def predict_from_base64(base64_str: str):
    """Decode a base64 image, run inference, return (class, confidence, department)."""
    # Strip optional data-URI prefix
    if "," in base64_str:
        base64_str = base64_str.split(",", 1)[1]

    img_bytes = base64.b64decode(base64_str)
    img = image.load_img(io.BytesIO(img_bytes), target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array, verbose=0)
    idx = int(np.argmax(preds))
    confidence = float(np.max(preds))
    predicted_class = CLASS_NAMES[idx]

    department = DEPARTMENT_MAP.get(predicted_class, "General")

    if confidence < CONFIDENCE_THRESHOLD:
        return "uncertain", confidence, department

    return predicted_class, confidence, department


# --------------- ROUTES ---------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Civic AI Model Service Running", "classes": CLASS_NAMES})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON: { "image": "<base64 string or data-URI>" }
    Returns JSON: {
        "predicted_class": "pothole",
        "confidence": 0.93,
        "department": "Roads & Highways",
        "all_scores": { "garbage": 0.02, ... }
    }
    """
    data = request.get_json(force=True)
    img_b64 = data.get("image")
    if not img_b64:
        return jsonify({"error": "No image provided"}), 400

    try:
        predicted_class, confidence, department = predict_from_base64(img_b64)

        # Also return raw scores for every class
        raw = base64.b64decode(img_b64.split(",", 1)[1] if "," in img_b64 else img_b64)
        img = image.load_img(io.BytesIO(raw), target_size=(224, 224))
        arr = np.expand_dims(image.img_to_array(img), axis=0)
        arr = preprocess_input(arr)
        preds = model.predict(arr, verbose=0)[0]
        all_scores = {CLASS_NAMES[i]: round(float(preds[i]), 4) for i in range(len(CLASS_NAMES))}

        return jsonify({
            "predicted_class": predicted_class,
            "confidence": round(confidence, 4),
            "department": department,
            "all_scores": all_scores,
            "threshold": CONFIDENCE_THRESHOLD,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("ML_SERVICE_PORT", 5001))
    print(f"🚀 Civic AI Model API starting on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
